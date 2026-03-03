#!/usr/bin/env python3
"""
🌙🔍 LUNA OS v3.0 — ANÁLISE PROFUNDA DE THREADS DE CONVERSAÇÃO
Extrai padrões REAIS das conversas completas
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.integrations.supabase_client import get_supabase
from loguru import logger

# Configurar logs
logger.add("logs/analise_threads_profunda.log", rotation="100 MB", retention="90 days")


class AnaliseThreadsProfunda:
    """
    Análise PROFUNDA de threads de conversação
    """
    
    def __init__(self):
        self.db = get_supabase()
        self.threads = []
        self.padroes = {}
        
    async def extrair_threads_completos(self, limit: int = 5000) -> List[Dict]:
        """
        Extrai THREADS COMPLETOS de conversas
        Cada thread tem TODAS as mensagens de um cliente
        """
        logger.info(f"📥 Extraindo threads completos (limite: {limit})...")
        
        # 1. Extrair TODAS as mensagens
        mensagens_result = self.db.table("whatsapp_messages_history").select(
            "id, phone, direction, content, message_timestamp, intent_detected"
        ).order("message_timestamp", desc=True).limit(limit).execute()
        
        mensagens = mensagens_result.data or []
        
        logger.info(f"   ✅ {len(mensagens)} mensagens extraídas")
        
        # 2. Agrupar por phone (thread)
        threads_dict = defaultdict(list)
        
        for msg in mensagens:
            phone = msg.get("phone", "unknown")
            threads_dict[phone].append(msg)
        
        # 3. Ordenar mensagens por timestamp dentro de cada thread
        threads = []
        
        for phone, msgs in threads_dict.items():
            # Ordenar por timestamp
            msgs_ordenados = sorted(
                msgs,
                key=lambda x: x.get("message_timestamp", "")
            )
            
            # Calcular métricas do thread
            inbound = [m for m in msgs_ordenados if m.get("direction") == "inbound"]
            outbound = [m for m in msgs_ordenados if m.get("direction") == "outbound"]
            
            # Duração do thread (primeira vs última mensagem)
            if msgs_ordenados:
                primeira_msg = msgs_ordenados[0].get("message_timestamp", "")
                ultima_msg = msgs_ordenados[-1].get("message_timestamp", "")
                
                try:
                    t1 = datetime.fromisoformat(primeira_msg.replace("Z", "+00:00"))
                    t2 = datetime.fromisoformat(ultima_msg.replace("Z", "+00:00"))
                    duracao_minutos = (t2 - t1).total_seconds() / 60
                except:
                    duracao_minutos = 0
            else:
                duracao_minutos = 0
            
            thread = {
                "phone": phone,
                "total_mensagens": len(msgs_ordenados),
                "inbound_count": len(inbound),
                "outbound_count": len(outbound),
                "duracao_minutos": duracao_minutos,
                "mensagens": msgs_ordenados,
                "primeira_msg": primeira_msg if msgs_ordenados else None,
                "ultima_msg": ultima_msg if msgs_ordenados else None
            }
            
            threads.append(thread)
        
        # 4. Ordenar threads por número de mensagens
        threads = sorted(threads, key=lambda x: x["total_mensagens"], reverse=True)
        
        self.threads = threads
        
        logger.info(f"✅ {len(threads)} threads extraídos")
        
        return threads
    
    def analisar_padroes_conversao(self) -> Dict:
        """
        Analisa padrões de conversas que CONVERTERAM vs NÃO converteram
        """
        logger.info("📊 Analisando padrões de conversão...")
        
        # Separar threads por status (precisa buscar conversations)
        threads_convertidos = []
        threads_nao_convertidos = []
        
        for thread in self.threads:
            phone = thread["phone"]
            
            # Buscar conversation deste phone
            conv_result = self.db.table("conversations").select("status").eq("phone", phone).limit(1).execute()
            
            convs = conv_result.data or []
            
            if convs:
                status = convs[0].get("status", "unknown")
                
                if status == "ended":
                    threads_convertidos.append(thread)
                else:
                    threads_nao_convertidos.append(thread)
        
        # Analisar diferenças
        padroes = {
            "convertidos": {
                "count": len(threads_convertidos),
                "media_mensagens": sum(t["total_mensagens"] for t in threads_convertidos) / len(threads_convertidos) if threads_convertidos else 0,
                "media_duracao": sum(t["duracao_minutos"] for t in threads_convertidos) / len(threads_convertidos) if threads_convertidos else 0,
                "ratio_inbound_outbound": 0
            },
            "nao_convertidos": {
                "count": len(threads_nao_convertidos),
                "media_mensagens": sum(t["total_mensagens"] for t in threads_nao_convertidos) / len(threads_nao_convertidos) if threads_nao_convertidos else 0,
                "media_duracao": sum(t["duracao_minutos"] for t in threads_nao_convertidos) / len(threads_nao_convertidos) if threads_nao_convertidos else 0,
                "ratio_inbound_outbound": 0
            }
        }
        
        # Calcular ratio inbound/outbound
        if threads_convertidos:
            total_in = sum(t["inbound_count"] for t in threads_convertidos)
            total_out = sum(t["outbound_count"] for t in threads_convertidos)
            padroes["convertidos"]["ratio_inbound_outbound"] = total_in / total_out if total_out > 0 else 0
        
        if threads_nao_convertidos:
            total_in = sum(t["inbound_count"] for t in threads_nao_convertidos)
            total_out = sum(t["outbound_count"] for t in threads_nao_convertidos)
            padroes["nao_convertidos"]["ratio_inbound_outbound"] = total_in / total_out if total_out > 0 else 0
        
        self.padroes["conversao"] = padroes
        
        logger.info(f"✅ Padrões de conversão analisados")
        
        return padroes
    
    def analisar_jornada_cliente(self) -> List[Dict]:
        """
        Analisa jornadas COMPLETAS de clientes
        Da primeira mensagem até conversão (ou abandono)
        """
        logger.info("🗺️ Analisando jornadas de clientes...")
        
        jornadas = []
        
        # Pegar top 20 threads com mais mensagens
        top_threads = self.threads[:20]
        
        for thread in top_threads:
            phone = thread["phone"]
            
            # Extrair sequência de intents
            intents_sequence = []
            
            for msg in thread["mensagens"]:
                intent = msg.get("intent_detected")
                if intent:
                    intents_sequence.append(intent)
            
            # Analisar jornada
            jornada = {
                "phone": phone,
                "total_mensagens": thread["total_mensagens"],
                "duracao_minutos": thread["duracao_minutos"],
                "sequencia_intents": intents_sequence[:10],  # Primeiros 10 intents
                "primeiro_intent": intents_sequence[0] if intents_sequence else None,
                "ultimo_intent": intents_sequence[-1] if intents_sequence else None,
                "mudou_intent": len(set(intents_sequence)) > 1 if intents_sequence else False
            }
            
            jornadas.append(jornada)
        
        logger.info(f"✅ {len(jornadas)} jornadas analisadas")
        
        return jornadas
    
    def identificar_gatilhos_sucesso(self) -> List[Dict]:
        """
        Identifica GATILHOS que levaram ao sucesso
        Palavras, frases, padrões em conversas que converteram
        """
        logger.info("🎯 Identificando gatilhos de sucesso...")
        
        gatilhos = {
            "palavras_sucesso": Counter(),
            "palavras_fracasso": Counter(),
            "frases_sucesso": Counter(),
            "frases_fracasso": Counter()
        }
        
        # Palavras de stop (ignorar)
        stop_words = {
            "oi", "olá", "ola", "bom", "dia", "tarde", "noite",
            "obrigado", "obrigada", "valeu", "por", "favor",
            "a", "o", "as", "os", "um", "uma", "de", "do", "da"
        }
        
        # Analisar threads convertidos vs não convertidos
        for thread in self.threads[:100]:  # Top 100
            phone = thread["phone"]
            
            # Verificar se converteu
            conv_result = self.db.table("conversations").select("status").eq("phone", phone).limit(1).execute()
            converteu = any(c.get("status") == "ended" for c in conv_result.data or [])
            
            # Analisar mensagens da Luna (outbound)
            for msg in thread["mensagens"]:
                if msg.get("direction") != "outbound":
                    continue
                
                content = msg.get("content", "").lower()
                
                if not content:
                    continue
                
                # Extrair palavras
                palavras = content.split()
                
                for palavra in palavras:
                    # Limpar pontuação
                    palavra = palavra.strip(".,!?;:")
                    
                    if len(palavra) < 3 or palavra in stop_words:
                        continue
                    
                    if converteu:
                        gatilhos["palavras_sucesso"][palavra] += 1
                    else:
                        gatilhos["palavras_fracasso"][palavra] += 1
        
        # Top 20 palavras de sucesso vs fracasso
        resultado = {
            "top_palavras_sucesso": dict(gatilhos["palavras_sucesso"].most_common(20)),
            "top_palavras_fracasso": dict(gatilhos["palavras_fracasso"].most_common(20))
        }
        
        self.padroes["gatilhos"] = resultado
        
        logger.info(f"✅ Gatilhos identificados")
        
        return resultado
    
    def gerar_relatorio_completo(self) -> Dict:
        """Gera relatório completo da análise"""
        logger.info("📊 Gerando relatório completo...")
        
        relatorio = {
            "timestamp": datetime.utcnow().isoformat(),
            "threads_analisados": len(self.threads),
            "padroes": self.padroes,
            "recomendacoes": self._gerar_recomendacoes()
        }
        
        return relatorio
    
    def _gerar_recomendacoes(self) -> List[Dict]:
        """Gera recomendações baseadas na análise"""
        recomendacoes = []
        
        # Recomendação 1: Baseado em padrões de conversão
        if "conversao" in self.padroes:
            conv = self.padroes["conversao"]
            
            if conv["convertidos"]["media_mensagens"] > conv["nao_convertidos"]["media_mensagens"]:
                recomendacoes.append({
                    "tipo": "engajamento",
                    "prioridade": "alta",
                    "mensagem": "Conversas com MAIS mensagens convertem mais",
                    "acao": "Luna deve fazer mais perguntas e manter conversa ativa",
                    "dados": {
                        "convertidos": conv["convertidos"]["media_mensagens"],
                        "nao_convertidos": conv["nao_convertidos"]["media_mensagens"]
                    }
                })
            
            if conv["convertidos"]["ratio_inbound_outbound"] > 1.5:
                recomendacoes.append({
                    "tipo": "escuta",
                    "prioridade": "media",
                    "mensagem": "Clientes que falam mais convertem mais",
                    "acao": "Luna deve ouvir mais e falar menos",
                    "dados": {
                        "ratio": conv["convertidos"]["ratio_inbound_outbound"]
                    }
                })
        
        # Recomendação 2: Baseado em gatilhos
        if "gatilhos" in self.padroes:
            gatilhos = self.padroes["gatilhos"]
            
            # Palavras que aparecem em sucessos
            top_sucesso = list(gatilhos.get("top_palavras_sucesso", {}).keys())[:5]
            
            if top_sucesso:
                recomendacoes.append({
                    "tipo": "linguagem",
                    "prioridade": "media",
                    "mensagem": f"Palavras associadas a sucesso: {', '.join(top_sucesso)}",
                    "acao": "Luna deve usar mais estas palavras",
                    "dados": {
                        "palavras": top_sucesso
                    }
                })
        
        return recomendacoes
    
    def imprimir_relatorio(self):
        """Imprime relatório formatado"""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🔍 ANÁLISE PROFUNDA DE THREADS DE CONVERSAÇÃO              ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        # Resumo
        print(f"📊 THREADS ANALISADOS: {len(self.threads)}")
        print()
        
        # Padrões de conversão
        print("📈 PADRÕES DE CONVERSÃO:")
        print("─" * 70)
        
        if "conversao" in self.padroes:
            conv = self.padroes["conversao"]
            
            print(f"   ✅ CONVERTIDOS: {conv['convertidos']['count']}")
            print(f"      • Média mensagens: {conv['convertidos']['media_mensagens']:.1f}")
            print(f"      • Duração média: {conv['convertidos']['media_duracao']:.0f} min")
            print(f"      • Ratio In/Out: {conv['convertidos']['ratio_inbound_outbound']:.2f}")
            print()
            print(f"   ❌ NÃO CONVERTIDOS: {conv['nao_convertidos']['count']}")
            print(f"      • Média mensagens: {conv['nao_convertidos']['media_mensagens']:.1f}")
            print(f"      • Duração média: {conv['nao_convertidos']['media_duracao']:.0f} min")
            print(f"      • Ratio In/Out: {conv['nao_convertidos']['ratio_inbound_outbound']:.2f}")
        
        print()
        
        # Gatilhos
        print("🎯 GATILHOS DE SUCESSO:")
        print("─" * 70)
        
        if "gatilhos" in self.padroes:
            gatilhos = self.padroes["gatilhos"]
            
            print(f"   ✅ Top Palavras (Sucesso):")
            for palavra, count in list(gatilhos.get("top_palavras_sucesso", {}).items())[:10]:
                print(f"      • {palavra}: {count}")
            
            print()
            print(f"   ❌ Top Palavras (Fracasso):")
            for palavra, count in list(gatilhos.get("top_palavras_fracasso", {}).items())[:10]:
                print(f"      • {palavra}: {count}")
        
        print()
        
        # Recomendações
        print("💡 RECOMENDAÇÕES:")
        print("─" * 70)
        
        recomendacoes = self._gerar_recomendacoes()
        
        for i, rec in enumerate(recomendacoes, 1):
            print(f"   {i}. [{rec['prioridade'].upper()}] {rec['mensagem']}")
            print(f"      → {rec['acao']}")
        
        print()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🔍 ANÁLISE DE THREADS — CONCLUÍDA                          ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
    
    def salvar_relatorio(self, arquivo_path: str):
        """Salva relatório em JSON"""
        try:
            relatorio = self.gerar_relatorio_completo()
            
            with open(arquivo_path, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Relatório salvo em: {arquivo_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")


# ==================== MAIN ====================

async def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🔍 ANÁLISE PROFUNDA DE THREADS                   ║")
    print("║     Padrões REAIS de conversação                  ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    analise = AnaliseThreadsProfunda()
    
    # 1. Extrair threads completos
    print("📥 Passo 1: Extrair Threads Completos")
    print("─" * 50)
    
    threads = await analise.extrair_threads_completos(limit=5000)
    
    print(f"✅ {len(threads)} threads extraídos")
    print()
    
    # 2. Analisar padrões de conversão
    print("📊 Passo 2: Analisar Padrões de Conversão")
    print("─" * 50)
    
    padroes_conv = analise.analisar_padroes_conversao()
    
    print(f"✅ Padrões analisados")
    print()
    
    # 3. Identificar gatilhos
    print("🎯 Passo 3: Identificar Gatilhos de Sucesso")
    print("─" * 50)
    
    gatilhos = analise.identificar_gatilhos_sucesso()
    
    print(f"✅ Gatilhos identificados")
    print()
    
    # 4. Imprimir relatório
    print("📊 Passo 4: Gerar Relatório")
    print("─" * 50)
    
    analise.imprimir_relatorio()
    
    # 5. Salvar relatório
    arquivo_saida = Path("/Users/franciscotaveira.ads/LUNA OS/logs/analise_threads_profunda.json")
    analise.salvar_relatorio(str(arquivo_saida))
    
    print("✅ Análise Profunda CONCLUÍDA!")
    print()
    print(f"📁 Relatório completo: {arquivo_saida}")
    print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
