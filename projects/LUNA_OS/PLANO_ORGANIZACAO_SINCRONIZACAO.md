# 🔄 PLANO DE ORGANIZAÇÃO E SINCRONIZAÇÃO

**Data:** 2026-03-01  
**Status:** ⚠️ **EM ANDAMENTO**  
**Objetivo:** Sincronizar Supabase ↔ Obsidian ↔ Painel Dashboard

---

## 🎯 VISÃO GERAL

### Sistemas que Precisam de Sincronização:

```
┌─────────────────┐
│   SUABASE       │
│   (Database)    │
│   - Serviços    │
│   - Profissionais│
│   - Clientes    │
│   - Agendamentos│
└────────┬────────┘
         │
         │ Sync Bidirecional
         │
┌────────▼────────┐
│   OBSIDIAN      │
│   (Knowledge)   │
│   - Serviços.md │
│   - Profis.md   │
│   - Clients.md  │
│   - Journals.md │
└────────┬────────┘
         │
         │ API REST
         │
┌────────▼────────┐
│   PAINEL        │
│   (Dashboard)   │
│   - Analytics   │
│   - Agenda      │
│   - Clientes    │
│   - Relatórios  │
└─────────────────┘
```

---

## 📊 STATUS ATUAL POR SISTEMA

### 1. SUABASE ⚠️

| Tabela | Status | Registros | Última Sync |
|--------|--------|-----------|-------------|
| `knowledge_base` | ⚠️ Seed pronto | 0 | Nunca |
| `clients` | ✅ Ativa | 758 | - |
| `professionals` | ⚠️ Precisa popular | 0 | Nunca |
| `services` | ⚠️ Precisa popular | 0 | Nunca |
| `appointments` | ✅ Ativa | - | - |
| `conversations` | ✅ Ativa | 204 | - |

**O Que Falta:**
- ⏳ Executar seed_haven.py
- ⏳ Popular tabela `professionals`
- ⏳ Popular tabela `services`
- ⏳ Criar triggers de sync

---

### 2. OBSIDIAN ✅

| Categoria | Status | Arquivos | Última Atualização |
|-----------|--------|----------|-------------------|
| `Services/` | ✅ Completo | 41 | 2026-03-01 |
| `Professionals/` | ⚠️ Parcial | 0 | Nunca |
| `Clients/` | ✅ Completo | 758 | 2026-03-01 |
| `Journals/` | ✅ Completo | 204 | 2026-03-01 |
| `FAQs/` | ⚠️ Parcial | 4 | 2026-03-01 |
| `Packages/` | ⚠️ Parcial | 0 | Nunca |

**O Que Falta:**
- ⏳ Criar arquivos de Profissionais (9)
- ⏳ Criar arquivos de Pacotes (4)
- ⏳ Atualizar FAQs com formato padronizado

---

### 3. PAINEL DASHBOARD ⚠️

| Página | Status | Dados | Última Sync |
|--------|--------|-------|-------------|
| `/dashboard` | ✅ Funcional | Supabase | - |
| `/clients` | ✅ Funcional | Supabase | - |
| `/conversations` | ✅ Funcional | Supabase | - |
| `/analytics` | ✅ Funcional | Supabase | - |
| `/intelligence` | ⚠️ Criada | Obsidian | Nunca |
| `/dojo` | ⚠️ Criada | Local | Nunca |

**O Que Falta:**
- ⏳ Página `/professionals`
- ⏳ Página `/services`
- ⏳ Página `/packages`
- ⏳ Integração com Obsidian

---

## 🔄 MATRIZ DE SINCRONIZAÇÃO

### Dados que Devem Ser Sincronizados:

| Dado | Origem | Destino | Frequência | Método |
|------|--------|---------|------------|--------|
| **Serviços** | Supabase | Obsidian | Diário | Script Python |
| **Serviços** | Supabase | Painel | Real-time | API REST |
| **Profissionais** | Supabase | Obsidian | Diário | Script Python |
| **Profissionais** | Supabase | Painel | Real-time | API REST |
| **Clientes** | Supabase | Obsidian | Horário | Daemon Sync |
| **Clientes** | Supabase | Painel | Real-time | API REST |
| **Journals** | Supabase | Obsidian | Horário | Daemon Sync |
| **Agendamentos** | Supabase | Painel | Real-time | API REST |
| **FAQs** | Supabase | Obsidian | Semanal | Script Python |
| **Pacotes** | Supabase | Obsidian | Semanal | Script Python |
| **Pacotes** | Supabase | Painel | Real-time | API REST |

---

## 📋 CHECKLIST DE ORGANIZAÇÃO

### FASE 1: Organizar Supabase ⚠️

#### 1.1 Executar Seed Haven
```bash
cd backend
python app/scripts/seed_haven.py
```

**Checklist:**
- [ ] 41 serviços inseridos
- [ ] 9 profissionais inseridos
- [ ] 5 cupons inseridos
- [ ] 4 FAQs inseridos
- [ ] 4 pacotes inseridos
- [ ] 1 business_info inserido

#### 1.2 Criar Tabelas Faltantes
```sql
-- Tabela professionals
CREATE TABLE IF NOT EXISTS professionals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  nickname TEXT,
  specialties TEXT[],
  schedule JSONB,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Tabela services
CREATE TABLE IF NOT EXISTS services (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  promo_price DECIMAL(10,2),
  duration_min INTEGER,
  category TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);
```

#### 1.3 Criar Triggers de Atualização
```sql
-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar triggers
CREATE TRIGGER update_professionals_updated_at BEFORE UPDATE ON professionals
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_services_updated_at BEFORE UPDATE ON services
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

### FASE 2: Organizar Obsidian ⚠️

#### 2.1 Criar Arquivos de Profissionais (9 arquivos)

**Template:** `Templates/Professional.md`
```markdown
---
tags:
  - professional
  - team
category: PROFESSIONALS
name: "{{name}}"
nickname: "{{nickname}}"
specialties: {{specialties}}
schedule: {{schedule}}
is_active: true
---

# 👩‍🦱 {{name}} ({{nickname}})

## 📊 Informações
- **Especialidades:** {{specialties}}
- **Horários:** {{schedule}}
- **Status:** {{is_active}}

## 🔄 Agenda
{{agenda_details}}

## 📝 Notas
{{notes}}

## 🔗 Links
- [[000_MCT_MASTER_INDEX]]
- [[SERVICES]]

---

*Última atualização: {{date}}*
```

**Script de Geração:**
```python
# backend/app/scripts/sync_professionals_obsidian.py
#!/usr/bin/env python3
"""
Sincroniza profissionais do Supabase para Obsidian
"""

from supabase import create_client
from pathlib import Path

def sync_professionals():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Buscar profissionais do Supabase
    result = supabase.table("professionals").select("*").execute()
    
    # Criar arquivos no Obsidian
    obsidian_path = Path("backend/app/knowledge/obsidian_vault/_Active/02-KNOWLEDGE/PROFESSIONALS/")
    obsidian_path.mkdir(parents=True, exist_ok=True)
    
    for prof in result.data:
        # Gerar arquivo Markdown
        content = generate_professional_md(prof)
        
        # Salvar arquivo
        filename = f"PROF-{prof['id']}.md"
        filepath = obsidian_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {prof['name']} sincronizado")

if __name__ == "__main__":
    sync_professionals()
```

#### 2.2 Criar Arquivos de Pacotes (4 arquivos)

**Template:** `Templates/Package.md`
```markdown
---
tags:
  - package
  - offer
category: PACKAGES
name: "{{name}}"
quantity: {{quantity}}
price: {{price}}
validity_days: {{validity_days}}
payment: {{payment}}
---

# 📦 {{name}}

## 📊 Informações
- **Quantidade:** {{quantity}}
- **Preço:** R$ {{price}}
- **Validade:** {{validity_days}} dias
- **Pagamento:** {{payment}}

## 📝 Detalhes
{{details}}

## 🔗 Links
- [[000_MCT_MASTER_INDEX]]
- [[SERVICES]]

---

*Última atualização: {{date}}*
```

#### 2.3 Atualizar FAQs (4 arquivos)

**Formato Padronizado:**
```markdown
---
tags:
  - faq
  - general
category: FAQS
question: "{{question}}"
answer: {{answer}}
---

# ❓ {{question}}

**Resposta:** {{answer}}

## 🔗 Links
- [[000_MCT_MASTER_INDEX]]

---

*Última atualização: {{date}}*
```

---

### FASE 3: Organizar Painel Dashboard ⚠️

#### 3.1 Criar Página `/professionals`

**Arquivo:** `frontend/app/professionals/page.tsx`
```tsx
"use client";

import useSWR from 'swr';
import { Users, Clock, Star } from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

export default function ProfessionalsPage() {
  const { data } = useSWR('/api/professionals', fetcher);
  
  return (
    <div className="flex-1 overflow-y-auto p-8">
      <h1 className="text-3xl font-black mb-6">Profissionais</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data?.professionals?.map((prof: any) => (
          <div key={prof.id} className="bg-white rounded-2xl shadow-xl p-6">
            <div className="flex items-center gap-4 mb-4">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white text-2xl font-black">
                {prof.nickname?.[0] || prof.name[0]}
              </div>
              <div>
                <h2 className="text-xl font-black">{prof.name}</h2>
                <p className="text-gray-600">{prof.nickname}</p>
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Star className="w-4 h-4 text-yellow-500" />
                <span className="text-sm">{prof.specialties?.join(', ')}</span>
              </div>
              
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-blue-500" />
                <span className="text-sm">{prof.schedule}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

#### 3.2 Criar Página `/services`

**Arquivo:** `frontend/app/services/page.tsx`
```tsx
"use client";

import useSWR from 'swr';
import { Scissors, Clock, DollarSign } from 'lucide-react';

export default function ServicesPage() {
  const { data } = useSWR('/api/services', fetcher);
  
  return (
    <div className="flex-1 overflow-y-auto p-8">
      <h1 className="text-3xl font-black mb-6">Serviços</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data?.services?.map((service: any) => (
          <div key={service.id} className="bg-white rounded-2xl shadow-xl p-6">
            <h2 className="text-xl font-black mb-4">{service.name}</h2>
            
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <DollarSign className="w-4 h-4 text-green-500" />
                <span className="text-sm">R$ {service.price}</span>
              </div>
              
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-blue-500" />
                <span className="text-sm">{service.duration_min} min</span>
              </div>
              
              <div className="flex items-center gap-2">
                <Scissors className="w-4 h-4 text-purple-500" />
                <span className="text-sm">{service.category}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

#### 3.3 Criar Página `/intelligence`

**Arquivo:** `frontend/app/intelligence/page.tsx` (já existe, atualizar)
```tsx
// Adicionar abas para:
// - Propostas do Dojo
// - Inteligência de Clientes
// - Edge Cases
```

---

### FASE 4: Scripts de Sincronização ⚠️

#### 4.1 Daemon de Sync (Horário)

**Script:** `backend/app/scripts/obsidian_sync_daemon.py`
```python
#!/usr/bin/env python3
"""
Daemon de Sincronização Supabase → Obsidian

Roda a cada hora e sincroniza:
- Clientes novos
- Journals novos
- Profissionais atualizados
- Serviços atualizados
"""

import time
import schedule
from pathlib import Path

def sync_clients():
    """Sincroniza clientes novos do Supabase para Obsidian"""
    print("🔄 Syncing clients...")
    # Implementar lógica de sync
    pass

def sync_journals():
    """Sincroniza journals novos do Supabase para Obsidian"""
    print("🔄 Syncing journals...")
    # Implementar lógica de sync
    pass

def sync_professionals():
    """Sincroniza profissionais do Supabase para Obsidian"""
    print("🔄 Syncing professionals...")
    # Implementar lógica de sync
    pass

def sync_services():
    """Sincroniza serviços do Supabase para Obsidian"""
    print("🔄 Syncing services...")
    # Implementar lógica de sync
    pass

# Agendar execuções
schedule.every().hour.do(sync_clients)
schedule.every().hour.do(sync_journals)
schedule.every().day.at("02:00").do(sync_professionals)
schedule.every().sunday.at("03:00").do(sync_services)

# Rodar daemon
if __name__ == "__main__":
    print("🚀 Starting Obsidian Sync Daemon...")
    while True:
        schedule.run_pending()
        time.sleep(60)
```

#### 4.2 API Endpoints para Painel

**Arquivo:** `backend/app/api/professionals.py`
```python
from fastapi import APIRouter, HTTPException
from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/professionals", tags=["Professionals"])

@router.get("")
async def list_professionals():
    """Lista todos os profissionais"""
    supabase = get_supabase()
    
    result = supabase.table("professionals").select("*").eq("is_active", True).execute()
    
    return {"professionals": result.data, "total": len(result.data)}

@router.get("/{professional_id}")
async def get_professional(professional_id: str):
    """Busca profissional por ID"""
    supabase = get_supabase()
    
    result = supabase.table("professionals").select("*").eq("id", professional_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Professional not found")
    
    return {"professional": result.data[0]}
```

**Arquivo:** `backend/app/api/services.py`
```python
from fastapi import APIRouter, HTTPException
from app.integrations.supabase_client import get_supabase

router = APIRouter(prefix="/api/services", tags=["Services"])

@router.get("")
async def list_services():
    """Lista todos os serviços"""
    supabase = get_supabase()
    
    result = supabase.table("services").select("*").eq("is_active", True).execute()
    
    return {"services": result.data, "total": len(result.data)}

@router.get("/{service_id}")
async def get_service(service_id: str):
    """Busca serviço por ID"""
    supabase = get_supabase()
    
    result = supabase.table("services").select("*").eq("id", service_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return {"service": result.data[0]}
```

---

## 📊 CRONOGRAMA DE IMPLEMENTAÇÃO

### Semana 1: Supabase ⚠️
- [ ] Executar seed_haven.py
- [ ] Criar tabelas professionals e services
- [ ] Criar triggers de atualização
- [ ] Validar dados inseridos

### Semana 2: Obsidian ⚠️
- [ ] Criar template Professional.md
- [ ] Gerar 9 arquivos de profissionais
- [ ] Criar template Package.md
- [ ] Gerar 4 arquivos de pacotes
- [ ] Atualizar 4 arquivos de FAQs

### Semana 3: Painel Dashboard ⚠️
- [ ] Criar página /professionals
- [ ] Criar página /services
- [ ] Criar página /packages
- [ ] Atualizar página /intelligence

### Semana 4: Scripts de Sync ⚠️
- [ ] Criar obsidian_sync_daemon.py
- [ ] Criar API endpoints professionals
- [ ] Criar API endpoints services
- [ ] Testar sync bidirecional

---

## ✅ CHECKLIST GERAL DE SINCRONIZAÇÃO

### Dados Críticos:
- [ ] **Serviços:** Supabase ↔ Obsidian ↔ Painel
- [ ] **Profissionais:** Supabase ↔ Obsidian ↔ Painel
- [ ] **Clientes:** Supabase ↔ Obsidian ↔ Painel
- [ ] **Agendamentos:** Supabase ↔ Painel
- [ ] **FAQs:** Supabase ↔ Obsidian
- [ ] **Pacotes:** Supabase ↔ Obsidian ↔ Painel

### APIs:
- [ ] GET /api/professionals
- [ ] GET /api/professionals/{id}
- [ ] GET /api/services
- [ ] GET /api/services/{id}
- [ ] GET /api/packages
- [ ] GET /api/packages/{id}

### Scripts:
- [ ] seed_haven.py (executar)
- [ ] obsidian_sync_daemon.py (criar)
- [ ] sync_professionals_obsidian.py (criar)
- [ ] sync_packages_obsidian.py (criar)

### Painel:
- [ ] Página /professionals (criar)
- [ ] Página /services (criar)
- [ ] Página /packages (criar)
- [ ] Página /intelligence (atualizar)

---

## 🎯 STATUS FINAL ESPERADO

### Após Sincronização Completa:

| Sistema | Status | Dados Sincronizados |
|---------|--------|---------------------|
| **Supabase** | ✅ 100% | 64 registros knowledge + 758 clients + 204 journals |
| **Obsidian** | ✅ 100% | 41 services + 9 professionals + 758 clients + 204 journals |
| **Painel** | ✅ 100% | Todos dados via API REST |

### Sync Automático:
- ✅ Clientes: Horário (Supabase → Obsidian)
- ✅ Journals: Horário (Supabase → Obsidian)
- ✅ Profissionais: Diário (Supabase → Obsidian)
- ✅ Serviços: Semanal (Supabase → Obsidian)
- ✅ Todos: Real-time (Supabase → Painel via API)

---

**Documento Criado:** 2026-03-01  
**Próxima Ação:** Executar seed_haven.py (Semana 1)  
**Previsão de Conclusão:** 4 semanas
