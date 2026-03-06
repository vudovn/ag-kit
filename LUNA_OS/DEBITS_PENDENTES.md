# 🔍 Débitos Técnicos Pendentes - LUNA OS v3.0

**Data da Análise:** 2026-03-03  
**Total Identificado:** 72 débitos  
**Status:** Pendentes de resolução

---

## 📊 Resumo por Severidade

| Severidade | Quantidade | Prioridade | Prazo Sugerido |
|------------|------------|------------|----------------|
| **Crítica** | 2 | Imediata | 24-48h |
| **Alta** | 24 | Alta | 1-2 sprints |
| **Média** | 28 | Média | 2-4 sprints |
| **Baixa** | 18 | Baixa | Backlog |

---

## 🚨 Débitos Críticos (Resolução Imediata)

### #C1 - Caminhos Hardcoded em Módulos de Produção
**Arquivos:**
- `backend/app/modules_v3/agenda_viva/optimizer.py` (linha 17)
- `backend/app/modules_v3/revenue_optimizer/optimizer.py` (linha 15)

**Problema:**
```python
LOGS_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs")
```

**Risco:** Código não funciona em outros ambientes (produção, outros devs)

**Solução:**
```python
LOGS_DIR = Path(os.getenv("LOGS_DIR", "logs"))
```

**Arquivo:** `backend/app/modules_v3/agenda_viva/optimizer.py`

---

### #C2 - Variáveis de Ambiente Críticas sem Validação
**Arquivo:** `backend/app/config.py`

**Problema:** Validação existe mas não cobre:
- `REDIS_URL`
- `MILVUS_HOST`
- `JAEGER_AGENT_HOST`
- `NTFY_TOPIC`

**Risco:** Sistema inicia em estado degradado sem alerta

**Solução:** Adicionar validação no `validate_critical_keys()`:
```python
if not self.redis_v3_url:
    warnings.append("REDIS_URL não configurada - filas desabilitadas")
```

---

## 🔴 Débitos Altos (1-2 Sprints)

### #A1 - Tratamento de Erro Genérico (`except:`)
**Arquivos:**
- `backend/app/api/health.py` (linhas 43, 122, 137, 172)
- `backend/app/modules_v3/integration_endpoint.py` (linhas 122, 188, 194)
- `backend/app/core/intelligence.py` (linha 153)
- `backend/app/core/memory.py` (linha 587)

**Problema:**
```python
except:
    # Erro não logado, não tratado
```

**Solução:**
```python
except Exception as e:
    logger.error(f"Erro específico: {e}")
    raise
```

---

### #A2 - Classes Muito Grandes (>200 linhas)
**Arquivos:**
| Classe | Linhas | Severidade |
|--------|--------|------------|
| `BrainEngine` (`brain.py`) | ~300 | Alta |
| `MemoryManager` (`memory.py`) | ~400 | Alta |
| `EvolutionEngine` (`evolution.py`) | ~350 | Média |
| `AgendaViva` (`agenda_viva/optimizer.py`) | ~380 | Média |

**Solução:** Dividir por responsabilidade:
```python
# BrainEngine → 3 classes
class IntentClassifier
class ContextBuilder
class ResponseGenerator
```

---

### #A3 - Funções Muito Longas (>50 linhas)
**Arquivos:**
| Função | Linhas | Arquivo |
|--------|--------|---------|
| `BrainEngine.process_message` | ~100 | `brain.py` |
| `BrainEngine._process_with_ai` | ~150 | `brain.py` |
| `handle_message` | ~100 | `webhooks.py` |
| `TaskRunner._process_ended_conversations` | ~100 | `task_runner.py` |

**Solução:** Extrair sub-pipelines:
```python
def _classify_intent(self, ...)
def _build_context(self, ...)
def _generate_response(self, ...)
```

---

### #A4 - Async/Sync Mixing Incorreto
**Arquivos:**
- `backend/app/core/task_runner.py` (linhas 56-62)
- `backend/app/webhooks.py` (linhas 230-330)

**Problema:**
```python
# Thread síncrona chamando asyncio.run()
asyncio.run(task_func())  # Pode vazar event loop
```

**Solução:**
```python
# Usar event loop compartilhado
loop = asyncio.get_event_loop()
loop.run_until_complete(task_func())
```

---

### #A5 - Validação de Input em Endpoints
**Arquivos:**
- `backend/app/api/knowledge.py` (linhas 71-85)
- `backend/app/api/campaigns.py` (linhas 33-55)
- `backend/app/api/dojo_learning.py` (linhas 91-120)

**Problema:**
```python
# Sem validação de datas
create_campaign(start_date, end_date)  # start > end?
```

**Solução:**
```python
class CampaignCreate(BaseModel):
    start_date: datetime
    end_date: datetime
    
    @validator('end_date')
    def validate_dates(cls, end, values):
        if end <= values['start_date']:
            raise ValueError('end_date deve ser após start_date')
        return end
```

---

### #A6 - Endpoints Sem Rate Limiting
**Arquivos:**
- `backend/app/api/sovereign_switch.py` (linhas 56-100)
- `backend/app/api/dojo_learning.py` (linhas 91-230)

**Problema:** Endpoints críticos sem proteção

**Solução:**
```python
@router.post("/switch")
@limiter.limit("10/minute")  # Restritivo para config
async def sovereign_switch(request: Request):
```

---

### #A7 - Testes Unitários Faltando (Módulos Críticos)
**Módulos sem testes:**
| Módulo | Criticidade | Arquivo de Teste Sugerido |
|--------|-------------|---------------------------|
| `guardrails.py` | Crítica | `test_guardrails.py` (parcial existe) |
| `learning.py` | Crítica | `test_learning.py` |
| `alert_system.py` | Alta | `test_alert_system.py` |
| `queue_manager.py` | Alta | `test_queue_manager.py` |
| `vector_db_manager.py` | Alta | `test_vector_db.py` |
| `churn_prediction.py` | Alta | `test_churn.py` (parcial existe) |

---

### #A8 - Acoplamento Excessivo
**Arquivo:** `backend/app/core/brain.py`

**Problema:** `BrainEngine` depende diretamente de:
- `memory`
- `kb` (KnowledgeBase)
- `campaign_manager`
- `openrouter`
- `scheduler`
- `guardrails`
- `learning`

**Solução:** Injeção de dependência:
```python
class BrainEngine:
    def __init__(
        self,
        memory: MemoryManager,
        knowledge: KnowledgeBase,
        campaign_mgr: CampaignManager,
        llm_client: LLMClient,
        # ...
    ):
        self.memory = memory
        self.knowledge = knowledge
        # ...
```

---

## 🟡 Débitos Médios (2-4 Sprints)

### #M1 - Código Duplicado
**Arquivos:**
- `backend/app/api/settings.py` (linhas 70-95)
- `backend/app/api/sovereign_switch.py` (linhas 56-90)

**Problema:** Lógica duplicada de persistência no `.env`

**Solução:**
```python
# app/utils/env_persister.py
def update_env_file(key: str, value: str):
    # Lógica centralizada
```

---

### #M2 - Logs Inconsistentes (print vs logger)
**Arquivos:**
- `backend/app/knowledge/loader.py` (linhas 18, 28)
- `backend/app/api/settings.py` (linhas 48, 107)

**Problema:**
```python
print(f"✅ Knowledge Base loaded...")  # ❌
logger.info("Knowledge Base loaded...")  # ✅
```

---

### #M3 - Type Hints Faltando
**Arquivos:**
- `backend/app/core/brain.py` - `classify_intent()`
- `backend/app/core/intelligence.py` - `extract_fields()`
- `backend/app/api/health.py` - `get_health_status()`

**Solução:**
```python
def classify_intent(message: str) -> Tuple[IntentType, float]:
```

---

### #M4 - Docstrings Faltando
**Arquivos:**
- `backend/app/modules_v3/feature_flags.py` (linhas 46-78)
- `backend/app/core/physics.py` (linhas 59-79)

**Solução:**
```python
def is_module_enabled(module_name: str) -> bool:
    """
    Verifica se módulo está habilitado via feature flag.
    
    Args:
        module_name: Nome do módulo
        
    Returns:
        True se habilitado, False caso contrário
    """
```

---

### #M5 - Hardcoded Values (Model IDs)
**Arquivo:** `backend/app/core/brain.py` (linhas 551, 602)

**Problema:**
```python
logic_model = os.getenv("LOGIC_MODEL_ID", "google/gemini-2.5-flash")
```

**Solução:** Mover para `config.py`:
```python
# config.py
model_logic: str = "google/gemini-2.5-flash"
model_voice: str = "anthropic/claude-3.5-sonnet"

# brain.py
from app.config import settings
logic_model = settings.model_logic
```

---

### #M6 - Imports Desorganizados
**Arquivos:**
- `backend/app/core/brain.py` (linhas 63-68)
- `backend/app/api/webhooks.py` (linhas 338-339)

**Problema:** Imports no meio do arquivo ou duplicados

**Solução:** Seguir ordem:
1. Standard library
2. Third-party
3. Local imports

---

### #M7 - Versões Inconsistentes
**Arquivos:**
- `backend/app/main.py` (linha 208): "v2.1"
- `backend/app/api/health.py` (linha 25): "2.0.0"
- `backend/app/main.py` (linha 180): "3.0.0"

**Solução:** Usar `settings.app_version` em todos os lugares:
```python
from app.config import settings
version=settings.app_version
```

---

### #M8 - Dependência de Plotly Não Usada
**Arquivo:** `backend/requirements.txt`

**Problema:** `plotly==5.18.0` não é importado em nenhum lugar

**Solução:** Remover ou mover para `requirements-dev.txt`

---

## 🟢 Débitos Baixos (Backlog)

### #B1 - Comentários Misturados (PT/EN)
**Arquivos:**
- `backend/app/main.py` (linhas 45-70)
- `backend/app/core/rate_limit.py` (todo)
- `backend/app/schemas.py` (linha 1)

**Solução:** Padronizar para PT-BR (público alvo) ou EN (padrão técnico)

---

### #B2 - Variável Global Não Utilizada
**Arquivo:** `backend/app/core/campaign_manager.py` (linhas 13-15)

**Problema:**
```python
campaign_manager = None  # Nunca instanciado
```

**Solução:** Instanciar ou remover

---

### #B3 - Import Comentado
**Arquivo:** `backend/app/main.py` (linhas 173-174)

**Problema:**
```python
# app.include_router(campaigns.router, ...)
```

**Solução:** Remover se não for usar

---

### #B4 - Fallback Hardcoded em Config
**Arquivo:** `backend/app/main.py` (linha 163)

**Problema:**
```python
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000")
```

**Solução:** Mover para `config.py`

---

### #B5 - Task em Background Sem Tratamento
**Arquivo:** `backend/app/core/brain.py` (linha 593)

**Problema:**
```python
asyncio.create_task(wascript.add_client_note(...))  # Erros silenciosos
```

**Solução:**
```python
task = asyncio.create_task(wascript.add_client_note(...))
task.add_done_callback(handle_task_error)
```

---

### #B6 - Scripts com Print
**Arquivos:**
- `backend/app/modules_v3/test_integration.py`
- `backend/app/scripts/auditoria_banco_dados.py`

**Solução:** Substituir por logger (baixa prioridade - scripts internos)

---

### #B7 - SQL Queries Raw em Scripts
**Arquivo:** `backend/app/scripts/auditoria_banco_dados.py`

**Solução:** Usar cliente Supabase (baixa prioridade - scripts internos)

---

### #B8 - Dependências de File Processing
**Arquivo:** `backend/requirements.txt`

**Problema:** `openpyxl`, `python-docx`, `PyPDF2` usados apenas em scripts

**Solução:** Mover para `requirements-dev.txt`

---

## 📋 Plano de Ação Sugerido

### Sprint 1 (Semana 1-2) - Críticos + Altos
- [ ] #C1 - Remover caminhos hardcoded
- [ ] #C2 - Validar ENV críticas
- [ ] #A1 - Corrigir `except:` genéricos
- [ ] #A5 - Validação de inputs
- [ ] #A6 - Rate limiting em endpoints críticos

### Sprint 2 (Semana 3-4) - Altos
- [ ] #A4 - Corrigir async/sync mixing
- [ ] #A7 - Criar testes unitários (guardrails, learning, alerts)
- [ ] #A3 - Dividir funções longas (brain.py)

### Sprint 3 (Semana 5-6) - Altos/Médios
- [ ] #A2 - Dividir classes grandes (BrainEngine, MemoryManager)
- [ ] #A8 - Injeção de dependência no Brain
- [ ] #M1 - Extrair código duplicado

### Sprint 4 (Semana 7-8) - Médios
- [ ] #M2 - Padronizar logs (remover prints)
- [ ] #M3 - Adicionar type hints
- [ ] #M4 - Adicionar docstrings
- [ ] #M5 - Mover hardcoded values para config

### Sprint 5 (Semana 9-10) - Médios/Baixos
- [ ] #M6 - Organizar imports
- [ ] #M7 - Padronizar versões
- [ ] #M8 - Limpar dependências não usadas
- [ ] #B1 - Padronizar comentários

### Backlog - Baixos
- [ ] #B2 - Remover variável global não usada
- [ ] #B3 - Remover imports comentados
- [ ] #B4 - Mover fallbacks para config
- [ ] #B5 - Tratamento de tasks em background
- [ ] #B6-B8 - Scripts e dependências

---

## 🎯 Métricas de Sucesso

| Métrica | Atual | Target (10 sprints) |
|---------|-------|---------------------|
| Débitos Críticos | 2 | 0 |
| Débitos Altos | 24 | ≤3 |
| Débitos Médios | 28 | ≤10 |
| Cobertura de Testes | ~15% | ≥70% |
| Funções >50 linhas | 5 | 0 |
| Classes >200 linhas | 4 | 0 |
| `except:` genéricos | 8 | 0 |
| Caminhos hardcoded | 2 | 0 |

---

## 📝 Notas

1. **Débitos #14 e #15** (comentários PT/EN e imports duplicados) foram parcialmente resolvidos nas correções anteriores, mas persistem em alguns arquivos.

2. **Débitos de testes** são críticos - módulos como `guardrails.py` e `learning.py` são o core do sistema e não têm cobertura adequada.

3. **Acoplamento do BrainEngine** é o débito arquitetural mais significativo - refatoração requer cuidado para não quebrar funcionalidade existente.

4. **Caminhos hardcoded** são bloqueantes para deploy em produção - devem ser resolvidos em 24-48h.

---

**Próxima Revisão:** 2026-03-17 (2 semanas)  
**Responsável:** Tech Lead  
**Status:** Aberto para atribuição
