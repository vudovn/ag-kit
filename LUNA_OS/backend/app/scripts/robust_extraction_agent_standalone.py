#!/usr/bin/env python3
"""
🌙🤖 LUNA OS v3.0 — ROBUST EXTRACTION AGENT (STANDALONE)
Versão standalone sem dependências complexas
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
from dataclasses import dataclass, asdict

# Supabase client via httpx
try:
    import httpx
except ImportError:
    print("❌ Installing httpx...")
    os.system("pip3 install httpx")
    import httpx


# ==================== CONFIG ====================

SUPABASE_URL = "https://sktrmwogifeuzrcnpvsw.supabase.co"
SUPABASE_KEY = ""  # Load from .env

# Load .env
env_file = Path("/Users/franciscotaveira.ads/LUNA OS/.env")
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                if key == 'SUPABASE_KEY':
                    SUPABASE_KEY = value


# ==================== DATA CLASSES ====================

@dataclass
class ExtractionStats:
    total_rows: int = 0
    total_bytes: int = 0
    batches_processed: int = 0
    errors: int = 0
    start_time: str = ""
    end_time: str = ""
    duration_seconds: float = 0.0
    rows_per_second: float = 0.0


# ==================== AGENTE ====================

class RobustExtractionAgent:
    """
    Agente robusto para extração de dados do Supabase (Standalone)
    """
    
    def __init__(self, table: str, output_dir: str, batch_size: int = 5000):
        self.table = table
        self.output_dir = output_dir
        self.batch_size = batch_size
        self.stats = ExtractionStats()
        self.errors = []
        self.checkpoint_file = Path(output_dir) / f".checkpoint_{table}.json"
        
        # Headers
        self.headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        # Create output dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print(f"🤖 RobustExtractionAgent initialized for table: {table}")
    
    def get_total_count(self) -> int:
        """Get total row count"""
        try:
            url = f"{SUPABASE_URL}/rest/v1/{self.table}"
            headers = self.headers.copy()
            headers["Prefer"] = "count=exact"
            params = {"limit": "1"}

            response = httpx.get(url, headers=headers, params=params, timeout=60)

            # Get count from Content-Range header
            content_range = response.headers.get("Content-Range", "")
            if "/" in content_range:
                count = int(content_range.split("/")[-1])
                print(f"   📊 Total count from header: {count:,}")
                return count

            # Fallback: try to get first batch and estimate
            print(f"   ⚠️ Content-Range not available, using fallback")
            return 50000  # Estimate

        except Exception as e:
            print(f"   ❌ Error getting count: {e}")
            return 50000  # Estimate
    
    def extract_batch(self, offset: int, limit: int) -> List[Dict]:
        """Extract a batch of rows"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                url = f"{SUPABASE_URL}/rest/v1/{self.table}"
                params = {
                    "limit": limit,
                    "offset": offset
                }
                
                response = httpx.get(url, headers=self.headers, params=params, timeout=300)
                response.raise_for_status()
                
                data = response.json()
                
                self.stats.batches_processed += 1
                self.stats.total_rows += len(data)
                self.stats.total_bytes += sum(len(json.dumps(row)) for row in data)
                
                return data
                
            except Exception as e:
                print(f"   ❌ Batch error (attempt {attempt + 1}/{max_retries}): {e}")
                self.errors.append({
                    "type": "batch_error",
                    "offset": offset,
                    "error": str(e),
                    "attempt": attempt + 1
                })
                
                if attempt < max_retries - 1:
                    time.sleep(10 * (attempt + 1))
                else:
                    raise
        
        return []
    
    def save_checkpoint(self, offset: int, data: List[Dict]):
        """Save checkpoint for resume"""
        checkpoint = {
            "table": self.table,
            "offset": offset,
            "rows_extracted": len(data),
            "timestamp": datetime.utcnow().isoformat(),
            "stats": asdict(self.stats)
        }
        
        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2)
    
    def load_checkpoint(self) -> int:
        """Load checkpoint"""
        if not self.checkpoint_file.exists():
            return 0
        
        with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
        
        return checkpoint.get("offset", 0)
    
    def save_data(self, data: List[Dict]) -> Path:
        """Save data to file"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.table}_{timestamp}.json"
        output_path = Path(self.output_dir) / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "table": self.table,
                    "extracted_at": timestamp,
                    "total_rows": len(data),
                    "total_bytes": self.stats.total_bytes
                },
                "data": data
            }, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Data saved to: {output_path}")
        
        return output_path
    
    def extract_table(self) -> Dict:
        """Extract table COMPLETE"""
        print(f"📥 Starting extraction of {self.table}...")
        
        self.stats.start_time = datetime.utcnow().isoformat()
        start_time = time.time()
        
        try:
            # 1. Get total count
            total_count = self.get_total_count()
            print(f"   📊 Total rows to extract: {total_count:,}")
            
            if total_count == 0:
                print("   ⚠️ No data to extract")
                return {"status": "error", "error": "No data"}
            
            # 2. Load checkpoint if exists
            start_offset = self.load_checkpoint()
            if start_offset > 0:
                print(f"   📍 Resuming from offset: {start_offset:,}")
            
            # 3. Extract in batches
            all_data = []
            offset = start_offset
            
            while offset < total_count:
                # Extract batch
                batch_data = self.extract_batch(offset, self.batch_size)
                
                if not batch_data:
                    print(f"   ⚠️ No more data at offset {offset}")
                    break
                
                all_data.extend(batch_data)
                offset += len(batch_data)
                
                # Save checkpoint
                self.save_checkpoint(offset, all_data)
                
                # Progress
                progress = (offset / total_count * 100) if total_count > 0 else 0
                elapsed = time.time() - start_time
                rows_per_sec = offset / elapsed if elapsed > 0 else 0
                
                print(f"   📊 Progress: {offset:,}/{total_count:,} ({progress:.1f}%) - {rows_per_sec:.1f} rows/sec")
                
                # Rate limiting
                time.sleep(0.5)
            
            # 4. Save data
            output_file = self.save_data(all_data)
            
            # Stats
            self.stats.end_time = datetime.utcnow().isoformat()
            self.stats.duration_seconds = time.time() - start_time
            self.stats.rows_per_second = self.stats.total_rows / self.stats.duration_seconds if self.stats.duration_seconds > 0 else 0
            
            print(f"✅ Extraction completed: {self.stats.total_rows:,} rows in {self.stats.duration_seconds:.1f}s")
            
            return {
                "status": "success",
                "stats": asdict(self.stats),
                "output_file": str(output_file),
                "errors": self.errors
            }
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            
            return {
                "status": "error",
                "error": str(e),
                "stats": asdict(self.stats),
                "errors": self.errors
            }


class WhatsAppExtractionSpecialist(RobustExtractionAgent):
    """
    Especialista em extração de conversas do WhatsApp
    """
    
    def __init__(self, output_dir: str):
        super().__init__(
            table="whatsapp_messages_history",
            output_dir=output_dir,
            batch_size=5000
        )
        
        print("📱 WhatsAppExtractionSpecialist initialized")
    
    def extract_complete_conversations(self) -> Dict:
        """
        Extrai conversas COMPLETAS agrupadas por phone
        """
        print("📱 Starting complete conversations extraction...")
        
        # 1. Extract all messages
        result = self.extract_table()
        
        if result.get("status") != "success":
            return result
        
        # 2. Load extracted data
        output_file = Path(result.get("output_file"))
        
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = data.get("data", [])
        
        print(f"📊 Grouping {len(messages):,} messages by phone...")
        
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
                except:
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
        
        output_path = Path(self.output_dir) / f"whatsapp_conversations_{timestamp}.json"
        
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
        
        print(f"✅ Conversations saved to: {output_path}")
        
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

def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🤖 ROBUST EXTRACTION AGENT — ATIVADO             ║")
    print("║     WhatsApp Specialist                            ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Check SUPABASE_KEY
    if not SUPABASE_KEY:
        print("❌ SUPABASE_KEY not found in .env")
        print("   Please check /Users/franciscotaveira.ads/LUNA OS/.env")
        return
    
    print(f"✅ SUPABASE_KEY loaded ({len(SUPABASE_KEY)} chars)")
    print()
    
    # Create specialist
    specialist = WhatsAppExtractionSpecialist(
        output_dir="/Users/franciscotaveira.ads/LUNA OS/logs/extractions"
    )
    
    # Extract complete conversations
    print("📱 Extracting Complete Conversations...")
    print("─" * 50)
    
    result = specialist.extract_complete_conversations()
    
    # Print result
    print()
    print("=" * 50)
    print("EXTRACTION RESULT")
    print("=" * 50)
    print()
    
    if result.get("status") == "success":
        print(f"✅ Status: SUCCESS")
        print(f"📊 Total Conversations: {result.get('total_conversations', 0):,}")
        print(f"📊 Total Messages: {result.get('total_messages', 0):,}")
        print()
        
        stats = result.get("stats", {})
        print(f"📈 CONVERSATION SIZES:")
        print(f"   • 10+ messages: {stats.get('conversations_with_10_plus', 0):,}")
        print(f"   • 50+ messages: {stats.get('conversations_with_50_plus', 0):,}")
        print(f"   • 100+ messages: {stats.get('conversations_with_100_plus', 0):,}")
        print()
        print(f"💾 Output: {result.get('output_file')}")
    else:
        print(f"❌ Status: FAILED")
        print(f"❌ Error: {result.get('error', 'Unknown')}")
        print()
    
    print()
    print("✅ Robust Extraction Agent COMPLETED!")
    print()


if __name__ == "__main__":
    main()
