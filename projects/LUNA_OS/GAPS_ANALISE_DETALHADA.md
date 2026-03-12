# 🔍 Análise Detalhada dos Gaps Pendentes - LUNA OS v3.0

**Data:** 2026-03-11  
**Autor:** LUNA OS Architecture Analysis  
**Nível:** Deep Dive Técnico

---

## 📋 ÍNDICE

1. [Gap Crítico #1: Belasis Mock Ativo](#gap-crítico-1-belasis-mock-ativo)
2. [Gap #2: Tabelas Redundantes de Campanhas](#gap-2-tabelas-redundantes-de-campanhas)
3. [Gap #3: Documentação do Endpoint Analytics](#gap-3-documentação-do-endpoint-analytics)
4. [Gap #4: Configuração Milvus](#gap-4-configuração-milvus)
5. [Gap #5: Endpoint de Histórico WhatsApp](#gap-5-endpoint-de-histórico-whatsapp)
6. [Gap #6: Components de Domínio no Frontend](#gap-6-components-de-domínio-no-frontend)
7. [Gaps Não Identificados Explicitamente](#gaps-não-identificados-explicitamente)

---

# Gap Crítico #1: Belasis Mock Ativo

## 📍 Descrição Detalhada

O sistema LUNA OS integra com o **Belasis ERP** para sincronizar:
- Profissionais do salão
- Serviços e preços
- Agenda e horários disponíveis
- Pedidos e histórico de clientes

Atualmente, o arquivo `.env` está configurado com:
```env
BELASIS_MOCK=true
BELASIS_API_KEY=
```

Isso ativa o **modo mock** no cliente Belasis, que retorna dados fictícios hardcoded.

## 🔬 Análise Técnica

### Código Envolvido

**Arquivo:** `backend/app/integrations/belasis.py`

```python
_MOCK_EMPLOYEES = [
    {"id": 1, "name": "Ju", "active": True},
    {"id": 2, "name": "Dávila", "active": True},
    {"id": 3, "name": "Lu", "active": True},
    {"id": 4, "name": "Carla", "active": True},
]

_MOCK_SERVICES = [
    {"id": 1, "description": "Escova Lisa", "price_cents": 5900, "duration": 45, "active": True},
    {"id": 2, "description": "Escova Modelada", "price_cents": 7900, "duration": 60, "active": True},
    # ... mais 5 serviços
]

class BelasisClient:
    def __init__(self):
        self.mock = settings.belasis_mock  # Lê BELASIS_MOCK do .env
    
    async def list_employees(self, active: bool = True, page: int = 1, limit: int = 100) -> list[dict]:
        """GET /employees"""
        if self.mock:
            logger.debug("🛡️ Belasis MOCK: employees")
            return _MOCK_EMPLOYEES  # ← Retorna dados FICTÍCIOS
        # Código real nunca é executado
        result = await self._get("/employees", {...})
        return result.get("data", [])
```

### Fluxo Atual (Mock)

```
┌──────────────┐
│  Frontend    │
│  /professionals
└──────┬───────┘
       │ GET /api/belasis/professionals
       ▼
┌──────────────┐
│  Backend     │
│  belasis_sync.py
└──────┬───────┘
       │ list_employees()
       ▼
┌──────────────┐
│  Belasis     │
│  Client      │
└──────┬───────┘
       │ if self.mock: return _MOCK_EMPLOYEES
       ▼
┌──────────────┐
│  DADOS       │
│  FICTÍCIOS   │  ← PROBLEMA!
│  (4 items)   │
└──────────────┘
```

### Fluxo Esperado (Real)

```
┌──────────────┐
│  Frontend    │
│  /professionals
└──────┬───────┘
       │ GET /api/belasis/professionals
       ▼
┌──────────────┐
│  Backend     │
│  belasis_sync.py
└──────┬───────┘
       │ list_employees()
       ▼
┌──────────────┐
│  Belasis     │
│  Client      │
└──────┬───────┘
       │ if self.mock: False
       │ await self._get("/employees")
       ▼
┌──────────────┐
│  Belasis     │
│  API Real    │
│  (HTTPS)     │
└──────┬───────┘
       │ GET https://api.belasis.com.br/api/v1/employees
       │ Header: ACCESS-TOKEN: bpk_***
       ▼
┌──────────────┐
│  DADOS       │
│  REAIS       │  ← CORRETO!
│  (9+ items)  │
└──────────────┘
```

## 💥 Impacto e Consequências

### Impacto Operacional

| Área | Impacto Atual | Impacto Esperado |
|------|---------------|------------------|
| **Profissionais** | 4 fictícios | 9+ reais do salão |
| **Serviços** | 7 fictícios | 40+ serviços reais |
| **Agenda** | Mock genérico | Agenda real do Belasis |
| **Preços** | Mockados | Preços reais do ERP |
| **Horários** | Mockados | Disponibilidade real |

### Impacto no Negócio

1. **Atendimento ao Cliente:**
   - ❌ Cliente vê profissionais que não existem
   - ❌ Preços podem estar errados
   - ❌ Horários disponíveis são fictícios
   - ❌ Serviços podem não corresponder à realidade

2. **Gestão do Salão:**
   - ❌ Impossível agendar horários reais
   - ❌ Impossível sincronizar com Belasis
   - ❌ Relatórios não refletem realidade
   - ❌ LUNA não pode operar em produção

3. **Confiança no Sistema:**
   - ❌ Usuários perdem confiança ao ver dados errados
   - ❌ Equipe do salão não pode usar o sistema
   - ❌ Risco de agendamentos conflitantes

### O Que Pode Estar Faltando para Resolver

#### 1. **API Key do Belasis** (Primário)

**O que é:** Token de autenticação para acessar a API do Belasis

**Como obter:**
```
1. Acessar https://api.belasis.com.br
2. Login com credenciais do salão
3. Menu: Configurações → API → Gerar Token
4. Copiar token (formato: bpk_xxxxxxxxxxxxxx)
5. Guardar em local seguro
```

**Formato esperado:**
```
bpk_501c3107d72d395b0cedccde3fc2049a431a017e
```

**Onde colocar:**
```env
BELASIS_API_KEY=bpk_SEU_TOKEN_AQUI
```

#### 2. **Configuração do Ambiente**

**Arquivo:** `.env`

**Configuração atual (ERRADA):**
```env
BELASIS_API_URL=https://api.belasis.com.br
BELASIS_API_KEY=
BELASIS_MOCK=true
```

**Configuração esperada (CORRETA):**
```env
BELASIS_API_URL=https://api.belasis.com.br
BELASIS_API_KEY=bpk_SEU_TOKEN_AQUI
BELASIS_MOCK=false
```

#### 3. **Reinicialização do Backend**

Após alterar `.env`, o backend precisa ser reiniciado:

```bash
# Se estiver usando Docker
docker compose restart luna-backend

# Ou se estiver rodando localmente
pkill -f "uvicorn.*main:app"
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. **Verificação de Conectividade**

**Possíveis problemas adicionais:**

a) **Firewall/Network:**
```bash
# Testar conectividade com Belasis
curl -I https://api.belasis.com.br/api/v1/employees \
  -H "ACCESS-TOKEN: bpk_SEU_TOKEN_AQUI"
```

b) **Token Inválido/Expirado:**
```bash
# Testar autenticação
curl https://api.belasis.com.br/api/v1/employees \
  -H "ACCESS-TOKEN: bpk_SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json"
```

c) **Rate Limit:**
- Belasis permite 30 requisições/minuto por API key
- Backend já tem rate limiter configurado

#### 5. **Validação dos Dados**

Após ativar Belasis real, validar:

```bash
# 1. Testar endpoint de profissionais
curl http://localhost:8000/api/belasis/professionals \
  -H "X-Admin-Key: SUA_ADMIN_KEY" | jq '.professionals[] | {id, name, active}'

# 2. Testar endpoint de serviços
curl http://localhost:8000/api/belasis/services \
  -H "X-Admin-Key: SUA_ADMIN_KEY" | jq '.services | length'

# 3. Testar endpoint de agenda
curl "http://localhost:8000/api/belasis/agenda?start_date=$(date +%Y-%m-%d)" \
  -H "X-Admin-Key: SUA_ADMIN_KEY" | jq '.appointments | length'

# 4. Verificar frontend
# Acessar http://localhost:3000/professionals
# Deve mostrar 9+ profissionais reais
```

## 📊 Benefícios de Resolver

### Imediatos
- ✅ Dados reais do salão
- ✅ Profissionais verdadeiros
- ✅ Serviços e preços corretos
- ✅ Agenda sincronizada

### Médio Prazo
- ✅ Agendamentos reais via WhatsApp
- ✅ Sincronização bidirecional
- ✅ Relatórios precisos
- ✅ Operação em produção

### Longo Prazo
- ✅ Confiança do usuário
- ✅ Redução de erros manuais
- ✅ Automação completa
- ✅ Escalabilidade

---

# Gap #2: Tabelas Redundantes de Campanhas

## 📍 Descrição Detalhada

O schema do Supabase possui **duas tabelas** para campanhas:

1. **`campaigns`** - Tabela principal, usada pelo backend
2. **`marketing_campaigns`** - Tabela secundária, possivelmente legado

## 🔬 Análise Técnica

### Estrutura das Tabelas

**Tabela `campaigns`:**
```sql
CREATE TABLE campaigns (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  status TEXT DEFAULT 'draft',
  description TEXT,
  start_date DATE,
  end_date DATE,
  discount_percent DECIMAL(5,2),
  discount_fixed DECIMAL(10,2),
  services TEXT[],
  trigger_keywords TEXT[],
  message_template TEXT,
  target_segment TEXT DEFAULT 'all',
  target_services TEXT[],
  add_on_services TEXT[],
  campaign_script TEXT,
  stats JSONB DEFAULT '{}',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Tabela `marketing_campaigns`:**
```sql
CREATE TABLE marketing_campaigns (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  status TEXT DEFAULT 'draft',
  description TEXT,
  start_date DATE,
  end_date DATE,
  discount_percent DECIMAL(5,2),
  -- ... campos similares
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Uso no Backend

**Tabela `campaigns` (ATIVA):**
```python
# backend/app/api/campaigns_new.py
@router.get("")
async def list_campaigns(status: str = None):
    db = get_supabase()
    query = db.table("campaigns").select("*")
    if status:
        query = query.eq("status", status)
    return query.execute().data
```

**Tabela `marketing_campaigns` (NÃO USADA):**
- Nenhuma referência no código backend
- Nenhum endpoint usa esta tabela
- Provavelmente é legado de refatoração anterior

## 💥 Impacto e Consequências

### Problemas Atuais

1. **Confusão de Desenvolvimento:**
   - Novos desenvolvedores podem usar a tabela errada
   - Dúvida sobre qual tabela é a "correta"
   - Documentação pode ficar inconsistente

2. **Dados Duplicados:**
   - Se alguém inserir em ambas as tabelas, há duplicação
   - Waste de storage (pequeno, mas desnecessário)
   - Possível inconsistência de dados

3. **Manutenção:**
   - Migrations precisam considerar ambas
   - Backups incluem dados desnecessários
   - Queries de análise podem pegar dados errados

### O Que Pode Estar Faltando para Resolver

#### 1. **Análise de Dados Existentes**

```sql
-- Verificar se marketing_campaigns tem dados
SELECT COUNT(*) FROM marketing_campaigns;

-- Verificar conteúdo
SELECT id, name, type, status, created_at 
FROM marketing_campaigns 
ORDER BY created_at DESC 
LIMIT 10;

-- Verificar se campaigns tem dados
SELECT COUNT(*) FROM campaigns;
```

#### 2. **Verificação de Dependências**

```bash
# Buscar referências a marketing_campaigns no código
grep -r "marketing_campaigns" backend/ frontend/

# Buscar referências no Supabase (functions, triggers, policies)
# No Supabase Dashboard ou via SQL:
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_definition LIKE '%marketing_campaigns%';
```

#### 3. **Plano de Ação**

**Cenário A: `marketing_campaigns` está vazia e sem dependências**
```sql
-- Remover tabela
DROP TABLE IF EXISTS marketing_campaigns CASCADE;

-- Remover policies RLS associadas
DROP POLICY IF EXISTS "Service role has full access" ON marketing_campaigns;

-- Remover triggers associados
DROP TRIGGER IF EXISTS update_marketing_campaigns_updated_at ON marketing_campaigns;
DROP FUNCTION IF EXISTS update_marketing_campaigns_updated_at() CASCADE;
```

**Cenário B: `marketing_campaigns` tem dados úteis**
```sql
-- Migrar dados para campaigns
INSERT INTO campaigns (name, type, status, description, start_date, end_date, ...)
SELECT name, type, status, description, start_date, end_date, ...
FROM marketing_campaigns
WHERE id NOT IN (SELECT id FROM campaigns);

-- Depois remover tabela
DROP TABLE marketing_campaigns CASCADE;
```

**Cenário C: `marketing_campaigns` é usada intencionalmente**
```sql
-- Renomear para clareza
ALTER TABLE marketing_campaigns RENAME TO campaigns_archive;

-- Ou adicionar comentário explicativo
COMMENT ON TABLE marketing_campaigns IS 
  'Legado: Usar tabela campaigns para novas campanhas';
```

#### 4. **Atualização de Documentação**

Após resolver, atualizar:
- `ARQUITETURA_ANALISE_COMPLETA.md`
- `LUNA_OS_ARCHITECTURE_DIAGRAMS.md`
- Comentários no código

## 📊 Benefícios de Resolver

### Imediatos
- ✅ Clareza sobre qual tabela usar
- ✅ Remoção de confusão
- ✅ Schema mais limpo

### Médio Prazo
- ✅ Menor risco de bugs
- ✅ Código mais manutenível
- ✅ Documentação consistente

### Longo Prazo
- ✅ Schema de banco otimizado
- ✅ Menor complexidade
- ✅ Melhor performance em queries

---

# Gap #3: Documentação do Endpoint Analytics

## 📍 Descrição Detalhada

O diagrama de arquitetura menciona o endpoint como `/api/analytics`, mas a implementação real usa `/api/analytics-super`.

## 🔬 Análise Técnica

### Discrepância

**Diagrama (`LUNA_OS_ARCHITECTURE_DIAGRAMS.md`):**
```
│  │  /api/conversations  /api/clients  /api/analytics  /api/semantic    │ │
```

**Implementação (`backend/app/main.py`):**
```python
from app.api.analytics_super import router as analytics_super_router

app.include_router(
    analytics_super.router,
    dependencies=_admin,
)  # Super Analytics
```

**Router (`backend/app/api/analytics_super.py`):**
```python
router = APIRouter(prefix="/api/analytics-super", tags=["Analytics Super"])

@router.get("")
async def get_analytics_dashboard():
    """Super Analytics Dashboard"""
    ...
```

### Origem da Discrepância

Provável cenário:
1. Endpoint foi originalmente criado como `/api/analytics`
2. Refatoração adicionou funcionalidades "super"
3. Router foi renomeado para `analytics-super`
4. Diagrama não foi atualizado

## 💥 Impacto e Consequências

### Problemas Atuais

1. **Confusão de Desenvolvimento:**
   - Novo dev pode procurar `/api/analytics` e não encontrar
   - Documentação inconsistente gera dúvidas
   - Tempo perdido procurando endpoint "fantasma"

2. **Integrações Externas:**
   - Se houver integrações documentadas, podem estar erradas
   - Webhooks ou scripts podem usar endpoint antigo

3. **Manutenção:**
   - Dificuldade em rastrear qual endpoint é o "correto"
   - Possibilidade de criar endpoint duplicado

### O Que Pode Estar Faltando para Resolver

#### 1. **Verificação de Uso Atual**

```bash
# Buscar referências no frontend
grep -r "analytics-super" frontend/
grep -r "/api/analytics" frontend/

# Buscar referências no backend
grep -r "analytics-super" backend/
grep -r "from app.api.analytics" backend/

# Buscar em testes
grep -r "analytics" backend/tests/
```

#### 2. **Plano de Ação**

**Opção A: Atualizar Diagrama (Recomendado)**
```markdown
# Em LUNA_OS_ARCHITECTURE_DIAGRAMS.md

Diff:
- /api/analytics
+ /api/analytics-super
```

**Opção B: Criar Alias (Se necessário compatibilidade)**
```python
# backend/app/main.py

# Manter endpoint novo
app.include_router(analytics_super.router, prefix="/api/analytics-super")

# Criar alias para endpoint antigo (redirect)
@app.get("/api/analytics")
async def analytics_redirect():
    return RedirectResponse(url="/api/analytics-super")
```

**Opção C: Renomear Endpoint (Breaking Change)**
```python
# Se quiser simplificar, remover "-super"
router = APIRouter(prefix="/api/analytics", tags=["Analytics"])
```

#### 3. **Atualização de Documentação**

Arquivos para atualizar:
- `LUNA_OS_ARCHITECTURE_DIAGRAMS.md`
- `README.md` (se mencionar analytics)
- `ARQUITETURA_ANALISE_COMPLETA.md`
- Qualquer documentação de API externa

## 📊 Benefícios de Resolver

### Imediatos
- ✅ Documentação consistente
- ✅ Menos confusão para devs

### Médio Prazo
- ✅ Melhor onboarding
- ✅ Menos erros de integração

---

# Gap #4: Configuração Milvus

## 📍 Descrição Detalhada

O diagrama de arquitetura menciona Milvus Vector Database na porta `:19530`, mas não está claro se esta configuração está documentada no `.env.example` e se está consistente com a implementação real.

## 🔬 Análise Técnica

### O Que é Milvus

**Milvus** é um banco de dados vetorial open-source usado para:
- Armazenar embeddings de conversas
- Busca semântica (RAG - Retrieval Augmented Generation)
- Similaridade de mensagens
- Context building para IA

### Configuração Atual

**Diagrama:**
```
MILVUS (Vector Database :19530)
  ┌──────────────────────────────────────────────────────────────┐
  │  luna_conversations                                          │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
  │  │conversation_ │  │  embedding   │  │   metadata   │       │
  │  │    id        │  │  [384 floats]│  │  - phone     │       │
  │  └──────────────┘  └──────────────┘  └──────────────┘       │
  └──────────────────────────────────────────────────────────────┘
```

**Implementação (`backend/app/integrations/vector_db_manager.py`):**
```python
from pymilvus import connections, Collection

class VectorDBManager:
    async def connect(self):
        # Lê configuração do ambiente
        host = os.getenv("MILVUS_HOST", "localhost")
        port = int(os.getenv("MILVUS_PORT", "19530"))
        
        connections.connect(
            host=host,
            port=port,
        )
```

**Uso no Brain:**
```python
# backend/app/core/brain.py
from app.integrations.semantic_memory import get_semantic_memory

semantic_memory = get_semantic_memory()

async def build_rag_context(self, phone: str, message: str):
    # Busca conversas similares no Milvus
    similar = await semantic_memory.search_similar(
        phone=phone,
        message=message,
        limit=5
    )
    return similar
```

### Configuração no `.env.example`

**Status atual:** Precisa verificação

**Configuração esperada:**
```env
# Milvus Vector Database
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_USER=
MILVUS_PASSWORD=
MILVUS_SECURE=false
```

## 💥 Impacto e Consequências

### Problemas Potenciais

1. **Configuração Não Documentada:**
   - Novos desenvolvedores não sabem configurar Milvus
   - Ambiente de desenvolvimento pode não funcionar
   - Deploy em produção pode falhar

2. **Porta Incorreta:**
   - Se porta no `.env` for diferente de 19530, conexão falha
   - Docker pode não estar expondo porta correta

3. **Milvus Não Inicializado:**
   - Se Milvus não estiver rodando, RAG não funciona
   - LUNA perde contexto de conversas passadas
   - Respostas ficam menos inteligentes

### O Que Pode Estar Faltando para Resolver

#### 1. **Verificação do `.env.example`**

```bash
# Verificar se Milvus está documentado
grep -i "milvus" .env.example

# Se não existir, adicionar:
cat >> .env.example << 'EOF'

# Milvus Vector Database (RAG)
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_USER=
MILVUS_PASSWORD=
MILVUS_SECURE=false
EOF
```

#### 2. **Verificação do Docker Compose**

```yaml
# docker-compose.yml

services:
  milvus-standalone:
    image: milvusdb/milvus:v2.3.0
    container_name: milvus-standalone
    ports:
      - "19530:19530"  # ← Verificar se está correto
      - "9091:9091"    # Milvus Inspector
    environment:
      - ETCD_USE_EMBED=true
      - ETCD_DATA_DIR=/var/lib/milvus/etcd
    volumes:
      - milvus-data:/var/lib/milvus
```

#### 3. **Verificação de Conectividade**

```bash
# Testar conexão com Milvus
docker exec -it milvus-standalone bash
# Dentro do container:
milvus-cli show collections

# Ou via Python:
python -c "
from pymilvus import connections
connections.connect(host='localhost', port=19530)
print('Milvus connected!')
"
```

#### 4. **Verificação de Collections**

```python
# Script de verificação
from pymilvus import connections, utility

connections.connect(host="localhost", port=19530)

# Listar collections
collections = utility.list_collections()
print(f"Collections: {collections}")

# Verificar se collections do LUNA existem
expected = ["luna_conversations", "luna_knowledge_base"]
for col in expected:
    if col in collections:
        print(f"✅ {col} exists")
    else:
        print(f"❌ {col} missing")
```

#### 5. **Plano de Ação**

**Se Milvus não estiver configurado:**

a) Adicionar ao `docker-compose.yml`:
```yaml
services:
  milvus-standalone:
    image: milvusdb/milvus:v2.3.0
    ports:
      - "19530:19530"
    environment:
      - ETCD_USE_EMBED=true
    volumes:
      - milvus-data:/var/lib/milvus
```

b) Adicionar ao `.env.example`:
```env
# Milvus Vector Database
MILVUS_HOST=luna-milvus
MILVUS_PORT=19530
```

c) Atualizar documentação:
- `README.md` - Adicionar Milvus nos pré-requisitos
- `LUNA_OS_ARCHITECTURE_DIAGRAMS.md` - Confirmar porta

## 📊 Benefícios de Resolver

### Imediatos
- ✅ Configuração clara e documentada
- ✅ Setup de desenvolvimento mais fácil

### Médio Prazo
- ✅ RAG funcionando corretamente
- ✅ Contexto de conversas preservado

### Longo Prazo
- ✅ IA mais inteligente com histórico
- ✅ Melhor experiência do usuário

---

# Gap #5: Endpoint de Histórico WhatsApp

## 📍 Descrição Detalhada

A tabela `whatsapp_messages_history` existe no Supabase mas não há um endpoint dedicado na API para consultar este histórico.

## 🔬 Análise Técnica

### Estrutura da Tabela

```sql
CREATE TABLE whatsapp_messages_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  message_id TEXT UNIQUE,           -- ID único da Evolution API
  phone TEXT NOT NULL,              -- Número do telefone
  sender_name TEXT,                 -- Nome do remetente
  content TEXT,                     -- Conteúdo da mensagem
  direction TEXT CHECK (direction IN ('inbound', 'outbound')),
  message_timestamp TIMESTAMPTZ NOT NULL,
  is_group BOOLEAN DEFAULT false,
  instance_name TEXT DEFAULT 'haven',
  metadata JSONB DEFAULT '{}'
);

-- Índices
CREATE INDEX idx_wmh_phone ON whatsapp_messages_history(phone);
CREATE INDEX idx_wmh_timestamp ON whatsapp_messages_history(message_timestamp);
CREATE INDEX idx_wmh_is_group ON whatsapp_messages_history(is_group);
```

### Uso Atual

**Inserção (EXISTE):**
```python
# backend/app/integrations/evolution.py
async def save_message_to_history(self, message: dict):
    db = get_supabase()
    db.table("whatsapp_messages_history").insert({
        "message_id": message["id"],
        "phone": message["phone"],
        "content": message["content"],
        "direction": message["direction"],
        "message_timestamp": message["timestamp"],
        "metadata": message.get("metadata", {}),
    }).execute()
```

**Consulta (NÃO EXISTE):**
- Nenhum endpoint `/api/history` ou similar
- Dados são inseridos mas não consultados via API
- Apenas acesso direto ao banco possível

## 💥 Impacto e Consequências

### Problemas Atuais

1. **Dados Inacessíveis:**
   - Histórico é armazenado mas não pode ser consultado
   - Impossível auditar conversas passadas
   - Dados ficam "órfãos" no banco

2. **Compliance e Auditoria:**
   - Não há como exportar histórico para compliance
   - Impossível gerar relatórios de conversas
   - Dificuldade em investigar problemas

3. **Features Perdidas:**
   - Não é possível mostrar histórico no frontend
   - Busca em conversas antigas não funciona
   - Analytics perde dados históricos

### Casos de Uso Potenciais

1. **Auditoria:**
   ```
   "Preciso ver todas as mensagens trocadas com cliente X em Março"
   ```

2. **Relatórios:**
   ```
   "Quantas mensagens foram enviadas/recebidas por dia?"
   ```

3. **Debug:**
   ```
   "O que foi dito nesta conversa específica?"
   ```

4. **Exportação:**
   ```
   "Exportar histórico de conversas para backup"
   ```

### O Que Pode Estar Faltando para Resolver

#### 1. **Criar Endpoint de Consulta**

**Arquivo:** `backend/app/api/history.py`

```python
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from datetime import datetime
from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/history", tags=["WhatsApp History"])


@router.get("")
async def get_whatsapp_history(
    phone: Optional[str] = Query(None, description="Phone number to filter"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    direction: Optional[str] = Query(None, description="inbound or outbound"),
    is_group: Optional[bool] = Query(None, description="Filter by group messages"),
    limit: int = Query(100, ge=1, le=1000, description="Max results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
):
    """
    Consulta histórico de mensagens WhatsApp.
    
    - **phone**: Filtrar por número de telefone
    - **start_date**: Data inicial (YYYY-MM-DD)
    - **end_date**: Data final (YYYY-MM-DD)
    - **direction**: Filtrar por direção (inbound/outbound)
    - **is_group**: Filtrar por mensagens de grupo
    - **limit**: Máximo de resultados (1-1000)
    - **offset**: Paginação
    """
    db = get_supabase()
    
    query = db.table("whatsapp_messages_history").select("*", count="exact")
    
    # Aplicar filtros
    if phone:
        query = query.eq("phone", phone)
    
    if start_date:
        query = query.gte("message_timestamp", start_date)
    
    if end_date:
        query = query.lte("message_timestamp", end_date)
    
    if direction:
        query = query.eq("direction", direction)
    
    if is_group is not None:
        query = query.eq("is_group", is_group)
    
    # Ordenar e paginar
    result = (
        query
        .order("message_timestamp", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    
    return {
        "messages": result.data,
        "total": result.count,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{message_id}")
async def get_message_by_id(message_id: str):
    """Busca mensagem específica por ID."""
    db = get_supabase()
    
    result = (
        db.table("whatsapp_messages_history")
        .select("*")
        .eq("message_id", message_id)
        .execute()
    )
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return {"message": result.data[0]}


@router.get("/stats/summary")
async def get_history_stats(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """
    Estatísticas do histórico de mensagens.
    """
    db = get_supabase()
    
    query = db.table("whatsapp_messages_history").select("*")
    
    if start_date:
        query = query.gte("message_timestamp", start_date)
    if end_date:
        query = query.lte("message_timestamp", end_date)
    
    messages = query.execute().data
    
    stats = {
        "total_messages": len(messages),
        "inbound": sum(1 for m in messages if m["direction"] == "inbound"),
        "outbound": sum(1 for m in messages if m["direction"] == "outbound"),
        "groups": sum(1 for m in messages if m["is_group"]),
        "unique_phones": len(set(m["phone"] for m in messages)),
    }
    
    return stats
```

#### 2. **Registrar Router no Main.py**

```python
# backend/app/main.py
from app.api.history import router as history_router

app.include_router(
    history_router,
    dependencies=[Depends(require_admin_key)],
)
```

#### 3. **Criar Página no Frontend (Opcional)**

**Arquivo:** `frontend/app/history/page.tsx`

```tsx
"use client";

import useSWR from 'swr';
import { apiFetch } from '@/lib/api';

export default function HistoryPage() {
  const { data, error } = useSWR('/api/history?limit=50', (url) =>
    apiFetch(url).then(r => r.json())
  );

  if (error) return <div>Erro ao carregar histórico</div>;
  if (!data) return <div>Carregando...</div>;

  return (
    <div>
      <h1>Histórico de Mensagens</h1>
      <p>Total: {data.total}</p>
      {data.messages.map(msg => (
        <div key={msg.id}>
          <span>{msg.phone}</span>
          <span>{msg.direction}</span>
          <span>{msg.content}</span>
          <span>{msg.message_timestamp}</span>
        </div>
      ))}
    </div>
  );
}
```

#### 4. **Considerações de Performance**

Para grandes volumes de dados:

```sql
-- Adicionar índices compostos
CREATE INDEX idx_wmh_phone_timestamp 
ON whatsapp_messages_history(phone, message_timestamp);

CREATE INDEX idx_wmh_direction_timestamp 
ON whatsapp_messages_history(direction, message_timestamp);

-- Considerar particionamento por data (se > 1M mensagens)
-- CREATE TABLE whatsapp_messages_history_2026_01 PARTITION OF whatsapp_messages_history
-- FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

## 📊 Benefícios de Resolver

### Imediatos
- ✅ Histórico consultável via API
- ✅ Auditoria e compliance possíveis

### Médio Prazo
- ✅ Página de histórico no frontend
- ✅ Relatórios e analytics enriquecidos

### Longo Prazo
- ✅ Exportação de dados
- ✅ Busca em conversas antigas
- ✅ Melhor inteligência de negócio

---

# Gap #6: Components de Domínio no Frontend

## 📍 Descrição Detalhada

O frontend possui apenas componentes UI genéricos (`Button`, `Card`, `Dialog`, etc.) mas não tem components específicos de domínio (`ConversationCard`, `ClientProfile`, `AppointmentItem`, etc.).

## 🔬 Análise Técnica

### Estrutura Atual

**Components Existentes (`frontend/components/`):**
```
components/
  ├── ui/
  │   ├── Button.tsx
  │   ├── Card.tsx
  │   ├── Dialog.tsx
  │   ├── Input.tsx
  │   ├── Tooltip.tsx
  │   └── text-scramble.tsx
  ├── ErrorBoundary.tsx
  ├── PageShell.tsx
  ├── Sidebar.tsx
  └── demo-text-scramble.tsx
```

**Components Faltantes (Domínio):**
```
components/domain/  ← NÃO EXISTE
  ├── ConversationCard.tsx
  ├── ConversationList.tsx
  ├── ClientProfile.tsx
  ├── ClientCard.tsx
  ├── AppointmentItem.tsx
  ├── AppointmentCalendar.tsx
  ├── CampaignCard.tsx
  ├── CampaignForm.tsx
  ├── ProfessionalCard.tsx
  ├── ServiceItem.tsx
  ├── MessageBubble.tsx
  ├── MessageList.tsx
  ├── IntelligenceCard.tsx
  ├── DojoScenarioCard.tsx
  └── ...
```

### Código Atual (Exemplo)

**Página de Conversas (`frontend/app/conversations/page.tsx`):**
```tsx
export default function ConversationsPage() {
  const { data } = useSWR('/api/conversations', fetcher);

  return (
    <div>
      {data?.map(conv => (
        // Lógica de UI misturada com lógica de domínio
        <div key={conv.id} className="rounded-[2rem] p-5" 
          style={{ background: '#17101A' }}>
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient">
              {conv.client_name?.[0]}
            </div>
            <div>
              <h3 className="text-base font-black">{conv.client_name}</h3>
              <p className="text-xs text-luna_pink-500">{conv.phone}</p>
            </div>
            <span className={`px-2 py-1 rounded-full text-xs ${
              conv.status === 'active' ? 'bg-green-900' : 'bg-gray-700'
            }`}>
              {conv.status}
            </span>
          </div>
          {/* Mais UI inline... */}
        </div>
      ))}
    </div>
  );
}
```

### Código Ideal (Com Components de Domínio)

```tsx
import { ConversationCard } from '@/components/domain/ConversationCard';

export default function ConversationsPage() {
  const { data } = useSWR('/api/conversations', fetcher);

  return (
    <div>
      {data?.map(conv => (
        <ConversationCard
          key={conv.id}
          conversation={conv}
          onClick={() => router.push(`/conversations/${conv.id}`)}
        />
      ))}
    </div>
  );
}
```

## 💥 Impacto e Consequências

### Problemas Atuais

1. **Código Duplicado:**
   - Mesma lógica de UI repetida em várias páginas
   - Se estilo mudar, precisa atualizar em múltiplos lugares
   - Maior chance de inconsistências visuais

2. **Manutenção Difícil:**
   - Páginas ficam grandes e complexas
   - Difícil testar componentes isoladamente
   - Refatoração é arriscada

3. **Onboarding Lento:**
   - Novos devs não encontram components de domínio
   - Precisa entender lógica de UI em cada página
   - Curva de aprendizado mais íngreme

4. **Testabilidade:**
   - Difícil testar componentes isoladamente
   - Testes precisam renderizar páginas completas
   - Cobertura de testes menor

### O Que Pode Estar Faltando para Resolver

#### 1. **Identificar Components Comuns**

Analisar páginas existentes e extrair padrões:

```bash
# Analisar páginas para encontrar padrões
grep -r "className.*rounded-\[2rem\]" frontend/app/
grep -r "bg-gradient" frontend/app/
```

#### 2. **Criar Estrutura de Components de Domínio**

**Arquivo:** `frontend/components/domain/ConversationCard.tsx`

```tsx
import { motion } from 'framer-motion';
import { Clock, MessageCircle, User } from 'lucide-react';

type Conversation = {
  id: string;
  client_name: string;
  client_phone: string;
  status: 'active' | 'closed' | 'pending';
  intent?: string;
  sentiment?: string;
  messages_count: number;
  started_at: string;
  last_message_at?: string;
};

type Props = {
  conversation: Conversation;
  onClick?: () => void;
  isSelected?: boolean;
};

const STATUS_COLORS = {
  active: 'bg-emerald-900/30 text-emerald-400 border-emerald-800',
  closed: 'bg-gray-800/30 text-gray-400 border-gray-700',
  pending: 'bg-amber-900/30 text-amber-400 border-amber-800',
};

export function ConversationCard({ conversation, onClick, isSelected }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-[2rem] p-5 transition-all cursor-pointer"
      style={{
        background: '#17101A',
        border: isSelected
          ? '1px solid rgba(201,151,123,0.5)'
          : '1px solid rgba(201,151,123,0.12)',
      }}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-start gap-3 mb-3">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-luna_pink-500 to-luna_pink-700 
          flex items-center justify-center text-white text-lg font-black flex-shrink-0">
          {conversation.client_name?.[0]?.toUpperCase()}
        </div>
        
        <div className="flex-1 min-w-0">
          <h2 className="text-base font-black text-luna_pink-100 truncate">
            {conversation.client_name || 'Cliente não identificado'}
          </h2>
          <div className="flex items-center gap-2 mt-0.5">
            <User className="w-3 h-3 text-luna_pink-600" />
            <span className="text-[10px] text-luna_pink-500 font-medium">
              {conversation.client_phone}
            </span>
          </div>
        </div>

        <span className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border ${
          STATUS_COLORS[conversation.status]
        }`}>
          {conversation.status}
        </span>
      </div>

      {/* Meta info */}
      <div className="flex items-center gap-3 text-[10px] text-luna_pink-600 font-semibold">
        <div className="flex items-center gap-1">
          <MessageCircle className="w-2.5 h-2.5" />
          <span>{conversation.messages_count} msgs</span>
        </div>
        
        {conversation.intent && (
          <div className="flex items-center gap-1">
            <span className="text-luna_pink-400">Intent:</span>
            <span className="text-luna_pink-300">{conversation.intent}</span>
          </div>
        )}
        
        {conversation.sentiment && (
          <div className="flex items-center gap-1">
            <span className="text-luna_pink-400">Sentimento:</span>
            <span className={`
              ${conversation.sentiment === 'positive' ? 'text-emerald-400' : ''}
              ${conversation.sentiment === 'negative' ? 'text-red-400' : ''}
              ${conversation.sentiment === 'neutral' ? 'text-gray-400' : ''}
            `}>
              {conversation.sentiment}
            </span>
          </div>
        )}
      </div>

      {/* Timestamp */}
      <div className="flex items-center gap-1 mt-3 text-[10px] text-luna_pink-700">
        <Clock className="w-2.5 h-2.5" />
        <span>{new Date(conversation.started_at).toLocaleString('pt-BR')}</span>
      </div>
    </motion.div>
  );
}
```

#### 3. **Refatorar Páginas Existentes**

**Antes:**
```tsx
// frontend/app/conversations/page.tsx
export default function ConversationsPage() {
  const { data } = useSWR('/api/conversations', fetcher);

  return (
    <div className="grid gap-4">
      {data?.map(conv => (
        <div key={conv.id} className="rounded-[2rem] p-5" 
          style={{ background: '#17101A' }}>
          {/* 100+ linhas de UI inline */}
        </div>
      ))}
    </div>
  );
}
```

**Depois:**
```tsx
import { ConversationCard } from '@/components/domain/ConversationCard';

export default function ConversationsPage() {
  const { data, isLoading } = useSWR('/api/conversations', fetcher);

  if (isLoading) return <ConversationsSkeleton />;
  if (!data?.length) return <EmptyState />;

  return (
    <div className="grid gap-4">
      {data.map(conv => (
        <ConversationCard
          key={conv.id}
          conversation={conv}
          onClick={() => router.push(`/conversations/${conv.id}`)}
        />
      ))}
    </div>
  );
}
```

#### 4. **Plano de Implementação**

**Fase 1: Components Críticos (1-2 dias)**
- [ ] `ConversationCard`
- [ ] `ClientCard`
- [ ] `MessageBubble`
- [ ] `AppointmentItem`

**Fase 2: Components Secundários (2-3 dias)**
- [ ] `CampaignCard`
- [ ] `ProfessionalCard`
- [ ] `ServiceItem`
- [ ] `IntelligenceCard`

**Fase 3: Components Complexos (3-5 dias)**
- [ ] `ConversationList` (com paginação)
- [ ] `AppointmentCalendar` (com drag-drop)
- [ ] `CampaignForm` (com validação)
- [ ] `DojoScenarioCard` (com métricas)

**Fase 4: Testes e Documentação (1-2 dias)**
- [ ] Testes unitários para cada component
- [ ] Storybook para documentação visual
- [ ] Guidelines de uso

## 📊 Benefícios de Resolver

### Imediatos
- ✅ Código mais limpo e organizado
- ✅ Menos duplicação

### Médio Prazo
- ✅ Mais fácil adicionar novas features
- ✅ Testes mais fáceis de escrever

### Longo Prazo
- ✅ Design system consistente
- ✅ Onboarding mais rápido
- ✅ Melhor qualidade de código

---

# 📋 RESUMO GERAL DOS GAPS

| # | Gap | Prioridade | Esforço | Impacto |
|---|-----|------------|---------|---------|
| 1 | Belasis Mock Ativo | 🔴 CRÍTICA | 1 hora | 🔴 ALTO |
| 2 | Tabelas Redundantes | 🟡 BAIXA | 2 horas | 🟡 MÉDIO |
| 3 | Documentação Analytics | 🟡 BAIXA | 30 min | 🟡 BAIXO |
| 4 | Configuração Milvus | 🟡 BAIXA | 2 horas | 🟡 MÉDIO |
| 5 | Endpoint Histórico | 🟡 MÉDIA | 4 horas | 🟢 ALTO |
| 6 | Components Domínio | 🟡 MÉDIA | 3-5 dias | 🟢 ALTO |

---

# 🎯 PLANO DE AÇÃO RECOMENDADO

## Semana 1 (Crítico)
- [ ] **Dia 1:** Resolver Gap #1 (Belasis Mock)
  - Obter API Key
  - Atualizar `.env`
  - Testar integração real

## Semana 2 (Importante)
- [ ] **Dia 1-2:** Resolver Gap #5 (Endpoint Histórico)
  - Criar `/api/history`
  - Testar queries
  - Documentar

- [ ] **Dia 3-5:** Iniciar Gap #6 (Components Domínio)
  - Criar estrutura
  - Implementar components críticos

## Semana 3 (Manutenção)
- [ ] **Dia 1:** Resolver Gap #2 (Tabelas Redundantes)
- [ ] **Dia 2:** Resolver Gap #3 (Documentação Analytics)
- [ ] **Dia 3:** Resolver Gap #4 (Configuração Milvus)
- [ ] **Dia 4-5:** Continuar Gap #6 (Components Domínio)

---

**Documento criado:** 2026-03-11  
**Próxima atualização:** Após resolução de cada gap  
**Responsável:** Equipe LUNA OS
