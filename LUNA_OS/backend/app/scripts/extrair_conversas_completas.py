#!/usr/bin/env python3
"""
🌙📥 LUNA OS v3.0 — EXTRAÇÃO DE CONVERSAS COMPLETAS
Extrai TODAS as mensagens COM CONTEÚDO do WhatsApp
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.integrations.supabase_client import get_supabase
from loguru import logger

# Configurar logs
logger.add("logs/extracao_conversas_completas.log", rotation="100 MB", retention="90 days")


class ExtratorConversasCompletas:
    """
    Extrai CONVERSAS COMPLETAS com TODO o conteúdo
    """
    
    def __init__(self):
        self.db = get_supabase()
        self.conversas = []
        self.estatisticas = {}
        
    async def extrair_todas_mensagens(self, batch_size: int = 10000) -> List[Dict]:
        """
        Extrai TODAS as mensagens COM CONTEÚDO
        Em batches para não sobrecarregar
        """
        logger.info("📥 Iniciando extração de TODAS as mensagens...")
        
        todas_mensagens = []
        offset = 0
        total_extraido = 0
        
        while True:
            logger.info(f"   📥 Batch {offset // batch_size + 1}...")
            
            try:
                # Extrair mensagens COM CONTENT
                result = self.db.table("whatsapp_messages_history").select("""
                    id,
                    phone,
                    direction,
                    content,
                    message_timestamp,
                    intent_detected,
                    sender_name,
                    instance_name
                """).order("message_timestamp", desc=True).range(offset, offset + batch_size - 1).execute()
                
                mensagens = result.data or []
                
                if not mensagens:
                    logger.info(f"   ✅ Fim das mensagens no offset {offset}")
                    break
                
                # Filtrar apenas mensagens COM CONTENT
                mensagens_com_content = [m for m in mensagens if m.get("content")]
                
                todas_mensagens.extend(mensagens_com_content)
                total_extraido += len(mensagens_com_content)
                
                logger.info(f"   ✅ {len(mensagens_com_content)} mensagens com conteúdo (total: {total_extraido:,})")
                
                offset += batch_size
                
                # Safety limit
                if total_extraido >= 100000:
                    logger.warning(f"   ⚠️ Limite de 100K atingido")
                    break
                    
            except Exception as e:
                logger.error(f"   ❌ Erro no batch {offset}: {e}")
                break
        
        self.estatisticas["total_mensagens_extraidas"] = total_extraido
        
        logger.info(f"✅ {total_extraido:,} mensagens extraídas com conteúdo")
        
        return todas_mensagens
    
    def agrupar_por_thread(self, mensagens: List[Dict]) -> List[Dict]:
        """
        Agrupa mensagens por phone (thread)
        """
        logger.info("📊 Agrupando por threads...")
        
        threads_dict = defaultdict(list)
        
        for msg in mensagens:
            phone = msg.get("phone", "unknown")
            threads_dict[phone].append(msg)
        
        # Ordenar mensagens dentro de cada thread
        threads = []
        
        for phone, msgs in threads_dict.items():
            # Ordenar por timestamp
            msgs_ordenadas = sorted(
                msgs,
                key=lambda x: x.get("message_timestamp", "")
            )
            
            # Calcular estatísticas do thread
            inbound = [m for m in msgs_ordenadas if m.get("direction") == "inbound"]
            outbound = [m for m in msgs_ordenadas if m.get("direction") == "outbound"]
            
            # Duração
            if msgs_ordenadas:
                t1 = msgs_ordenadas[0].get("message_timestamp", "")
                t2 = msgs_ordenadas[-1].get("message_timestamp", "")
                
                try:
                    dt1 = datetime.fromisoformat(t1.replace("Z", "+00:00"))
                    dt2 = datetime.fromisoformat(t2.replace("Z", "+00:00"))
                    duracao_minutos = (dt2 - dt1).total_seconds() / 60
                except Exception as e:
                    # [DEBT #A9] Manter fallback mas logar erro específico
                    logger.debug(f"Erro ao calcular duração: {e}")
                    duracao_minutos = 0
            else:
                duracao_minutos = 0
            
            thread = {
                "phone": phone,
                "total_mensagens": len(msgs_ordenadas),
                "inbound_count": len(inbound),
                "outbound_count": len(outbound),
                "duracao_minutos": duracao_minutos,
                "data_inicio": t1 if msgs_ordenadas else None,
                "data_fim": t2 if msgs_ordenadas else None,
                "mensagens": msgs_ordenadas,
                "primeira_mensagem": inbound[0].get("content", "")[:100] if inbound else "",
                "ultima_mensagem": msgs_ordenadas[-1].get("content", "")[:100] if msgs_ordenadas else ""
            }
            
            threads.append(thread)
        
        # Ordenar threads por número de mensagens
        threads = sorted(threads, key=lambda x: x["total_mensagens"], reverse=True)
        
        self.estatisticas["total_threads"] = len(threads)
        self.estatisticas["threads_com_10_mais"] = sum(1 for t in threads if t["total_mensagens"] >= 10)
        self.estatisticas["threads_com_50_mais"] = sum(1 for t in threads if t["total_mensagens"] >= 50)
        self.estatisticas["threads_com_100_mais"] = sum(1 for t in threads if t["total_mensagens"] >= 100)
        
        logger.info(f"✅ {len(threads)} threads agrupados")
        
        self.conversas = threads
        
        return threads
    
    def salvar_conversas(self, arquivo_json: str, arquivo_txt: str):
        """
        Salva conversas em JSON e TXT
        """
        logger.info(f"💾 Salvando conversas...")
        
        # 1. Salvar JSON completo (apenas metadados para não pesar)
        conversas_para_json = []
        
        for conv in self.conversas:
            conv_resumida = {
                "phone": conv["phone"],
                "total_mensagens": conv["total_mensagens"],
                "inbound_count": conv["inbound_count"],
                "outbound_count": conv["outbound_count"],
                "duracao_minutos": conv["duracao_minutos"],
                "data_inicio": conv["data_inicio"],
                "data_fim": conv["data_fim"],
                "primeira_mensagem": conv["primeira_mensagem"],
                "ultima_mensagem": conv["ultima_mensagem"],
                "mensagens": conv["mensagens"]  # Todas as mensagens
            }
            conversas_para_json.append(conv_resumida)
        
        with open(arquivo_json, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.utcnow().isoformat(),
                "estatisticas": self.estatisticas,
                "conversas": conversas_para_json
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 JSON salvo: {arquivo_json}")
        
        # 2. Salvar TXT legível (top 100 conversas)
        with open(arquivo_txt, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("LUNA OS — CONVERSAS COMPLETAS DO WHATSAPP\n")
            f.write(f"Extraído em: {datetime.utcnow().isoformat()}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"ESTATÍSTICAS:\n")
            f.write(f"  Total Mensagens: {self.estatisticas.get('total_mensagens_extraidas', 0):,}\n")
            f.write(f"  Total Threads: {self.estatisticas.get('total_threads', 0):,}\n")
            f.write(f"  Threads com 10+ msgs: {self.estatisticas.get('threads_com_10_mais', 0):,}\n")
            f.write(f"  Threads com 50+ msgs: {self.estatisticas.get('threads_com_50_mais', 0):,}\n")
            f.write(f"  Threads com 100+ msgs: {self.estatisticas.get('threads_com_100_mais', 0):,}\n")
            f.write("\n" + "=" * 80 + "\n\n")
            
            # Top 100 conversas
            for i, conv in enumerate(self.conversas[:100], 1):
                f.write(f"\n{'='*80}\n")
                f.write(f"CONVERSA #{i} — {conv['phone']}\n")
                f.write(f"{'='*80}\n")
                f.write(f"Mensagens: {conv['total_mensagens']}\n")
                f.write(f"Duração: {conv['duracao_minutos']:.0f} minutos\n")
                f.write(f"Início: {conv['data_inicio']}\n")
                f.write(f"Fim: {conv['data_fim']}\n")
                f.write(f"\nFLUXO DA CONVERSA:\n")
                f.write(f"{'-'*80}\n")
                
                for msg in conv["mensagens"]:
                    direction = msg.get("direction", "unknown")
                    content = msg.get("content", "")
                    timestamp = msg.get("message_timestamp", "")
                    
                    if direction == "inbound":
                        f.write(f"🧑 [{timestamp}] {content}\n")
                    else:
                        f.write(f"🤖 [{timestamp}] {content}\n")
                
                f.write(f"{'-'*80}\n")
        
        logger.info(f"💾 TXT salvo: {arquivo_txt}")
    
    def imprimir_estatisticas(self):
        """Imprime estatísticas formatadas"""
        logger.info("\n")
        logger.info("╔══════════════════════════════════════════════════════════════╗")
        logger.info("║  📥 CONVERSAS COMPLETAS — ESTATÍSTICAS                      ║")
        logger.info("╚════════════════════════════════════════════════════════════╝")
        logger.info()
        
        logger.info(f"📊 TOTAL MENSAGENS: {self.estatisticas.get('total_mensagens_extraidas', 0):,}")
        logger.info(f"📊 TOTAL THREADS: {self.estatisticas.get('total_threads', 0):,}")
        logger.info()
        
        logger.info(f"📈 THREADS POR TAMANHO:")
        logger.info(f"   • 10+ mensagens: {self.estatisticas.get('threads_com_10_mais', 0):,}")
        logger.info(f"   • 50+ mensagens: {self.estatisticas.get('threads_com_50_mais', 0):,}")
        logger.info(f"   • 100+ mensagens: {self.estatisticas.get('threads_com_100_mais', 0):,}")
        logger.info()
        
        if self.conversas:
            logger.info(f"📊 TOP 10 CONVERSAS (por número de mensagens):")
            logger.info(f"   {'#':<4} {'Phone':<15} {'Msgs':<6} {'Duração':<10} {'Início'}")
            logger.info(f"   {'─'*4} {'─'*15} {'─'*6} {'─'*10} {'─'*25}")
            
            for i, conv in enumerate(self.conversas[:10], 1):
                logger.info(f"   {i:<4} {conv['phone']:<15} {conv['total_mensagens']:<6} {conv['duracao_minutos']:<10.0f}min {conv['data_inicio'][:16] if conv['data_inicio'] else 'N/A'}
            
            logger.info()
        
        logger.info("╔══════════════════════════════════════════════════════════════╗")
        logger.info("║  📥 EXTRAÇÃO COMPLETA — CONCLUÍDA                           ║")
        logger.info("╚════════════════════════════════════════════════════════════╝")
        logger.info()


# ==================== MAIN ====================

async def main():
    """Main function"""
    logger.info("\n")
    logger.info("╔════════════════════════════════════════════════════╗")
    logger.info("║  📥 EXTRAÇÃO DE CONVERSAS COMPLETAS               ║")
    logger.info("║     TODAS as mensagens COM CONTEÚDO               ║")
    logger.info("╚════════════════════════════════════════════════════╝")
    logger.info()
    
    extrator = ExtratorConversasCompletas()
    
    # 1. Extrair todas as mensagens
    logger.info("📥 Passo 1: Extrair TODAS as Mensagens")
    logger.info("─" * 50)
    
    mensagens = await extrator.extrair_todas_mensagens(batch_size=10000)
    
    logger.info(f"✅ {len(mensagens):,} mensagens extraídas")
    logger.info()
    
    # 2. Agrupar por thread
    logger.info("📊 Passo 2: Agrupar por Threads")
    logger.info("─" * 50)
    
    threads = extrator.agrupar_por_thread(mensagens)
    
    logger.info(f"✅ {len(threads):,} threads agrupados")
    logger.info()
    
    # 3. Imprimir estatísticas
    logger.info("📊 Passo 3: Estatísticas")
    logger.info("─" * 50)
    
    extrator.imprimir_estatisticas()
    
    # 4. Salvar arquivos
    logger.info("💾 Passo 4: Salvar Arquivos")
    logger.info("─" * 50)
    
    arquivo_json = Path("/Users/franciscotaveira.ads/LUNA OS/logs/conversas_completas.json")
    arquivo_txt = Path("/Users/franciscotaveira.ads/LUNA OS/logs/conversas_completas.txt")
    
    extrator.salvar_conversas(str(arquivo_json), str(arquivo_txt))
    
    logger.info()
    logger.info("✅ Extração COMPLETA CONCLUÍDA!")
    logger.info()
    logger.info(f"📁 Arquivos:")
    logger.info(f"   • JSON: {arquivo_json}")
    logger.info(f"   • TXT: {arquivo_txt}")
    logger.info()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
