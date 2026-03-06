#!/usr/bin/env python3
"""
🌙🤖 LUNA OS v3.0 — ROBUST EXTRACTION AGENT
Agente Python Especialista em Extração de Dados do Supabase
"""

import sys
import json
import time
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import hashlib

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.integrations.supabase_client import get_supabase
from loguru import logger

# Configurar logs
logger.add("logs/extraction_agent.log", rotation="100 MB", retention="90 days", level="INFO")


# ==================== DATA CLASSES ====================

@dataclass
class ExtractionStats:
    """Estatísticas da extração"""
    total_rows: int = 0
    total_bytes: int = 0
    batches_processed: int = 0
    errors: int = 0
    start_time: str = ""
    end_time: str = ""
    duration_seconds: float = 0.0
    rows_per_second: float = 0.0


@dataclass
class ExtractionConfig:
    """Configuração da extração"""
    table: str
    output_dir: str
    batch_size: int = 10000
    max_workers: int = 3
    max_retries: int = 3
    retry_delay: int = 5
    timeout_seconds: int = 300
    compress: bool = True
    format: str = "json"  # json, csv, parquet
    validate: bool = True
    resume: bool = True


# ==================== AGENTE DE EXTRAÇÃO ====================

class RobustExtractionAgent:
    """
    Agente robusto para extração de dados do Supabase
    """
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.db = get_supabase()
        self.stats = ExtractionStats()
        self.checkpoint_file = Path(config.output_dir) / f".checkpoint_{config.table}.json"
        self.errors = []
        
        # Criar output directory
        Path(config.output_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🤖 RobustExtractionAgent initialized for table: {config.table}")
    
    async def extract_table(self) -> Dict:
        """
        Extrai tabela COMPLETA com todas as otimizações
        """
        logger.info(f"📥 Starting extraction of {self.config.table}...")
        
        self.stats.start_time = datetime.utcnow().isoformat()
        start_time = time.time()
        
        try:
            # 1. Get total count
            total_count = await self._get_total_count()
            logger.info(f"   📊 Total rows to extract: {total_count:,}")
            
            # 2. Load checkpoint if resume
            start_offset = 0
            if self.config.resume and self.checkpoint_file.exists():
                start_offset = await self._load_checkpoint()
                logger.info(f"   📍 Resuming from offset: {start_offset:,}")
            
            # 3. Extract in batches
            all_data = []
            offset = start_offset
            
            while offset < total_count:
                batch_data = await self._extract_batch(offset, self.config.batch_size)
                
                if not batch_data:
                    logger.warning(f"   ⚠️ No more data at offset {offset}")
                    break
                
                all_data.extend(batch_data)
                offset += len(batch_data)
                
                # Save checkpoint
                if self.config.resume:
                    await self._save_checkpoint(offset, all_data)
                
                # Progress
                progress = (offset / total_count * 100) if total_count > 0 else 0
                logger.info(f"   📊 Progress: {offset:,}/{total_count:,} ({progress:.1f}%)")
                
                # Rate limiting
                await asyncio.sleep(0.5)
            
            # 4. Save data
            output_file = await self._save_data(all_data)
            
            # 5. Validate
            if self.config.validate:
                await self._validate_data(all_data, total_count)
            
            # Stats
            self.stats.end_time = datetime.utcnow().isoformat()
            self.stats.duration_seconds = time.time() - start_time
            self.stats.rows_per_second = self.stats.total_rows / self.stats.duration_seconds if self.stats.duration_seconds > 0 else 0
            
            logger.info(f"✅ Extraction completed: {self.stats.total_rows:,} rows in {self.stats.duration_seconds:.1f}s")
            
            return {
                "status": "success",
                "stats": asdict(self.stats),
                "output_file": str(output_file),
                "errors": self.errors
            }
            
        except Exception as e:
            logger.error(f"❌ Extraction failed: {e}")
            
            return {
                "status": "error",
                "error": str(e),
                "stats": asdict(self.stats),
                "errors": self.errors
            }
    
    async def _get_total_count(self) -> int:
        """Get total row count"""
        try:
            result = self.db.table(self.config.table).select("count", count="exact").limit(1).execute()
            return result.count if hasattr(result, 'count') else len(result.data)
        except Exception as e:
            logger.error(f"   ❌ Error getting count: {e}")
            return 0
    
    async def _extract_batch(self, offset: int, limit: int) -> List[Dict]:
        """Extract a batch of rows"""
        for attempt in range(self.config.max_retries):
            try:
                result = self.db.table(self.config.table).select("*").range(offset, offset + limit - 1).execute()
                
                data = result.data or []
                
                self.stats.batches_processed += 1
                self.stats.total_rows += len(data)
                self.stats.total_bytes += sum(len(json.dumps(row)) for row in data)
                
                return data
                
            except Exception as e:
                logger.error(f"   ❌ Batch error (attempt {attempt + 1}/{self.config.max_retries}): {e}")
                self.errors.append({
                    "type": "batch_error",
                    "offset": offset,
                    "error": str(e),
                    "attempt": attempt + 1
                })
                
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay * (attempt + 1))
                else:
                    raise
        
        return []
    
    async def _save_data(self, data: List[Dict]) -> Path:
        """Save data to file"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        if self.config.format == "json":
            filename = f"{self.config.table}_{timestamp}.json"
            output_path = Path(self.config.output_dir) / filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "metadata": {
                        "table": self.config.table,
                        "extracted_at": timestamp,
                        "total_rows": len(data),
                        "total_bytes": self.stats.total_bytes
                    },
                    "data": data
                }, f, indent=2, ensure_ascii=False)
        
        elif self.config.format == "csv":
            import csv
            
            filename = f"{self.config.table}_{timestamp}.csv"
            output_path = Path(self.config.output_dir) / filename
            
            if data:
                with open(output_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
        
        logger.info(f"💾 Data saved to: {output_path}")
        
        return output_path
    
    async def _save_checkpoint(self, offset: int, data: List[Dict]):
        """Save checkpoint for resume"""
        checkpoint = {
            "table": self.config.table,
            "offset": offset,
            "rows_extracted": len(data),
            "timestamp": datetime.utcnow().isoformat(),
            "stats": asdict(self.stats)
        }
        
        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2)
    
    async def _load_checkpoint(self) -> int:
        """Load checkpoint"""
        with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
        
        return checkpoint.get("offset", 0)
    
    async def _validate_data(self, data: List[Dict], expected_count: int):
        """Validate extracted data"""
        logger.info("🔍 Validating data...")
        
        issues = []
        
        # 1. Check count
        if len(data) < expected_count * 0.95:  # 95% tolerance
            issues.append(f"Row count mismatch: {len(data)} vs {expected_count}")
        
        # 2. Check duplicates
        ids = [row.get("id") for row in data if row.get("id")]
        duplicates = len(ids) - len(set(ids))
        
        if duplicates > 0:
            issues.append(f"Duplicate IDs found: {duplicates}")
        
        # 3. Check nulls
        null_counts = defaultdict(int)
        
        for row in data:
            for key, value in row.items():
                if value is None:
                    null_counts[key] += 1
        
        high_null_columns = {k: v for k, v in null_counts.items() if v > len(data) * 0.5}
        
        if high_null_columns:
            issues.append(f"Columns with >50% nulls: {high_null_columns}")
        
        # 4. Check data integrity
        if data and "created_at" in data[0]:
            dates = [row.get("created_at") for row in data if row.get("created_at")]
            
            if dates:
                min_date = min(dates)
                max_date = max(dates)
                
                logger.info(f"   📅 Date range: {min_date} to {max_date}")
        
        if issues:
            logger.warning(f"⚠️ Validation issues: {issues}")
            self.errors.extend([{"type": "validation", "issue": i} for i in issues])
        else:
            logger.info("✅ Validation passed")
    
    async def extract_multiple_tables(self, tables: List[str]) -> Dict:
        """Extract multiple tables"""
        logger.info(f"📥 Starting multi-table extraction: {len(tables)} tables")
        
        results = {}
        
        for i, table in enumerate(tables, 1):
            logger.info(f"📊 Table {i}/{len(tables)}: {table}")
            
            self.config.table = table
            result = await self.extract_table()
            
            results[table] = result
            
            # Delay between tables
            if i < len(tables):
                await asyncio.sleep(5)
        
        return {
            "status": "success",
            "tables": results,
            "total_tables": len(tables),
            "successful": sum(1 for r in results.values() if r.get("status") == "success"),
            "failed": sum(1 for r in results.values() if r.get("status") == "error")
        }


# ==================== WHATSAPP EXTRACTION SPECIALIST ====================

class WhatsAppExtractionSpecialist(RobustExtractionAgent):
    """
    Especialista em extração de conversas do WhatsApp
    """
    
    def __init__(self, output_dir: str):
        config = ExtractionConfig(
            table="whatsapp_messages_history",
            output_dir=output_dir,
            batch_size=5000,
            max_workers=2,
            max_retries=5,
            retry_delay=10,
            timeout_seconds=600,
            compress=False,
            format="json",
            validate=True,
            resume=True
        )
        
        super().__init__(config)
        
        logger.info("📱 WhatsAppExtractionSpecialist initialized")
    
    async def extract_complete_conversations(self) -> Dict:
        """
        Extrai conversas COMPLETAS agrupadas por phone
        """
        logger.info("📱 Starting complete conversations extraction...")
        
        # 1. Extract all messages
        result = await self.extract_table()
        
        if result.get("status") != "success":
            return result
        
        # 2. Load extracted data
        output_file = Path(result.get("output_file"))
        
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = data.get("data", [])
        
        logger.info(f"📊 Grouping {len(messages):,} messages by phone...")
        
        # 3. Group by phone
        conversations = defaultdict(list)
        
        for msg in messages:
            phone = msg.get("phone", "unknown")
            conversations[phone].append(msg)
        
        # 4. Sort messages within each conversation
        for phone in conversations:
            conversations[phone] = sorted(
                conversations[phone],
                key=lambda x: x.get("message_timestamp", "")
            )
        
        # 5. Calculate conversation stats
        conversation_stats = []
        
        for phone, msgs in conversations.items():
            inbound = [m for m in msgs if m.get("direction") == "inbound"]
            outbound = [m for m in msgs if m.get("direction") == "outbound"]
            
            # Duration
            if msgs:
                t1 = msgs[0].get("message_timestamp", "")
                t2 = msgs[-1].get("message_timestamp", "")
                
                try:
                    dt1 = datetime.fromisoformat(t1.replace("Z", "+00:00"))
                    dt2 = datetime.fromisoformat(t2.replace("Z", "+00:00"))
                    duration_minutes = (dt2 - dt1).total_seconds() / 60
                except Exception as e:
                    # [DEBT #A9] Manter fallback mas logar erro específico
                    logger.debug(f"Erro ao calcular duração: {e}")
                    duration_minutes = 0
            else:
                duration_minutes = 0
            
            conversation_stats.append({
                "phone": phone,
                "total_messages": len(msgs),
                "inbound_count": len(inbound),
                "outbound_count": len(outbound),
                "duration_minutes": duration_minutes,
                "first_message": msgs[0].get("message_timestamp") if msgs else None,
                "last_message": msgs[-1].get("message_timestamp") if msgs else None,
                "first_content": inbound[0].get("content", "")[:100] if inbound else "",
                "last_content": msgs[-1].get("content", "")[:100] if msgs else ""
            })
        
        # 6. Sort by message count
        conversation_stats = sorted(
            conversation_stats,
            key=lambda x: x["total_messages"],
            reverse=True
        )
        
        # 7. Save conversations
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        output_path = Path(self.config.output_dir) / f"whatsapp_conversations_{timestamp}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "extracted_at": timestamp,
                    "total_conversations": len(conversation_stats),
                    "total_messages": len(messages),
                    "stats": {
                        "conversations_with_10_plus": sum(1 for c in conversation_stats if c["total_messages"] >= 10),
                        "conversations_with_50_plus": sum(1 for c in conversation_stats if c["total_messages"] >= 50),
                        "conversations_with_100_plus": sum(1 for c in conversation_stats if c["total_messages"] >= 100)
                    }
                },
                "conversations": conversation_stats
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Conversations saved to: {output_path}")
        
        return {
            "status": "success",
            "total_conversations": len(conversation_stats),
            "total_messages": len(messages),
            "output_file": str(output_path),
            "stats": {
                "conversations_with_10_plus": sum(1 for c in conversation_stats if c["total_messages"] >= 10),
                "conversations_with_50_plus": sum(1 for c in conversation_stats if c["total_messages"] >= 50),
                "conversations_with_100_plus": sum(1 for c in conversation_stats if c["total_messages"] >= 100)
            }
        }


# ==================== MAIN ====================

async def main():
    """Main function"""
    logger.info("\n")
    logger.info("╔════════════════════════════════════════════════════╗")
    logger.info("║  🤖 ROBUST EXTRACTION AGENT                       ║")
    logger.info("║     WhatsApp Specialist                            ║")
    logger.info("╚════════════════════════════════════════════════════╝")
    logger.info()
    
    # Create specialist
    specialist = WhatsAppExtractionSpecialist(
        output_dir="/Users/franciscotaveira.ads/LUNA OS/logs/extractions"
    )
    
    # Extract complete conversations
    logger.info("📱 Extracting Complete Conversations...")
    logger.info("─" * 50)
    
    result = await specialist.extract_complete_conversations()
    
    # Print result
    logger.info()
    logger.info("=" * 50)
    logger.info("EXTRACTION RESULT")
    logger.info("=" * 50)
    logger.info()
    
    if result.get("status") == "success":
        logger.info(f"✅ Status: SUCCESS")
        logger.info(f"📊 Total Conversations: {result.get('total_conversations', 0):,}")
        logger.info(f"📊 Total Messages: {result.get('total_messages', 0):,}")
        logger.info()
        
        stats = result.get("stats", {})
        logger.info(f"📈 CONVERSATION SIZES:")
        logger.info(f"   • 10+ messages: {stats.get('conversations_with_10_plus', 0):,}")
        logger.info(f"   • 50+ messages: {stats.get('conversations_with_50_plus', 0):,}")
        logger.info(f"   • 100+ messages: {stats.get('conversations_with_100_plus', 0):,}")
        logger.info()
        logger.info(f"💾 Output: {result.get('output_file')}")
    else:
        logger.info(f"❌ Status: FAILED")
        logger.info(f"❌ Error: {result.get('error', 'Unknown')}")
        logger.info()
    
    logger.info()
    logger.info("✅ Robust Extraction Agent COMPLETED!")
    logger.info()


if __name__ == "__main__":
    asyncio.run(main())
