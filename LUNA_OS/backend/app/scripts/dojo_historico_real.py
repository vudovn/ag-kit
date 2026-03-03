#!/usr/bin/env python3
"""
🌙🥋 LUNA OS v3.0 — DOJO DE HISTÓRICO REAL
Usa as 40.000 mensagens REAIS para simular conversas
e testar como a Luna se sairia com situações reais
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.integrations.supabase_client import get_supabase
from app.core.brain import process_message
from loguru import logger

# Configurar logs
logger.add("logs/dojo_historico_real.log", rotation="10 MB", retention="30 days")


class DojoHistoricoReal:
    """
    Dojo que usa conversas REAIS do histórico
    para testar a Luna em situações reais
    """
    
    def __init__(self):
        self.db = get_supabase()
        self.conversas_reais = []
        self.resultados_testes = []
        
    def carregar_historico_real(self, limit: int = 1000) -> int:
        """Carrega conversas reais do Supabase"""
        try:
            logger.info(f"📥 Carregando {limit} conversas reais...")
            
            # Buscar conversas com mensagens
            result = self.db.table("whatsapp_messages_history").select("""
                id,
                phone,
                content,
                direction,
                message_timestamp,
                intent_detected
            """).order("message_timestamp", desc=True).limit(limit).execute()
            
            self.conversas_reais = result.data or []
            
            logger.info(f"✅ {len(self.conversas_reais)} conversas carregadas")
            
            return len(self.conversas_reais)
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar histórico: {e}")
            return 0
    
    def carregar_historico_de_arquivo(self, arquivo_path: str) -> int:
        """Carrega conversas de arquivo JSON (backup)"""
        try:
            logger.info(f"📥 Carregando histórico de {arquivo_path}...")
            
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Se for lista de conversas
            if isinstance(dados, list):
                self.conversas_reais = dados
            # Se for estrutura com 'conversations'
            elif isinstance(dados, dict) and 'conversations' in dados:
                self.conversas_reais = dados['conversations']
            
            logger.info(f"✅ {len(self.conversas_reais)} conversas carregadas")
            
            return len(self.conversas_reais)
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar arquivo: {e}")
            return 0
    
    async def simular_conversa(self, conversa_id: int) -> Dict:
        """
        Simula uma conversa real e compara com resposta original
        """
        try:
            if conversa_id >= len(self.conversas_reais):
                return {"status": "erro", "mensagem": "Conversa não encontrada"}
            
            conversa_real = self.conversas_reais[conversa_id]
            
            # Dados da conversa real
            phone = conversa_real.get('phone', '5549999999999')
            mensagem_cliente = conversa_real.get('content', '')
            timestamp = conversa_real.get('message_timestamp', '')
            
            # Pular se não for mensagem de cliente (inbound)
            if conversa_real.get('direction') != 'inbound':
                return {"status": "skip", "motivo": "Não é inbound"}
            
            # Processar com a Luna
            start_time = datetime.utcnow()
            resposta_luna = await process_message(
                phone=phone,
                name="Cliente Real",
                message=mensagem_cliente,
                history=[]
            )
            end_time = datetime.utcnow()
            
            # Calcular métricas
            tempo_processamento_ms = (end_time - start_time).total_seconds() * 1000
            
            # Comparar com resposta original (se existir)
            resposta_original = conversa_real.get('resposta_bot', None)
            
            resultado = {
                "conversa_id": conversa_id,
                "phone": phone,
                "timestamp": timestamp,
                "mensagem_cliente": mensagem_cliente,
                "resposta_luna": resposta_luna.get('response', ''),
                "resposta_original": resposta_original,
                "intent_luna": resposta_luna.get('intent', ''),
                "intent_original": conversa_real.get('intent_detected', ''),
                "tempo_processamento_ms": tempo_processamento_ms,
                "sentiment": resposta_luna.get('sentiment', 'unknown'),
                "confidence": resposta_luna.get('intent_confidence', 0),
                "timestamp_teste": datetime.utcnow().isoformat()
            }
            
            self.resultados_testes.append(resultado)
            
            logger.info(f"📊 Conversa {conversa_id}: {resultado['intent_luna']} ({tempo_processamento_ms:.0f}ms)")
            
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro ao simular conversa {conversa_id}: {e}")
            return {"status": "erro", "mensagem": str(e)}
    
    async def testar_todas_conversas(self) -> Dict:
        """
        Testa TODAS as conversas carregadas
        """
        try:
            logger.info(f"🧪 Iniciando teste de {len(self.conversas_reais)} conversas...")
            
            resultados = []
            
            for i, conversa in enumerate(self.conversas_reais):
                if i % 100 == 0:
                    logger.info(f"📊 Progresso: {i}/{len(self.conversas_reais)}")
                
                resultado = await self.simular_conversa(i)
                if resultado.get('status') != 'skip':
                    resultados.append(resultado)
            
            # Gerar relatório
            relatorio = self._gerar_relatorio_geral(resultados)
            
            logger.info(f"✅ Teste concluído: {len(resultados)} conversas testadas")
            
            return relatorio
            
        except Exception as e:
            logger.error(f"❌ Erro ao testar todas: {e}")
            return {"status": "erro", "mensagem": str(e)}
    
    def _gerar_relatorio_geral(self, resultados: List[Dict]) -> Dict:
        """Gera relatório geral de todos os testes"""
        try:
            if not resultados:
                return {"status": "sem_dados"}
            
            total = len(resultados)
            
            # Intents mais comuns
            intents = [r.get('intent_luna', 'unknown') for r in resultados if r.get('intent_luna')]
            intents_count = {}
            for intent in intents:
                intents_count[intent] = intents_count.get(intent, 0) + 1
            
            # Tempo médio
            tempos = [r.get('tempo_processamento_ms', 0) for r in resultados]
            tempo_medio = sum(tempos) / len(tempos) if tempos else 0
            
            # Confiança média
            confiances = [r.get('confidence', 0) for r in resultados]
            confianca_media = sum(confiances) / len(confiances) if confiances else 0
            
            # Sentimentos
            sentimentos = [r.get('sentiment', 'unknown') for r in resultados]
            sentimentos_count = {}
            for sent in sentimentos:
                sentimentos_count[sent] = sentimentos_count.get(sent, 0) + 1
            
            # Taxa de acerto de intent (comparar com original)
            acertos = 0
            for r in resultados:
                if r.get('intent_luna') == r.get('intent_original'):
                    acertos += 1
            taxa_acerto = (acertos / total * 100) if total > 0 else 0
            
            relatorio = {
                "status": "sucesso",
                "total_conversas": total,
                "tempo_medio_ms": tempo_medio,
                "confianca_media": confianca_media,
                "taxa_acerto_intent": taxa_acerto,
                "intents_detectadas": intents_count,
                "sentimentos": sentimentos_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return relatorio
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório: {e}")
            return {"status": "erro", "mensagem": str(e)}
    
    def salvar_relatorio(self, arquivo_path: str, relatorio: Dict):
        """Salva relatório em arquivo JSON"""
        try:
            with open(arquivo_path, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Relatório salvo em: {arquivo_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")
    
    def imprimir_relatorio(self, relatorio: Dict):
        """Imprime relatório formatado"""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🥋 DOJO DE HISTÓRICO REAL — RELATÓRIO                      ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        print(f"📊 Total Conversas Testadas: {relatorio.get('total_conversas', 0)}")
        print(f"⏱️ Tempo Médio: {relatorio.get('tempo_medio_ms', 0):.0f}ms")
        print(f"🎯 Confiança Média: {relatorio.get('confianca_media', 0):.1f}%")
        print(f"✅ Taxa de Acerto (Intent): {relatorio.get('taxa_acerto_intent', 0):.1f}%")
        print()
        
        print("📋 Intents Detectadas:")
        intents = relatorio.get('intents_detectadas', {})
        for intent, count in sorted(intents.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   • {intent}: {count}")
        print()
        
        print("😊 Sentimentos:")
        sentimentos = relatorio.get('sentimentos', {})
        for sent, count in sentimentos.items():
            print(f"   • {sent}: {count}")
        print()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🏆 DOJO DE HISTÓRICO REAL — CONCLUÍDO                      ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()


# ==================== MAIN ====================

async def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🥋 DOJO DE HISTÓRICO REAL                        ║")
    print("║     Testando Luna com 40.000 mensagens reais      ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    dojo = DojoHistoricoReal()
    
    # 1. Carregar histórico
    print("📥 Passo 1: Carregar Histórico Real")
    print("─" * 50)
    
    # Tentar carregar do Supabase primeiro
    count = dojo.carregar_historico_real(limit=1000)
    
    # Se não conseguir, tentar arquivo
    if count == 0:
        arquivo_backup = Path("/Users/franciscotaveira.ads/LUNA OS/logs/all_messages_full_*.json")
        import glob
        arquivos = glob.glob(str(arquivo_backup))
        if arquivos:
            count = dojo.carregar_historico_de_arquivo(arquivos[0])
    
    if count == 0:
        print("❌ Nenhum histórico encontrado")
        return
    
    print(f"✅ {count} conversas carregadas")
    print()
    
    # 2. Testar algumas conversas (exemplo)
    print("🧪 Passo 2: Testar Conversas (Exemplo)")
    print("─" * 50)
    
    # Testar primeiras 10 conversas como exemplo
    for i in range(min(10, count)):
        resultado = await dojo.simular_conversa(i)
        if resultado.get('status') == 'sucesso':
            print(f"   ✅ Conversa {i}: {resultado.get('intent_luna', 'unknown')}")
    
    print()
    
    # 3. Gerar relatório
    print("📊 Passo 3: Gerar Relatório")
    print("─" * 50)
    
    relatorio = dojo._gerar_relatorio_geral(dojo.resultados_testes)
    dojo.imprimir_relatorio(relatorio)
    
    # 4. Salvar relatório
    print("💾 Passo 4: Salvar Relatório")
    print("─" * 50)
    
    arquivo_saida = Path("/Users/franciscotaveira.ads/LUNA OS/logs/dojo_historico_real_relatorio.json")
    dojo.salvar_relatorio(str(arquivo_saida), relatorio)
    
    print()
    print("✅ Dojo de Histórico Real CONCLUÍDO!")
    print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
