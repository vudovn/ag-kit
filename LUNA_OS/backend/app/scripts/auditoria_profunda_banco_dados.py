#!/usr/bin/env python3
"""
🌙🔍 LUNA OS v3.0 — AUDITORIA HONESTA DO BANCO DE DADOS
Extração PROFUNDA e REAL das conversas do WhatsApp
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
logger.add("logs/auditoria_profunda.log", rotation="50 MB", retention="90 days")


class AuditoriaProfunda:
    """
    Auditoria HONESTA e PROFUNDA do banco de dados
    """
    
    def __init__(self):
        self.db = get_supabase()
        self.resultados = {}
        
    async def extrair_tudo(self) -> Dict:
        """
        Extrai TUDO do banco de dados
        Sem filtros, sem resumos, dados CRUS
        """
        logger.info("🔍 Iniciando extração PROFUNDA...")
        
        resultados = {
            "timestamp": datetime.utcnow().isoformat(),
            "tabelas": {},
            "relacionamentos": {},
            "padroes": {},
            "inconsistencias": [],
            "oportunidades": []
        }
        
        # 1. Extrair TODAS as tabelas
        logger.info("📥 Extraindo TODAS as tabelas...")
        
        tabelas = [
            "clients",
            "conversations",
            "whatsapp_messages_history",
            "business_intelligence",
            "learning_log",
            "dojo_feedback",
            "campaigns",
            "knowledge_base"
        ]
        
        for tabela in tabelas:
            try:
                logger.info(f"   📊 {tabela}...")
                
                # Extrair TODOS os registros
                result = self.db.table(tabela).select("*").execute()
                dados = result.data or []
                
                resultados["tabelas"][tabela] = {
                    "count": len(dados),
                    "colunas": list(dados[0].keys()) if dados else [],
                    "amostra": dados[:5] if dados else [],  # Primeiros 5 registros
                    "data_min": dados[-1].get('created_at', 'N/A') if dados else 'N/A',
                    "data_max": dados[0].get('created_at', 'N/A') if dados else 'N/A'
                }
                
                logger.info(f"   ✅ {tabela}: {len(dados)} registros")
                
            except Exception as e:
                logger.error(f"   ❌ {tabela}: {e}")
                resultados["tabelas"][tabela] = {
                    "count": 0,
                    "error": str(e)
                }
        
        # 2. Analisar relacionamentos
        logger.info("🔗 Analisando relacionamentos...")
        
        # Clients → Conversations
        clients_result = self.db.table("clients").select("phone, id").execute()
        conversations_result = self.db.table("conversations").select("phone, id").execute()
        
        clients_phones = set(c.get("phone") for c in clients_result.data) if clients_result.data else set()
        convs_phones = set(c.get("phone") for c in conversations_result.data) if conversations_result.data else set()
        
        resultados["relacionamentos"]["clients_conversations"] = {
            "clients_com_conversas": len(clients_phones & convs_phones),
            "clients_sem_conversas": len(clients_phones - convs_phones),
            "conversas_sem_client": len(convs_phones - clients_phones)
        }
        
        # 3. Analisar mensagens por conversa
        logger.info("💬 Analisando mensagens por conversa...")
        
        mensagens_result = self.db.table("whatsapp_messages_history").select(
            "phone, direction, content, message_timestamp"
        ).order("message_timestamp", desc=True).limit(10000).execute()
        
        mensagens = mensagens_result.data or []
        
        # Agrupar por phone
        mensagens_por_phone = defaultdict(list)
        for msg in mensagens:
            phone = msg.get("phone", "unknown")
            mensagens_por_phone[phone].append(msg)
        
        # Estatísticas
        counts = [len(msgs) for msgs in mensagens_por_phone.values()]
        
        resultados["padroes"]["mensagens"] = {
            "total_mensagens": len(mensagens),
            "total_phones": len(mensagens_por_phone),
            "media_mensagens_por_phone": sum(counts) / len(counts) if counts else 0,
            "max_mensagens_por_phone": max(counts) if counts else 0,
            "min_mensagens_por_phone": min(counts) if counts else 0,
            "phones_com_10_mais": sum(1 for c in counts if c >= 10),
            "phones_com_50_mais": sum(1 for c in counts if c >= 50),
            "phones_com_100_mais": sum(1 for c in counts if c >= 100)
        }
        
        # 4. Analisar distribuição de intents
        logger.info("🎯 Analisando intents...")
        
        convs_result = self.db.table("conversations").select(
            "intent, sentiment, status"
        ).execute()
        
        convs = convs_result.data or []
        
        intents_count = defaultdict(int)
        sentiments_count = defaultdict(int)
        status_count = defaultdict(int)
        
        for conv in convs:
            intent = conv.get("intent", "unknown")
            sentiment = conv.get("sentiment", "unknown")
            status = conv.get("status", "unknown")
            
            if intent:
                intents_count[intent] += 1
            if sentiment:
                sentiments_count[sentiment] += 1
            if status:
                status_count[status] += 1
        
        resultados["padroes"]["intents"] = dict(sorted(intents_count.items(), key=lambda x: x[1], reverse=True))
        resultados["padroes"]["sentiments"] = dict(sentiments_count.items())
        resultados["padroes"]["status"] = dict(status_count.items())
        
        # 5. Identificar inconsistências
        logger.info("⚠️ Identificando inconsistências...")
        
        # Mensagens sem content
        mensagens_sem_content = sum(1 for m in mensagens if not m.get("content"))
        if mensagens_sem_content > 0:
            resultados["inconsistencias"].append({
                "tipo": "mensagens_sem_content",
                "count": mensagens_sem_content,
                "impacto": "Alto - Não podemos analisar conversas sem conteúdo"
            })
        
        # Conversas sem intent
        convs_sem_intent = sum(1 for c in convs if not c.get("intent"))
        if convs_sem_intent > 0:
            resultados["inconsistencias"].append({
                "tipo": "conversas_sem_intent",
                "count": convs_sem_intent,
                "impacto": "Médio - Dificil analisar padrões sem intent"
            })
        
        # 6. Identificar oportunidades
        logger.info("💡 Identificando oportunidades...")
        
        # Oportunidade 1: Threads completos para análise
        threads_completos = sum(1 for c in counts if c >= 20)
        if threads_completos > 0:
            resultados["oportunidades"].append({
                "tipo": "threads_completos",
                "count": threads_completos,
                "descricao": f"{threads_completos} clientes com 20+ mensagens para análise profunda"
            })
        
        # Oportunidade 2: Conversas com sucesso vs fracasso
        convs_fechadas = status_count.get("ended", 0)
        convs_ativas = status_count.get("active", 0)
        
        if convs_fechadas > 0:
            resultados["oportunidades"].append({
                "tipo": "conversas_sucesso",
                "count": convs_fechadas,
                "descricao": f"{convs_fechadas} conversas fechadas para analisar padrões de sucesso"
            })
        
        # Oportunidade 3: BI já coletado
        bi_result = self.db.table("business_intelligence").select("*").limit(100).execute()
        bi_count = len(bi_result.data) if bi_result.data else 0
        
        if bi_count > 0:
            resultados["oportunidades"].append({
                "tipo": "business_intelligence",
                "count": bi_count,
                "descricao": f"{bi_count} registros de BI para análise de insights"
            })
        
        logger.info(f"✅ Auditoria profunda concluída")
        
        self.resultados = resultados
        
        return resultados
    
    def imprimir_relatorio(self):
        """Imprime relatório formatado"""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🔍 AUDITORIA HONESTA DO BANCO DE DADOS                     ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        # Tabelas
        print("📊 TABELAS EXTRAÍDAS:")
        print("─" * 70)
        for tabela, dados in self.resultados.get("tabelas", {}).items():
            count = dados.get("count", 0)
            print(f"   • {tabela}: {count:,} registros")
            if dados.get("colunas"):
                print(f"     Colunas: {', '.join(dados['colunas'][:5])}...")
        print()
        
        # Relacionamentos
        print("🔗 RELACIONAMENTOS:")
        print("─" * 70)
        rels = self.resultados.get("relacionamentos", {})
        for rel, dados in rels.items():
            print(f"   • {rel}:")
            for key, value in dados.items():
                print(f"     {key}: {value:,}")
        print()
        
        # Padrões
        print("📊 PADRÕES ENCONTRADOS:")
        print("─" * 70)
        padroes = self.resultados.get("padroes", {})
        
        if "mensagens" in padroes:
            msgs = padroes["mensagens"]
            print(f"   💬 Mensagens:")
            print(f"     • Total: {msgs.get('total_mensagens', 0):,}")
            print(f"     • Por cliente (média): {msgs.get('media_mensagens_por_phone', 0):.1f}")
            print(f"     • Por cliente (max): {msgs.get('max_mensagens_por_phone', 0):,}")
            print(f"     • Clientes com 10+ msgs: {msgs.get('phones_com_10_mais', 0):,}")
            print(f"     • Clientes com 50+ msgs: {msgs.get('phones_com_50_mais', 0):,}")
            print(f"     • Clientes com 100+ msgs: {msgs.get('phones_com_100_mais', 0):,}")
            print()
        
        if "intents" in padroes:
            print(f"   🎯 Top Intents:")
            intents = padroes["intents"]
            for intent, count in list(intents.items())[:10]:
                print(f"     • {intent}: {count:,}")
            print()
        
        if "sentiments" in padroes:
            print(f"   😊 Sentimentos:")
            sentiments = padroes["sentiments"]
            for sentiment, count in sentiments.items():
                print(f"     • {sentiment}: {count:,}")
            print()
        
        # Inconsistências
        print("⚠️ INCONSISTÊNCIAS:")
        print("─" * 70)
        inconsistencias = self.resultados.get("inconsistencias", [])
        if inconsistencias:
            for inc in inconsistencias:
                print(f"   ❌ {inc['tipo']}: {inc['count']:,} ({inc['impacto']})")
        else:
            print("   ✅ Nenhuma inconsistência crítica encontrada")
        print()
        
        # Oportunidades
        print("💡 OPORTUNIDADES:")
        print("─" * 70)
        oportunidades = self.resultados.get("oportunidades", [])
        if oportunidades:
            for opp in oportunidades:
                print(f"   💡 {opp['tipo']}: {opp['descricao']}")
        else:
            print("   ⚠️ Nenhuma oportunidade identificada")
        print()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🔍 AUDITORIA HONESTA — CONCLUÍDA                           ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
    
    def salvar_relatorio(self, arquivo_path: str):
        """Salva relatório completo em JSON"""
        try:
            # Remover amostras grandes para não pesar o JSON
            relatorio_limpo = json.loads(json.dumps(self.resultados, default=str))
            
            with open(arquivo_path, 'w', encoding='utf-8') as f:
                json.dump(relatorio_limpo, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Relatório salvo em: {arquivo_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")


# ==================== MAIN ====================

async def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🔍 AUDITORIA HONESTA DO BANCO DE DADOS           ║")
    print("║     Extração PROFUNDA e REAL                      ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    auditoria = AuditoriaProfunda()
    
    # Extrair tudo
    print("🔍 Extraindo TODOS os dados...")
    print("─" * 50)
    
    resultados = await auditoria.extrair_tudo()
    
    # Imprimir relatório
    auditoria.imprimir_relatorio()
    
    # Salvar relatório
    arquivo_saida = Path("/Users/franciscotaveira.ads/LUNA OS/logs/auditoria_profunda_completa.json")
    auditoria.salvar_relatorio(str(arquivo_saida))
    
    print("✅ Auditoria Honesta CONCLUÍDA!")
    print()
    print(f"📁 Relatório completo: {arquivo_saida}")
    print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
