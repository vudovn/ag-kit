#!/usr/bin/env python3
"""
🌙💼 LUNA OS — WhatsApp Sales Intelligence Report
Relatório Completo de Inteligência de Vendas via WhatsApp

Analisa TODAS as conversas e extrai insights como um analista de vendas sênior.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.integrations.supabase_client import get_supabase
from loguru import logger
import httpx

logger.add("logs/sales_intelligence.log", rotation="10 MB", retention="30 days")


class WhatsAppSalesAnalyst:
    """
    Analista de Vendas via WhatsApp - MCT Intelligence
    """
    
    def __init__(self):
        self.db = get_supabase()
        self.conversations = []
        self.clients = []
        self.messages = []
        self.analytics = {}
        
    def fetch_all_data(self, days: int = 30):
        """Busca TODOS os dados do Supabase"""
        logger.info("📊 Buscando dados no Supabase...")
        
        # Conversas
        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        conv_result = self.db.table("conversations").select("*").gte("started_at", start_date).execute()
        self.conversations = conv_result.data or []
        logger.info(f"✅ {len(self.conversations)} conversas encontradas")
        
        # Clientes
        clients_result = self.db.table("clients").select("*").execute()
        self.clients = clients_result.data or []
        logger.info(f"✅ {len(self.clients)} clientes encontrados")
        
        # Mensagens (histórico WhatsApp)
        msg_result = self.db.table("whatsapp_messages_history").select("*").gte("message_timestamp", start_date).execute()
        self.messages = msg_result.data or []
        logger.info(f"✅ {len(self.messages)} mensagens encontradas")
        
        return len(self.conversations) > 0
    
    def analyze_conversation_volume(self) -> Dict:
        """Analisa volume de conversas por período"""
        if not self.conversations:
            return {}
        
        # Por dia
        by_day = Counter()
        for conv in self.conversations:
            day = conv.get('started_at', '')[:10]
            by_day[day] += 1
        
        # Por status
        by_status = Counter(conv.get('status', 'unknown') for conv in self.conversations)
        
        # Por intent
        by_intent = Counter(conv.get('intent', 'unknown') for conv in self.conversations if conv.get('intent'))
        
        # Por sentiment
        by_sentiment = Counter(conv.get('sentiment', 'unknown') for conv in self.conversations if conv.get('sentiment'))
        
        return {
            'total_conversations': len(self.conversations),
            'by_day': dict(by_day.most_common()),
            'by_status': dict(by_status),
            'by_intent': dict(by_intent.most_common()),
            'by_sentiment': dict(by_sentiment),
            'avg_per_day': len(self.conversations) / max(len(by_day), 1)
        }
    
    def analyze_client_behavior(self) -> Dict:
        """Analisa comportamento dos clientes"""
        if not self.clients:
            return {}
        
        # Clientes com tags
        tagged_clients = [c for c in self.clients if c.get('tags')]
        
        # Clientes recorrentes (mais de 1 conversa)
        client_conv_count = Counter(conv.get('phone') for conv in self.conversations)
        returning_clients = sum(1 for count in client_conv_count.values() if count > 1)
        
        # Top clientes por conversa
        top_clients = client_conv_count.most_common(10)
        
        # Tags mais comuns
        all_tags = []
        for client in self.clients:
            all_tags.extend(client.get('tags', []))
        top_tags = Counter(all_tags).most_common(10)
        
        return {
            'total_clients': len(self.clients),
            'tagged_clients': len(tagged_clients),
            'returning_clients': returning_clients,
            'top_clients_by_conversations': top_clients,
            'top_tags': top_tags,
            'returning_rate': (returning_clients / len(self.clients) * 100) if self.clients else 0
        }
    
    def analyze_message_patterns(self) -> Dict:
        """Analisa padrões de mensagens"""
        if not self.messages:
            return {}
        
        # Por direção
        by_direction = Counter(msg.get('direction', 'unknown') for msg in self.messages)
        
        # Por tipo
        by_type = Counter(msg.get('message_type', 'unknown') for msg in self.messages)
        
        # Por horário
        by_hour = Counter()
        for msg in self.messages:
            timestamp = msg.get('message_timestamp', '')
            if len(timestamp) > 13:
                hour = timestamp[11:13]
                by_hour[hour] += 1
        
        # Mensagens por cliente
        by_phone = Counter(msg.get('phone') for msg in self.messages)
        top_talkers = by_phone.most_common(10)
        
        return {
            'total_messages': len(self.messages),
            'by_direction': dict(by_direction),
            'by_type': dict(by_type),
            'by_hour': dict(sorted(by_hour.items())),
            'top_talkers': top_talkers,
            'avg_messages_per_client': len(self.messages) / len(by_phone) if by_phone else 0
        }
    
    def analyze_sales_funnel(self) -> Dict:
        """Analisa funil de vendas"""
        if not self.conversations:
            return {}
        
        # Funil por intent (sinal de interesse)
        intents = [conv.get('intent') for conv in self.conversations if conv.get('intent')]
        
        # Interesse alto (agendamento, pacote, preco)
        high_intent = sum(1 for i in intents if i in ['agendar', 'agendamento', 'pacote', 'preco'])
        
        # Interesse médio (servicos, historico)
        medium_intent = sum(1 for i in intents if i in ['servicos', 'historico', 'multi_servico'])
        
        # Interesse baixo (saudacao, conversas)
        low_intent = sum(1 for i in intents if i in ['saudacao', 'conversa', 'horario_func', 'localizacao'])
        
        # Conversão (status ended com sentiment positive)
        converted = sum(1 for conv in self.conversations 
                       if conv.get('status') == 'ended' and conv.get('sentiment') == 'positive')
        
        return {
            'total_leads': len(self.conversations),
            'high_intent': high_intent,
            'high_intent_rate': (high_intent / len(intents) * 100) if intents else 0,
            'medium_intent': medium_intent,
            'medium_intent_rate': (medium_intent / len(intents) * 100) if intents else 0,
            'low_intent': low_intent,
            'low_intent_rate': (low_intent / len(intents) * 100) if intents else 0,
            'converted': converted,
            'conversion_rate': (converted / len(self.conversations) * 100) if self.conversations else 0
        }
    
    def analyze_response_time(self) -> Dict:
        """Analisa tempo de resposta"""
        # Nota: Requer dados mais detalhados de timestamps
        # Por enquanto, usa estimativas baseadas em conversas ativas
        
        active_convs = [c for c in self.conversations if c.get('status') == 'active']
        ended_convs = [c for c in self.conversations if c.get('status') == 'ended']
        
        return {
            'active_conversations': len(active_convs),
            'ended_conversations': len(ended_convs),
            'active_rate': (len(active_convs) / len(self.conversations) * 100) if self.conversations else 0
        }
    
    def identify_objections(self) -> Dict:
        """Identifica objeções de vendas"""
        # Busca no business_intelligence
        bi_result = self.db.table("business_intelligence").select("*").execute()
        bi_data = bi_result.data or []
        
        # Agrupa objeções
        all_objections = []
        for entry in bi_data:
            objections = entry.get('objections', [])
            if isinstance(objections, list):
                all_objections.extend(objections)
        
        objection_counts = Counter(all_objections)
        
        return {
            'total_objections': len(all_objections),
            'top_objections': objection_counts.most_common(10),
            'objection_rate': (len(all_objections) / len(self.conversations) * 100) if self.conversations else 0
        }
    
    def analyze_customer_mood(self) -> Dict:
        """Analisa humor dos clientes"""
        # Busca no business_intelligence
        bi_result = self.db.table("business_intelligence").select("*").execute()
        bi_data = bi_result.data or []
        
        moods = Counter(entry.get('customer_mood', 'unknown') for entry in bi_data if entry.get('customer_mood'))
        urgencies = Counter(entry.get('urgency_level', 3) for entry in bi_data if entry.get('urgency_level'))
        
        return {
            'mood_distribution': dict(moods),
            'urgency_distribution': dict(urgencies),
            'avg_urgency': sum(urgencies.elements()) / len(urgencies) if urgencies else 0
        }
    
    def generate_insights(self) -> List[Dict]:
        """Gera insights acionáveis"""
        insights = []
        
        # Volume insights
        vol = self.analytics.get('conversation_volume', {})
        if vol.get('avg_per_day', 0) < 5:
            insights.append({
                'type': 'warning',
                'category': 'volume',
                'title': 'Volume Baixo de Conversas',
                'description': f'Média de apenas {vol.get("avg_per_day"):.1f} conversas/dia',
                'recommendation': 'Aumentar investimento em tráfego e captação de leads'
            })
        
        # Funnel insights
        funnel = self.analytics.get('sales_funnel', {})
        if funnel.get('high_intent_rate', 0) < 20:
            insights.append({
                'type': 'warning',
                'category': 'funnel',
                'title': 'Baixa Intenção de Compra',
                'description': f'Apenas {funnel.get("high_intent_rate"):.1f}% demonstram alto interesse',
                'recommendation': 'Melhorar qualificação de leads e copy de captação'
            })
        
        if funnel.get('conversion_rate', 0) < 30:
            insights.append({
                'type': 'critical',
                'category': 'conversion',
                'title': 'Taxa de Conversão Baixa',
                'description': f'Taxa de conversão de apenas {funnel.get("conversion_rate"):.1f}%',
                'recommendation': 'Revisar script de vendas, oferecer promoções, melhorar follow-up'
            })
        
        # Response time insights
        resp = self.analytics.get('response_time', {})
        if resp.get('active_rate', 0) > 50:
            insights.append({
                'type': 'warning',
                'category': 'response',
                'title': 'Muitas Conversas Ativas',
                'description': f'{resp.get("active_rate"):.1f}% das conversas estão ativas (sem fechamento)',
                'recommendation': 'Implementar follow-up automático e criar senso de urgência'
            })
        
        # Objection insights
        obj = self.analytics.get('objections', {})
        if obj.get('objection_rate', 0) > 30:
            insights.append({
                'type': 'warning',
                'category': 'objections',
                'title': 'Alta Taxa de Objeções',
                'description': f'{obj.get("objection_rate"):.1f}% das conversas têm objeções',
                'recommendation': 'Criar FAQ proativo, antecipar objeções comuns'
            })
        
        # Mood insights
        mood = self.analytics.get('customer_mood', {})
        mood_dist = mood.get('mood_distribution', {})
        if mood_dist.get('frustrated', 0) > mood_dist.get('happy', 0):
            insights.append({
                'type': 'critical',
                'category': 'satisfaction',
                'title': 'Clientes Frustrados',
                'description': 'Mais clientes frustrados do que felizes',
                'recommendation': 'Revisar atendimento, treinar equipe em empatia'
            })
        
        return insights
    
    def generate_report(self, days: int = 30) -> Dict:
        """Gera relatório completo"""
        logger.info("📊 Gerando relatório de inteligência de vendas...")
        
        # Fetch data
        self.fetch_all_data(days=days)
        
        # Run analysis
        self.analytics['conversation_volume'] = self.analyze_conversation_volume()
        self.analytics['client_behavior'] = self.analyze_client_behavior()
        self.analytics['message_patterns'] = self.analyze_message_patterns()
        self.analytics['sales_funnel'] = self.analyze_sales_funnel()
        self.analytics['response_time'] = self.analyze_response_time()
        self.analytics['objections'] = self.identify_objections()
        self.analytics['customer_mood'] = self.analyze_customer_mood()
        self.analytics['insights'] = self.generate_insights()
        
        # Summary
        self.analytics['summary'] = {
            'period_days': days,
            'generated_at': datetime.utcnow().isoformat(),
            'total_conversations': len(self.conversations),
            'total_clients': len(self.clients),
            'total_messages': len(self.messages),
            'data_quality': 'good' if len(self.conversations) > 10 else 'limited'
        }
        
        return self.analytics
    
    def print_report(self):
        """Imprime relatório formatado"""
        logger.info("\n")
        logger.info("╔══════════════════════════════════════════════════════════════╗")
        logger.info("║  🌙 LUNA OS — WHATSAPP SALES INTELLIGENCE REPORT            ║")
        logger.info("╚════════════════════════════════════════════════════════════╝")
        logger.info()
        
        # Summary
        summary = self.analytics.get('summary', {})
        logger.info(f"📅 Período: {summary.get('period_days', 0)} dias")
        logger.info(f"🕐 Gerado em: {summary.get('generated_at', 'N/A')}")
        logger.info(f"📊 Qualidade dos Dados: {summary.get('data_quality', 'unknown').upper()}")
        logger.info()
        
        logger.info("─" * 60)
        logger.info("📈 VOLUME DE CONVERSAS")
        logger.info("─" * 60)
        vol = self.analytics.get('conversation_volume', {})
        logger.info(f"Total: {vol.get('total_conversations', 0)}")
        logger.info(f"Média/dia: {vol.get('avg_per_day', 0):.1f}")
        logger.info(f"\nPor Status:")
        for status, count in vol.get('by_status', {}).items():
            logger.info(f"  • {status}: {count}")
        logger.info(f"\nPor Intent:")
        for intent, count in vol.get('by_intent', {}).items():
            logger.info(f"  • {intent}: {count}")
        logger.info(f"\nPor Sentimento:")
        for sentiment, count in vol.get('by_sentiment', {}).items():
            logger.info(f"  • {sentiment}: {count}")
        logger.info()
        
        logger.info("─" * 60)
        logger.info("🎯 FUNIL DE VENDAS")
        logger.info("─" * 60)
        funnel = self.analytics.get('sales_funnel', {})
        logger.info(f"Total Leads: {funnel.get('total_leads', 0)}")
        logger.info(f"Alta Intenção: {funnel.get('high_intent')} ({funnel.get('high_intent_rate', 0):.1f}%)")
        logger.info(f"Média Intenção: {funnel.get('medium_intent')} ({funnel.get('medium_intent_rate', 0):.1f}%)")
        logger.info(f"Baixa Intenção: {funnel.get('low_intent')} ({funnel.get('low_intent_rate', 0):.1f}%)")
        logger.info(f"\n✅ Conversões: {funnel.get('converted')} ({funnel.get('conversion_rate', 0):.1f}%)")
        logger.info()
        
        logger.info("─" * 60)
        logger.info("👥 COMPORTAMENTO DOS CLIENTES")
        logger.info("─" * 60)
        clients = self.analytics.get('client_behavior', {})
        logger.info(f"Total Clientes: {clients.get('total_clients', 0)}")
        logger.info(f"Clientes com Tags: {clients.get('tagged_clients', 0)}")
        logger.info(f"Clientes Recorrentes: {clients.get('returning_clients')} ({clients.get('returning_rate', 0):.1f}%)")
        logger.info(f"\nTop Tags:")
        for tag, count in clients.get('top_tags', []):
            logger.info(f"  • #{tag}: {count}")
        logger.info()
        
        logger.info("─" * 60)
        logger.info("💬 PADRÕES DE MENSAGENS")
        logger.info("─" * 60)
        msgs = self.analytics.get('message_patterns', {})
        logger.info(f"Total Mensagens: {msgs.get('total_messages', 0)}")
        logger.info(f"Média/Cliente: {msgs.get('avg_messages_per_client', 0):.1f}")
        logger.info(f"\nPor Direção:")
        for direction, count in msgs.get('by_direction', {}).items():
            logger.info(f"  • {direction}: {count}")
        logger.info(f"\nPor Horário:")
        for hour, count in msgs.get('by_hour', {}).items():
            logger.info(f"  • {hour}h: {count}")
        logger.info()
        
        logger.info("─" * 60)
        logger.info("⚠️  OBJEÇÕES")
        logger.info("─" * 60)
        obj = self.analytics.get('objections', {})
        logger.info(f"Total Objeções: {obj.get('total_objections', 0)}")
        logger.info(f"Taxa: {obj.get('objection_rate', 0):.1f}%")
        logger.info(f"\nTop Objeções:")
        for objection, count in obj.get('top_objections', []):
            logger.info(f"  • {objection}: {count}")
        logger.info()
        
        logger.info("─" * 60)
        logger.info("😊 HUMOR DOS CLIENTES")
        logger.info("─" * 60)
        mood = self.analytics.get('customer_mood', {})
        logger.info(f"Urgência Média: {mood.get('avg_urgency', 0):.1f}/5")
        logger.info(f"\nDistribuição de Humor:")
        for mood_type, count in mood.get('mood_distribution', {}).items():
            logger.info(f"  • {mood_type}: {count}")
        logger.info()
        
        logger.info("─" * 60)
        logger.info("💡 INSIGHTS ACIONÁVEIS")
        logger.info("─" * 60)
        insights = self.analytics.get('insights', [])
        if not insights:
            logger.info("Nenhum insight crítico no momento.")
        else:
            for i, insight in enumerate(insights, 1):
                icon = "🔴" if insight.get('type') == 'critical' else "🟡"
                logger.info(f"\n{icon} {i}. {insight.get('title')}")
                logger.info(f"   {insight.get('description')}")
                logger.info(f"   💡 {insight.get('recommendation')}")
        logger.info()
        
        logger.info("╔══════════════════════════════════════════════════════════════╗")
        logger.info("║  🏆 FIM DO RELATÓRIO                                         ║")
        logger.info("╚════════════════════════════════════════════════════════════╝")
        logger.info()


def main():
    """Main function"""
    analyst = WhatsAppSalesAnalyst()
    
    # Generate report (last 30 days by default)
    days = 30
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError as e:
            # [DEBT #A9] Manter fallback mas logar erro específico
            logger.debug(f"Argumento inválido, usando default 30 dias: {e}")
            days = 30
    
    report = analyst.generate_report(days=days)
    analyst.print_report()
    
    # Save to file
    output_path = Path(__file__).parent / "logs" / f"sales_intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"💾 Relatório salvo em: {output_path}")
    logger.info(f"📁 Relatório completo salvo em: {output_path}")


if __name__ == "__main__":
    main()
