# 🌙 LUNA OS — Scripts de Analytics & Extração

**Localização:** `/Users/franciscotaveira.ads/LUNA OS/backend/app/scripts/`

**Dados salvos em:** `/Users/franciscotaveira.ads/LUNA OS/logs/`

---

## 📥 Scripts de Extração

### 1. `full_extraction.py` ⭐ RECOMENDADO
**Função:** Extrai TODAS as conversas individuais do Supabase (exclui grupos)

**Uso:**
```bash
cd "/Users/franciscotaveira.ads/LUNA OS/backend/app/scripts"
python3 full_extraction.py
```

**Saída:**
- `/Users/franciscotaveira.ads/LUNA OS/logs/extractions/whatsapp_conversations_YYYYMMDD_HHMMSS.json`
- `/Users/franciscotaveira.ads/LUNA OS/logs/extractions/top_conversations_YYYYMMDD_HHMMSS.txt`

**Configurações:**
- `batch_size = 1000` (limite da API)
- `offset = 184000` (continua de onde parou)
- Filtra: `is_group = false`

---

### 2. `extracao_direta_conversas.py`
**Função:** Extração direta com retry logic para erros 502/503

**Uso:**
```bash
python3 extracao_direta_conversas.py
```

**Configurações:**
- `batch_size = 5000`
- `max_batches = 200`
- Retry com backoff exponencial

---

## 📊 Scripts de Análise

### 1. `analyze_conversations.py` ⭐ PRINCIPAL
**Função:** Análise completa em 7 dimensões

**Métricas:**
1. 👑 Perfil de Clientes VIP (top 20)
2. ⏱️ Tempo de Resposta (média, mediana, distribuição)
3. ❓ FAQs Automáticas (detecção por patterns)
4. 📅 Horários e Dias (pico, distribuição)
5. 🎯 Jornada do Cliente (conversão por tamanho)
6. 🔑 Palavras-chave (serviços e ações)
7. 📊 Resumo Executivo

**Uso:**
```bash
python3 analyze_conversations.py
```

**Saída:**
- `/Users/franciscotaveira.ads/LUNA OS/logs/analytics/vip_clients.json`
- `/Users/franciscotaveira.ads/LUNA OS/logs/analytics/faq_detection.json`
- `/Users/franciscotaveira.ads/LUNA OS/logs/analytics/complete_analytics_report.json`

---

### 2. `deep_faq_analysis.py` ⭐ COMPLEMENTAR
**Função:** Análise profunda de conteúdo e sentimento

**Métricas:**
- 🔍 N-grams (palavras e frases mais comuns)
- 🎯 Intenções (agendamento, preço, serviço, etc.)
- 😊 Sentimento (positivo, negativo, neutro)
- 📋 Exemplos de mensagens

**Uso:**
```bash
python3 deep_faq_analysis.py
```

**Saída:**
- `/Users/franciscotaveira.ads/LUNA OS/logs/analytics/deep_faq_sentiment_analysis.json`

---

## 📄 Relatório Consolidado

### `RELATORIO_COMPLETO.md`
**Local:** `/Users/franciscotaveira.ads/LUNA OS/logs/analytics/`

**Conteúdo:**
- Resumo executivo
- Top 10 clientes VIP
- Tempo de resposta
- Intenções detectadas
- Padrões temporais
- Sentimento
- Recomendações prioritárias

**Visualizar:**
```bash
cat "/Users/franciscotaveira.ads/LUNA OS/logs/analytics/RELATORIO_COMPLETO.md"
```

---

## 🚀 Fluxo Recomendado

### Extração Completa (nova)
```bash
# 1. Extrair dados
python3 full_extraction.py

# 2. Analisar dados
python3 analyze_conversations.py

# 3. Análise profunda (opcional)
python3 deep_faq_analysis.py

# 4. Ver relatório
cat "/Users/franciscotaveira.ads/LUNA OS/logs/analytics/RELATORIO_COMPLETO.md"
```

### Re-análise (dados já extraídos)
```bash
# Apenas analisar
python3 analyze_conversations.py
python3 deep_faq_analysis.py
```

---

## 📁 Estrutura de Pastas

```
/Users/franciscotaveira.ads/LUNA OS/
├── backend/app/scripts/
│   ├── full_extraction.py          # Extração completa
│   ├── extracao_direta_conversas.py # Extração alternativa
│   ├── analyze_conversations.py     # Análise principal
│   └── deep_faq_analysis.py         # Análise profunda
│   └── README_ANALYTICS.md         # Esta documentação
└── logs/
    ├── extractions/
    │   └── whatsapp_conversations_*.json
    └── analytics/
        ├── RELATORIO_COMPLETO.md
        ├── complete_analytics_report.json
        ├── vip_clients.json
        ├── faq_detection.json
        └── deep_faq_sentiment_analysis.json
```

---

## 🔧 Configurações

Todos os scripts usam:
- **Supabase URL:** `https://sktrmwogifeuzrcnpvsw.supabase.co`
- **ENV:** `/Users/franciscotaveira.ads/LUNA OS/.env`
- **Tabela:** `whatsapp_messages_history`
- **Filtro:** `is_group = false` (apenas conversas individuais)

---

## 📊 Últimos Dados

- **Total Mensagens:** 211,517
- **Total Conversas:** 110
- **Clientes VIP:** 81 (100+ msgs)
- **Período:** Fevereiro 2026

---

**🌙 LUNA OS Analytics Suite**
