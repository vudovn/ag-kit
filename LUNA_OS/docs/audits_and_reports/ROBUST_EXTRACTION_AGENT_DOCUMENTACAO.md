# 🌙🤖 ROBUST EXTRACTION AGENT

## Agente Python Especialista em Extração de Dados

**Data:** 27 de Fevereiro de 2026  
**Status:** ✅ **IMPLEMENTADO**  
**Foco:** **EXTRAÇÃO ROBUSTA + PROFISSIONAL**

---

## 🎯 ARQUITETURA DO AGENTE

### **Classe Base: RobustExtractionAgent**

**Features:**
```
✅ Batch Extraction (10K rows por batch)
✅ Resume Capability (checkpoint saving)
✅ Error Recovery (retry com backoff)
✅ Progress Tracking (tempo real)
✅ Data Validation (integrity checks)
✅ Multiple Formats (JSON, CSV, Parquet)
✅ Checkpoint Saving (resume after failure)
✅ Parallel Extraction (multi-worker)
```

---

### **Classe Especializada: WhatsAppExtractionSpecialist**

**Features:**
```
✅ Extração de whatsapp_messages_history
✅ Agrupamento automático por phone
✅ Ordenação cronológica
✅ Cálculo de estatísticas por conversa
✅ Detecção de threads longos
✅ Output em JSON estruturado
```

---

## 🚀 COMO USAR

### **Uso Básico:**

```python
from robust_extraction_agent import WhatsAppExtractionSpecialist

# Create specialist
specialist = WhatsAppExtractionSpecialist(
    output_dir="/Users/franciscotaveira.ads/LUNA OS/logs/extractions"
)

# Extract
result = await specialist.extract_complete_conversations()
```

### **Uso Avançado:**

```python
from robust_extraction_agent import RobustExtractionAgent, ExtractionConfig

# Config
config = ExtractionConfig(
    table="clients",
    output_dir="/path/to/output",
    batch_size=5000,
    max_workers=3,
    max_retries=5,
    retry_delay=10,
    timeout_seconds=600,
    compress=True,
    format="json",
    validate=True,
    resume=True
)

# Create agent
agent = RobustExtractionAgent(config)

# Extract
result = await agent.extract_table()
```

---

## 📊 COMANDOS DE LINHA

### **Extrair Conversas WhatsApp:**
```bash
cd "/Users/franciscotaveira.ads/LUNA OS/backend"
python3 app/scripts/robust_extraction_agent.py
```

**Isso vai:**
1. ✅ Extrair TODAS as mensagens do whatsapp_messages_history
2. ✅ Agrupar por phone (threads)
3. ✅ Ordenar cronologicamente
4. ✅ Calcular estatísticas
5. ✅ Salvar em JSON estruturado
6. ✅ Validar dados
7. ✅ Criar checkpoints

**Tempo:** 5-15 minutos (dependendo do volume)

---

## 📁 OUTPUT ESPERADO

### **Arquivo JSON:**
```
logs/extractions/whatsapp_conversations_20260227_072400.json
```

### **Estrutura:**
```json
{
  "metadata": {
    "extracted_at": "20260227_072400",
    "total_conversations": 2500,
    "total_messages": 35000,
    "stats": {
      "conversations_with_10_plus": 800,
      "conversations_with_50_plus": 200,
      "conversations_with_100_plus": 50
    }
  },
  "conversations": [
    {
      "phone": "5549999999999",
      "total_messages": 156,
      "inbound_count": 78,
      "outbound_count": 78,
      "duration_minutes": 145.5,
      "first_message": "2026-02-20T14:30:00Z",
      "last_message": "2026-02-20T16:55:00Z",
      "first_content": "Oi, tem horário para amanhã?",
      "last_content": "Perfeito! Te vejo amanhã às 15h."
    }
    // ... mais 2.499 conversas
  ]
}
```

---

## 📊 ESTATÍSTICAS ESPERADAS

### **Cenário Realista:**
```
📊 TOTAL CONVERSAS: 1.500-3.000
📊 TOTAL MENSAGENS: 25.000-40.000

📈 CONVERSAS POR TAMANHO:
   • 10+ mensagens: 500-1.000
   • 50+ mensagens: 100-300
   • 100+ mensagens: 20-100
```

### **O Que Isso Significa:**
```
✅ 25.000-40.000 mensagens REAIS extraídas
✅ 1.500-3.000 threads COMPLETOS
✅ 500-1.000 threads com 10+ mensagens
✅ 100-300 threads com 50+ mensagens
✅ 20-100 threads com 100+ mensagens
```

---

## 🔧 CONFIGURAÇÕES DISPONÍVEIS

### **ExtractionConfig:**

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| `table` | str | - | Tabela para extrair |
| `output_dir` | str | - | Diretório de output |
| `batch_size` | int | 10000 | Rows por batch |
| `max_workers` | int | 3 | Workers paralelos |
| `max_retries` | int | 3 | Retries por erro |
| `retry_delay` | int | 5 | Delay entre retries |
| `timeout_seconds` | int | 300 | Timeout da extração |
| `compress` | bool | True | Comprimir output |
| `format` | str | "json" | Formato (json/csv/parquet) |
| `validate` | bool | True | Validar dados |
| `resume` | bool | True | Resume após falha |

---

## 🛡️ RECURSOS DE SEGURANÇA

### **1. Checkpoint Saving:**
```python
# Salva checkpoint a cada batch
# Permite resume após falha
# Evita re-extrair dados já extraídos
```

### **2. Error Recovery:**
```python
# Retry automático com backoff exponencial
# max_retries=5
# retry_delay=10 (segundos)
# Backoff: 10s, 20s, 40s, 80s, 160s
```

### **3. Data Validation:**
```python
# Check row count
# Check duplicates
# Check null columns
# Check date ranges
# Check data integrity
```

### **4. Rate Limiting:**
```python
# Delay entre batches (0.5s)
# Evita sobrecarregar Supabase
# Previne rate limiting
```

---

## 📊 MONITORAMENTO

### **Logs em Tempo Real:**
```
2026-02-27 07:24:00.000 | INFO | 📥 Starting extraction of whatsapp_messages_history...
2026-02-27 07:24:01.000 | INFO |    📊 Total rows to extract: 35000
2026-02-27 07:24:02.000 | INFO |    📊 Progress: 10,000/35,000 (28.6%)
2026-02-27 07:24:03.000 | INFO |    📊 Progress: 20,000/35,000 (57.1%)
2026-02-27 07:24:04.000 | INFO |    📊 Progress: 30,000/35,000 (85.7%)
2026-02-27 07:24:05.000 | INFO |    ✅ Extraction completed: 35,000 rows in 245.3s
2026-02-27 07:24:06.000 | INFO | 💾 Data saved to: /path/to/output.json
```

### **Estatísticas:**
```python
{
  "total_rows": 35000,
  "total_bytes": 52428800,
  "batches_processed": 7,
  "errors": 0,
  "start_time": "2026-02-27T07:24:00.000Z",
  "end_time": "2026-02-27T07:28:05.000Z",
  "duration_seconds": 245.3,
  "rows_per_second": 142.7
}
```

---

## 🔍 VALIDAÇÃO DE DADOS

### **Checks Realizados:**

**1. Row Count:**
```python
# Verifica se extraiu >= 95% do esperado
if len(data) < expected_count * 0.95:
    issue("Row count mismatch")
```

**2. Duplicate Detection:**
```python
# Detecta IDs duplicados
duplicates = len(ids) - len(set(ids))
if duplicates > 0:
    issue(f"Duplicate IDs: {duplicates}")
```

**3. Null Columns:**
```python
# Detecta colunas com >50% nulls
high_null_columns = {k: v for k, v in null_counts.items() if v > len(data) * 0.5}
if high_null_columns:
    issue(f"Columns with >50% nulls: {high_null_columns}")
```

**4. Date Range:**
```python
# Verifica range de datas
min_date = min(dates)
max_date = max(dates)
logger.info(f"Date range: {min_date} to {max_date}")
```

---

## 💡 EXEMPLOS DE USO

### **Exemplo 1: Extrair Tabela Simples:**
```python
config = ExtractionConfig(
    table="clients",
    output_dir="/path/to/output"
)

agent = RobustExtractionAgent(config)
result = await agent.extract_table()
```

### **Exemplo 2: Extrair Múltiplas Tabelas:**
```python
tables = ["clients", "conversations", "whatsapp_messages_history"]

agent = RobustExtractionAgent(config)
result = await agent.extract_multiple_tables(tables)
```

### **Exemplo 3: Extrair com Resume:**
```python
config = ExtractionConfig(
    table="whatsapp_messages_history",
    output_dir="/path/to/output",
    resume=True  # Enable resume
)

agent = RobustExtractionAgent(config)
result = await agent.extract_table()

# Se falhar, rodar novamente resume do checkpoint
result = await agent.extract_table()  # Resume automatic
```

### **Exemplo 4: WhatsApp Specialist:**
```python
specialist = WhatsAppExtractionSpecialist(
    output_dir="/path/to/output"
)

result = await specialist.extract_complete_conversations()
```

---

## 📁 ARQUIVOS GERADOS

### **Output Files:**
```
logs/extractions/
├── whatsapp_conversations_20260227_072400.json    ← Conversas agrupadas
├── whatsapp_messages_history_20260227_072000.json ← Mensagens raw
├── clients_20260227_071500.json                   ← Clients
└── .checkpoint_whatsapp_messages_history.json     ← Checkpoint
```

### **Log Files:**
```
logs/
└── extraction_agent.log    ← Log completo da extração
```

---

## 🎯 PRÓXIMOS PASSOS

### **1. Executar Agente:**
```bash
python3 app/scripts/robust_extraction_agent.py
```

### **2. Verificar Output:**
```bash
ls -lh logs/extractions/
cat logs/extractions/whatsapp_conversations_*.json | jq '.metadata'
```

### **3. Analisar Dados:**
```bash
python3 app/scripts/analise_profunda_threads.py
```

### **4. Treinar Luna:**
```bash
# Usar conversas reais para melhorar respostas
# Atualizar knowledge base
# Refinar brain.py
```

---

## 📊 CHECKLIST DE VALIDAÇÃO

### **Depois de Executar:**
```
□ 1. ⏳ Arquivos foram criados?
□ 2. ⏳ JSON tem > 10MB?
□ 3. ⏳ Total mensagens > 10.000?
□ 4. ⏳ Total conversas > 500?
□ 5. ⏳ Conversas com 50+ msgs > 50?
□ 6. ⏳ Validação passou?
□ 7. ⏳ Checkpoint salvo?
```

### **Se TODOS ✅:**
```
✅ Extração BEM SUCEDIDA
✅ Dados SUFICIENTES
✅ Podemos analisar padrões
✅ Podemos treinar Luna
```

---

**🌙 "Inteligência completa. Complexidade invisível."**

**Status:** ✅ **ROBUST EXTRACTION AGENT IMPLEMENTADO**

**Próximo:** **`python3 app/scripts/robust_extraction_agent.py`**

**Benefício:** **EXTRAÇÃO PROFISSIONAL + ROBUSTA + VALIDADA**
