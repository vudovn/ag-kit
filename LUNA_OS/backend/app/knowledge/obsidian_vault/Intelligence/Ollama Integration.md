# 🦙 Ollama Integration - Documentação

**Status:** ✅ **Operacional**  
**Modelo:** llama3.2 (3.2B, Q4_K_M)  
**Hardware:** Apple M1 (Native)  
**API:** http://127.0.0.1:11434

---

## 📋 VISÃO GERAL

Integração do **Conversation Intelligence Module** com **Ollama Local** para geração de insights inteligentes sem consumir créditos de API.

---

## 🏗️ ARQUITETURA

```
┌─────────────────────────────────────────────────────────────┐
│                    LUNA OS - WhatsApp                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Conversation Intelligence Module                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Extractor   │  │ Psychology  │  │   Sales     │         │
│  │   Agent     │  │    Agent    │  │   Agent     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Behavior   │  │  Insights   │  │  Learning   │         │
│  │   Agent     │  │    Agent    │  │   Agent     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    OLLAMA LOCAL (M1)                         │
│  Model: llama3.2:latest (3.2B, ~2GB)                        │
│  Endpoint: http://127.0.0.1:11434/api/generate              │
│  Uso: Gerar resumos executivos e recomendações              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT                            │
│  📁 Intelligence/Ollama Insights/                           │
│  📁 Intelligence/Agent Analysis/                            │
│  📁 Intelligence/Psychology Profiles/                       │
│  📁 Intelligence/Sales Patterns/                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 INSTALAÇÃO

### 1. Instalar Ollama (macOS M1)

```bash
# Via site oficial (recomendado)
curl -fsSL https://ollama.com/install.sh | sh

# Ou via Homebrew
brew install ollama
```

### 2. Baixar Modelo

```bash
# Modelo leve para M1 (recomendado)
ollama pull llama3.2

# Alternativa: phi3 (ainda mais leve)
ollama pull phi3
```

### 3. Verificar Instalação

```bash
# Listar modelos instalados
ollama list

# Testar geração
ollama run llama3.2 "Olá, como vai?"
```

---

## 📖 USO

### Via API (Recomendado para Agentes)

```python
import httpx

async def ask_ollama(prompt: str, model: str = "llama3.2"):
    """Envia prompt para Ollama local"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60.0
        )
        return response.json()["response"]

# Exemplo de uso
insight = await ask_ollama("""
Analise esta conversa e gere insights:

Dados da Psicologia:
- Emoção: alegria
- DISC: Influente

Dados de Vendas:
- Funil: consideration
- Objeções: preço

Gere 3 recomendações acionáveis.
""")
```

### Via Python (Direto)

```python
import subprocess

def ask_ollama_cli(prompt: str):
    """Usa CLI do Ollama"""
    result = subprocess.run(
        ["ollama", "run", "llama3.2", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout
```

---

## 📁 ESTRUTURA DO OBSIDIAN

### Pastas Criadas

```
Intelligence/
├── Dashboard.md                    # Dashboard principal
├── Ollama Integration.md           # Esta documentação
├── Ollama Insights/                # Insights gerados pelo Ollama
│   └── Insight-{phone}-{date}.md
├── Agent Analysis/                 # Análises completas dos agentes
│   └── Analysis-{phone}-{date}.md
├── Psychology Profiles/            # Perfis psicológicos
│   └── Profile-{phone}.md
└── Sales Patterns/                 # Padrões de vendas
    └── Pattern-{period}.md
```

### Templates

**Templates criados em:** `Templates/Conversation Intelligence/`

1. **Ollama Insight Template.md**
   - Resumo executivo (Ollama)
   - Insights de psicologia, vendas, comportamento
   - Recomendações acionáveis

2. **Agent Analysis Template.md**
   - Dados de todos os 5 agentes
   - Métricas detalhadas
   - Links para perfis

3. **Psychology Profile Template.md**
   - Perfil DISC completo
   - Emoções predominantes
   - Gatilhos mentais

4. **Sales Pattern Template.md**
   - Métricas do período
   - Objeções mais comuns
   - Tendências identificadas

---

## 🔗 INTEGRAÇÃO COM AGENTES

### StorageAgent (Modificado)

```python
class StorageAgent:
    def _store_in_obsidian(self, context, results, ollama_insight=None):
        """Armazena no Obsidian com insight do Ollama"""
        
        # Template: Ollama Insight
        if ollama_insight:
            file_path = f"Intelligence/Ollama Insights/Insight-{context.phone}-{date}.md"
            content = self._generate_ollama_content(context, results, ollama_insight)
            self._write_obsidian_file(file_path, content)
        
        # Template: Agent Analysis
        file_path = f"Intelligence/Agent Analysis/Analysis-{context.phone}-{date}.md"
        content = self._generate_analysis_content(context, results)
        self._write_obsidian_file(file_path, content)
```

### InsightsAgent (Modificado)

```python
class InsightsAgent:
    async def analyze_with_ollama(self, context, agent_results):
        """Usa Ollama para gerar insights inteligentes"""
        
        # Compilar dados brutos dos agentes
        raw_data = self._compile_agent_data(agent_results)
        
        # Prompt para Ollama
        prompt = f"""
        Você é um especialista em análise de conversas de vendas.
        
        Analise os dados abaixo e gere insights acionáveis:
        
        {raw_data}
        
        Gere:
        1. Resumo executivo (2-3 frases)
        2. 3 insights principais
        3. 3 recomendações acionáveis
        4. Prioridade (0-100)
        """
        
        # Chamar Ollama local
        ollama_response = await self._ask_local_brain(prompt)
        
        return {
            "ollama_insight": ollama_response,
            "model": "llama3.2",
            "processing_time_ms": ollama_time,
        }
```

---

## 📊 EXEMPLO DE INSIGHT GERADO

### Arquivo: `Intelligence/Ollama Insights/Insight-5549991112233-20260301.md`

```markdown
---
type: ollama_insight
created_at: 2026-03-01 14:30
phone: 5549991112233
client_name: Maria Silva
ollama_model: llama3.2
processing_time_ms: 1250
confidence_score: 0.87
---

# 🧠 Insight Ollama: Maria Silva

## 📊 Resumo Executivo

Cliente demonstra alto interesse (emoção: alegria) com perfil Influente (DISC).
Está no estágio de consideração, com objeção de preço não resolvida.
Recomenda-se abordagem emocional com prova social e oferta de parcelamento.

## 💡 Recomendações Acionáveis

1. **Imediato:** Enviar depoimentos de clientes com perfil similar
2. **24h:** Oferecer parcelamento em 3x sem juros
3. **48h:** Follow-up com oferta de desconto para primeira vez (10%)

## 🎯 Prioridade: 82/100
```

---

## 🧪 TESTES

### Testar Ollama

```bash
# Testar API
curl http://127.0.0.1:11434/api/tags

# Testar geração
curl http://127.0.0.1:11434/api/generate \
  -d '{"model":"llama3.2","prompt":"Olá","stream":false}'
```

### Testar Integração

```bash
# Testar endpoint de análise
curl -X POST http://localhost:8000/api/conversation-intelligence/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test_123",
    "phone": "5549991112233",
    "messages": [
      {"direction": "inbound", "content": "Oi, quero agendar"},
      {"direction": "outbound", "content": "Oi! Qual dia?"}
    ]
  }'
```

---

## 📈 MÉTRICAS

| Métrica | Esperado | Observado |
|---------|----------|-----------|
| Tempo Geração Ollama | <2s | ~1-1.5s |
| Tamanho Modelo | ~2GB | 2.02GB |
| Uso de RAM | <4GB | ~3GB |
| Custos API | $0 | $0 ✅ |

---

## 🔧 CONFIGURAÇÃO

### Variáveis de Ambiente

```bash
# .env
OLLAMA_API_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=60
OBSIDIAN_VAULT_PATH=/path/to/obsidian_vault
```

### Configurar Agentes

```python
config = {
    "ollama": {
        "enabled": True,
        "api_url": "http://127.0.0.1:11434",
        "model": "llama3.2",
        "timeout": 60,
    },
    "obsidian": {
        "enabled": True,
        "vault_path": "/path/to/obsidian_vault",
        "templates_path": "Templates/Conversation Intelligence",
    },
}
```

---

## 🚨 TROUBLESHOOTING

### Ollama não responde

```bash
# Reiniciar daemon
ollama serve

# Verificar logs
tail -f ~/.ollama/logs/server.log
```

### Modelo não encontrado

```bash
# Listar modelos
ollama list

# Reinstalar
ollama rm llama3.2
ollama pull llama3.2
```

### Obsidian não atualiza

```bash
# Forçar sync do Dataview
# No Obsidian: Ctrl/Cmd + P → "Dataview: Force refresh"
```

---

## 🔗 LINKS RELACIONADOS

- [[000_MCT_MASTER_INDEX]]
- [[Dashboard]]
- [[Conversation Intelligence]]
- [[Templates]]

---

**Documentação criada:** 2026-03-01  
**Via:** Agent Flow  
**Status:** ✅ **Operacional**
