#!/usr/bin/env python3
"""
🌙💰 LUNA OS v3.0 — DOCE DAS CONTAS
Diagnóstico Financeiro Completo de Todo o Histórico
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from collections import Counter

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.integrations.supabase_client import get_supabase
from loguru import logger

# Configurar logs
logger.add("logs/doce_das_contas.log", rotation="10 MB", retention="30 days")


class DoceDasContas:
    """
    Diagnóstico financeiro completo de TODO o histórico
    """
    
    def __init__(self):
        self.db = get_supabase()
        self.dados_financeiros = []
        
    def analisar_todo_historico(self, dias: int = 1825) -> Dict:
        """
        Analisa TODO o histórico (5 anos = 1825 dias)
        """
        try:
            logger.info(f"💰 Analisando {dias} dias de histórico...")
            
            start_date = (datetime.utcnow() - timedelta(days=dias)).isoformat()
            
            # 1. Buscar todas as conversas do período
            logger.info("📥 Buscando conversas...")
            conversas = self.db.table("conversations").select("""
                id,
                phone,
                status,
                intent,
                started_at,
                ended_at
            """).gte("started_at", start_date).execute()
            
            total_conversas = len(conversas.data or [])
            logger.info(f"✅ {total_conversas} conversas encontradas")
            
            # 2. Buscar mensagens
            logger.info("📥 Buscando mensagens...")
            mensagens = self.db.table("whatsapp_messages_history").select("""
                id,
                phone,
                content,
                direction,
                message_timestamp
            """).gte("message_timestamp", start_date).execute()
            
            total_mensagens = len(mensagens.data or [])
            logger.info(f"✅ {total_mensagens} mensagens encontradas")
            
            # 3. Buscar clientes
            logger.info("📥 Buscando clientes...")
            clientes = self.db.table("clients").select("""
                id,
                phone,
                name,
                total_visits,
                total_spent,
                first_contact,
                last_contact
            """).execute()
            
            total_clientes = len(clientes.data or [])
            logger.info(f"✅ {total_clientes} clientes encontrados")
            
            # 4. Calcular métricas financeiras
            logger.info("💰 Calculando métricas...")
            
            # Clientes por status
            clientes_ativos = sum(1 for c in clientes.data if c.get('total_visits', 0) > 0)
            clientes_inativos = total_clientes - clientes_ativos
            
            # Receita total
            receita_total = sum(c.get('total_spent', 0) for c in clientes.data)
            
            # Ticket médio
            ticket_medio = receita_total / clientes_ativos if clientes_ativos > 0 else 0
            
            # Visitas totais
            visitas_totais = sum(c.get('total_visits', 0) for c in clientes.data)
            
            # Frequência média
            frequencia_media = visitas_totais / clientes_ativos if clientes_ativos > 0 else 0
            
            # 5. Análise temporal
            logger.info("📊 Análise temporal...")
            
            conversas_por_mes = Counter()
            for conv in conversas.data or []:
                started = conv.get('started_at', '')
                if len(started) >= 7:
                    mes = started[:7]  # YYYY-MM
                    conversas_por_mes[mes] += 1
            
            # 6. Análise de intenções
            logger.info("🎯 Análise de intenções...")
            
            intents_count = Counter()
            for conv in conversas.data or []:
                intent = conv.get('intent', 'unknown')
                if intent:
                    intents_count[intent] += 1
            
            # 7. Análise de conversão
            logger.info("📈 Análise de conversão...")
            
            conversas_ativas = sum(1 for c in conversas.data if c.get('status') == 'active')
            conversas_fechadas = sum(1 for c in conversas.data if c.get('status') == 'ended')
            conversas_historicas = sum(1 for c in conversas.data if c.get('status') == 'historical')
            
            taxa_conversao = (conversas_fechadas / total_conversas * 100) if total_conversas > 0 else 0
            
            # 8. Projeções
            logger.info("🔮 Projeções...")
            
            # Projeção mensal (baseado nos últimos 3 meses)
            meses_recentes = list(conversas_por_mes.keys())[-3:]
            conversas_recentes = sum(conversas_por_mes.get(m, 0) for m in meses_recentes)
            media_mensal = conversas_recentes / len(meses_recentes) if meses_recentes else 0
            
            receita_projetada_mes = media_mensal * ticket_medio
            receita_projetada_ano = receita_projetada_mes * 12
            
            # 9. Oportunidades de melhoria
            logger.info("💡 Oportunidades...")
            
            oportunidades = []
            
            # Clientes inativos
            if clientes_inativos > 0:
                oportunidades.append({
                    "tipo": "reativacao",
                    "descricao": f"{clientes_inativos} clientes inativos",
                    "potencial": clientes_inativos * ticket_medio * 0.1  # 10% de reativação
                })
            
            # Clientes com baixa frequência
            baixa_frequencia = sum(1 for c in clientes.data if c.get('total_visits', 0) < 3)
            if baixa_frequencia > 0:
                oportunidades.append({
                    "tipo": "frequencia",
                    "descricao": f"{baixa_frequencia} clientes com baixa frequência",
                    "potencial": baixa_frequencia * ticket_medio * 0.2  # 20% de melhoria
                })
            
            # Conversão baixa
            if taxa_conversao < 30 and total_conversas > 0:
                oportunidades.append({
                    "tipo": "conversao",
                    "descricao": f"Taxa de conversão baixa ({taxa_conversao:.1f}%)",
                    "potencial": receita_total * 0.15  # 15% de melhoria
                })
            
            # 10. Montar relatório
            relatorio = {
                "status": "sucesso",
                "periodo": {
                    "dias": dias,
                    "inicio": start_date,
                    "fim": datetime.utcnow().isoformat()
                },
                "resumo": {
                    "total_conversas": total_conversas,
                    "total_mensagens": total_mensagens,
                    "total_clientes": total_clientes,
                    "clientes_ativos": clientes_ativos,
                    "clientes_inativos": clientes_inativos
                },
                "financeiro": {
                    "receita_total": receita_total,
                    "ticket_medio": ticket_medio,
                    "visitas_totais": visitas_totais,
                    "frequencia_media": frequencia_media,
                    "receita_projetada_mes": receita_projetada_mes,
                    "receita_projetada_ano": receita_projetada_ano
                },
                "conversao": {
                    "conversas_ativas": conversas_ativas,
                    "conversas_fechadas": conversas_fechadas,
                    "conversas_historicas": conversas_historicas,
                    "taxa_conversao": taxa_conversao
                },
                "intencoes": dict(intents_count.most_common(10)),
                "temporal": dict(conversas_por_mes),
                "oportunidades": oportunidades,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"✅ Relatório gerado com sucesso")
            
            return relatorio
            
        except Exception as e:
            logger.error(f"❌ Erro ao analisar histórico: {e}")
            return {"status": "erro", "mensagem": str(e)}
    
    def imprimir_relatorio(self, relatorio: Dict):
        """Imprime relatório formatado"""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  💰 DOCE DAS CONTAS — DIAGNÓSTICO FINANCEIRO                ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        # Resumo
        resumo = relatorio.get('resumo', {})
        print(f"📊 RESUMO DO PERÍODO:")
        print(f"   • Total Conversas: {resumo.get('total_conversas', 0):,}")
        print(f"   • Total Mensagens: {resumo.get('total_mensagens', 0):,}")
        print(f"   • Total Clientes: {resumo.get('total_clientes', 0):,}")
        print(f"   • Clientes Ativos: {resumo.get('clientes_ativos', 0):,}")
        print(f"   • Clientes Inativos: {resumo.get('clientes_inativos', 0):,}")
        print()
        
        # Financeiro
        financeiro = relatorio.get('financeiro', {})
        print(f"💰 FINANCEIRO:")
        print(f"   • Receita Total: R$ {financeiro.get('receita_total', 0):,.2f}")
        print(f"   • Ticket Médio: R$ {financeiro.get('ticket_medio', 0):,.2f}")
        print(f"   • Visitas Totais: {financeiro.get('visitas_totais', 0):,}")
        print(f"   • Frequência Média: {financeiro.get('frequencia_media', 0):.1f} visitas/cliente")
        print()
        print(f"   • Projeção Mensal: R$ {financeiro.get('receita_projetada_mes', 0):,.2f}")
        print(f"   • Projeção Anual: R$ {financeiro.get('receita_projetada_ano', 0):,.2f}")
        print()
        
        # Conversão
        conversao = relatorio.get('conversao', {})
        print(f"📈 CONVERSÃO:")
        print(f"   • Conversas Ativas: {conversao.get('conversas_ativas', 0):,}")
        print(f"   • Conversas Fechadas: {conversao.get('conversas_fechadas', 0):,}")
        print(f"   • Conversas Históricas: {conversao.get('conversas_historicas', 0):,}")
        print(f"   • Taxa de Conversão: {conversao.get('taxa_conversao', 0):.1f}%")
        print()
        
        # Intenções
        intencoes = relatorio.get('intencoes', {})
        print(f"🎯 TOP INTENÇÕES:")
        for intent, count in list(intencoes.items())[:5]:
            print(f"   • {intent}: {count:,}")
        print()
        
        # Oportunidades
        oportunidades = relatorio.get('oportunidades', [])
        if oportunidades:
            print(f"💡 OPORTUNIDADES DE MELHORIA:")
            potencial_total = 0
            for opp in oportunidades:
                print(f"   • {opp.get('descricao', '')}")
                print(f"     Potencial: R$ {opp.get('potencial', 0):,.2f}")
                potencial_total += opp.get('potencial', 0)
            print()
            print(f"   POTENCIAL TOTAL: R$ {potencial_total:,.2f}")
            print()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  💰 DOCE DAS CONTAS — DIAGNÓSTICO CONCLUÍDO                 ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
    
    def salvar_relatorio(self, arquivo_path: str, relatorio: Dict):
        """Salva relatório em arquivo JSON"""
        try:
            with open(arquivo_path, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Relatório salvo em: {arquivo_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")


# ==================== MAIN ====================

def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  💰 DOCE DAS CONTAS — Diagnóstico Financeiro      ║")
    print("║     Análise completa de TODO o histórico          ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    doce = DoceDasContas()
    
    # Analisar todo histórico (5 anos = 1825 dias)
    print("💰 Analisando 5 anos de histórico...")
    print("─" * 50)
    
    relatorio = doce.analisar_todo_historico(dias=1825)
    
    if relatorio.get('status') == 'sucesso':
        # Imprimir relatório
        doce.imprimir_relatorio(relatorio)
        
        # Salvar relatório
        arquivo_saida = Path("/Users/franciscotaveira.ads/LUNA OS/logs/doce_das_contas_relatorio.json")
        doce.salvar_relatorio(str(arquivo_saida), relatorio)
        
        print("✅ Doce das Contas CONCLUÍDO!")
        print()
    else:
        print(f"❌ Erro: {relatorio.get('mensagem', 'Desconhecido')}")


if __name__ == "__main__":
    main()
