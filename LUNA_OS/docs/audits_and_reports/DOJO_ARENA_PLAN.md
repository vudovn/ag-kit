# 🌙🥋 LUNA OS DOJO ARENA — Planejamento Soberano

**Data:** 26 de Fevereiro de 2026  
**Framework:** AGENT_FLOW.md + MCT Agent Factory  
**Status:** **PLANEJAMENTO COMPLETO** ✅

---

## 🎯 VISÃO GERAL

**O Que É O Dojo?**
```
O Dojo é uma ARENA DE TREINAMENTO onde a LUNA:
1. Recebe cenários de teste (personas, situações)
2. Processa em tempo real
3. Exibe resposta + metadados (intent, mood, urgency)
4. Permite ajuste fino de parâmetros
5. Salva resultados para evolução
```

**Por Que Dojo?**
```
ANTES (Sem Dojo):
- Testes manuais no WhatsApp
- Sem visibilidade de metadados
- Difícil reproduzir cenários
- Sem métricas de evolução

AGORA (Com Dojo):
- Cenários pré-definidos
- Metadados em tempo real
- Reprodutibilidade total
- Score de maturidade visível
```

---

## 🏗️ ARQUITETURA DO DOJO

### **1. Componentes Principais**

```
╔══════════════════════════════════════════════════════════════╗
║  LUNA OS DOJO ARENA                                        ║
╠════════════════════════════════════════════════════════════╣
║                                                             ║
║  ┌─────────────────┐     ┌─────────────────┐               ║
║  │  Frontend Dojo  │────▶│  Backend Dojo   │               ║
║  │  (React/Next)   │◀────│  (FastAPI)      │               ║
║  └─────────────────┘     └────────┬────────┘               ║
║                                   │                         ║
║                    ┌──────────────┴──────────────┐         ║
║                    │                             │         ║
║           ┌────────▼────────┐          ┌────────▼────────┐║
║           │  Brain Engine   │          │  Evolution API  │║
║           │  (Processa)     │          │  (Simula WhatsApp)║
║           └────────┬────────┘          └─────────────────┘║
║                    │                                       ║
║           ┌────────▼────────┐                             ║
║           │  Supabase       │                             ║
║           │  (Salva Logs)   │                             ║
║           └─────────────────┘                             ║
║                                                             ║
╚════════════════════════════════════════════════════════════╝
```

---

## 📁 ESTRUTURA DE ARQUIVOS

### **Backend (FastAPI)**

```
LUNA_OS/
├── backend/
│   ├── app/
│   │   ├── dojo/
│   │   │   ├── __init__.py
│   │   │   ├── scenarios.py      # Cenários pré-definidos
│   │   │   ├── personas.py       # Personas de clientes
│   │   │   ├── metrics.py        # Cálculo de métricas
│   │   │   └── api.py            # Endpoints Dojo
│   │   └── api/
│   │       └── dojo.py           # Router Dojo
```

### **Frontend (Next.js)**

```
LUNA_OS/
├── frontend/
│   └── app/
│       └── dojo/
│           ├── page.tsx          # Arena Principal
│           ├── scenarios.tsx     # Lista de Cenários
│           ├── metrics.tsx       # Dashboard de Métricas
│           └── components/
│               ├── ChatWindow.tsx
│               ├── MetadataPanel.tsx
│               └── ScenarioCard.tsx
```

---

## 🎭 PERSONAS DISPONÍVEIS (Exemplos)

### **Persona 1: Cliente Apressada**
```json
{
  "name": "Cliente Apressada",
  "mood": "hurry",
  "urgency": 5,
  "scenario": "Precisa de horário para HOJE",
  "sample_message": "Oi! Tem horário pra hoje agora? É urgente!",
  "expected_response": "Oferecer horários disponíveis hoje",
  "success_criteria": ["urgency_detected", "fast_response", "solution_offered"]
}
```

### **Persona 2: Cliente Sensível a Preço**
```json
{
  "name": "Cliente Sensível a Preço",
  "mood": "hesitant",
  "urgency": 2,
  "scenario": "Pergunta preço 3x antes de agendar",
  "sample_message": "Quanto custa? Tem desconto? É caro...",
  "expected_response": "Focar em valor, não preço. Oferecer pacote.",
  "success_criteria": ["value_proposition", "package_offered", "objection_handled"]
}
```

### **Persona 3: Cliente Insatisfeita**
```json
{
  "name": "Cliente Insatisfeita",
  "mood": "frustrated",
  "urgency": 4,
  "scenario": "Reclama de atendimento anterior",
  "sample_message": "Fiz as unhas aqui e descascou em 2 dias!",
  "expected_response": "Empatia + solução + handoff se necessário",
  "success_criteria": ["empathy_shown", "solution_offered", "handoff_if_needed"]
}
```

---

## 🥋 CENÁRIOS DE TREINO

### **Nível 1: Básico (Iniciante)**

| # | Cenário | Persona | Objetivo |
|---|---------|---------|----------|
| 1 | Saudação simples | Happy | Responder com calor humano |
| 2 | Pergunta de horário | Normal | Informar horário de funcionamento |
| 3 | Pergunta de localização | Normal | Enviar endereço + mapa |
| 4 | Pergunta de preço | Hesitant | Informar preço + valor |
| 5 | Agendamento simples | Happy | Coletar serviço + horário |

### **Nível 2: Intermediário**

| # | Cenário | Persona | Objetivo |
|---|---------|---------|----------|
| 6 | Múltiplos serviços | Happy | Upsell de pacote |
| 7 | Objeção de preço | Hesitant | Contornar objeção |
| 8 | Urgência alta | Hurry | Priorizar + acalmar |
| 9 | Dúvida técnica | Hesitant | Explicar + educar |
| 10 | Comparação com concorrente | Hesitant | Diferenciar + valor |

### **Nível 3: Avançado**

| # | Cenário | Persona | Objetivo |
|---|---------|---------|----------|
| 11 | Cliente insatisfeita | Frustrated | Empatia + solução |
| 12 | Pedido de reembolso | Frustrated | Política + handoff |
| 13 | Crítica nas redes sociais | Frustrated | Gerenciar crise |
| 14 | Pedido especial complexo | Happy | Criatividade + limites |
| 15 | Múltiplas objeções | Hesitant | Contornar todas |

---

## 📊 MÉTRICAS DO DOJO

### **Métricas em Tempo Real**

```typescript
interface DojoMetrics {
  // Resposta da LUNA
  response_time_ms: number;      // Tempo de resposta
  intent_detected: string;       // Intent classificada
  confidence_score: number;      // Confiança (0-1)
  
  // Inteligência de Negócio
  customer_mood: string;         // happy/frustrated/hurry/hesitant
  urgency_level: number;         // 1-5
  potential_value: string;       // high/medium/low
  objections_detected: string[]; // ['preco', 'horario']
  
  // Qualidade da Resposta
  empathy_score: number;         // 0-100
  clarity_score: number;         // 0-100
  actionability_score: number;   // 0-100
  
  // Resultado
  success: boolean;              // Cenário concluído?
  handoff_triggered: boolean;    // Handoff necessário?
  user_satisfaction: number;     // 1-5 (feedback humano)
}
```

### **Dashboard de Métricas**

```tsx
// frontend/app/dojo/page.tsx

<div className="grid grid-cols-4 gap-4">
  <MetricCard 
    title="Tempo de Resposta" 
    value={`${metrics.response_time_ms}ms`}
    trend={metrics.response_time_ms < 1000 ? 'up' : 'down'}
  />
  <MetricCard 
    title="Confiança" 
    value={`${(metrics.confidence_score * 100).toFixed(0)}%`}
    trend={metrics.confidence_score > 0.8 ? 'up' : 'down'}
  />
  <MetricCard 
    title="Empatia" 
    value={`${metrics.empathy_score}/100`}
    trend={metrics.empathy_score > 70 ? 'up' : 'down'}
  />
  <MetricCard 
    title="Sucesso" 
    value={metrics.success ? '✅' : '❌'}
    trend={metrics.success ? 'up' : 'down'}
  />
</div>
```

---

## 🔧 IMPLEMENTAÇÃO TÉCNICA

### **Backend: Endpoints Dojo**

```python
# backend/app/api/dojo.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.dojo.scenarios import get_scenarios, get_scenario_by_id
from app.dojo.personas import get_personas, get_persona_by_id
from app.core.brain import process_message
from app.core.evolution import calculate_maturity_score

router = APIRouter(prefix="/api/dojo", tags=["Dojo"])

class DojoRequest(BaseModel):
    scenario_id: Optional[str] = None
    persona_id: Optional[str] = None
    message: str
    phone: str = "5549999999999"  # Phone padrão para testes
    name: str = "Teste Dojo"

class DojoResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    processing_time_ms: int
    metrics: dict
    success: bool
    feedback: Optional[str] = None

@router.get("/scenarios")
async def list_scenarios(level: str = "all"):
    """Lista todos os cenários disponíveis."""
    return get_scenarios(level)

@router.get("/personas")
async def list_personas():
    """Lista todas as personas disponíveis."""
    return get_personas()

@router.post("/test", response_model=DojoResponse)
async def run_test(request: DojoRequest):
    """
    Executa um teste no Dojo.
    Processa mensagem e retorna resposta + métricas.
    """
    import time
    start_time = time.time()
    
    # Processar mensagem com Brain
    result = await process_message(
        phone=request.phone,
        name=request.name,
        message=request.message,
        history=[]
    )
    
    processing_time = (time.time() - start_time) * 1000
    
    # Calcular métricas
    metrics = {
        "response_time_ms": round(processing_time, 2),
        "intent_detected": result.get("intent"),
        "confidence_score": result.get("intent_confidence", 0),
        "customer_mood": result.get("sentiment", "neutral"),
        "urgency_level": 3,  # Extrair do intelligence
        "potential_value": "medium",
        "objections_detected": [],  # Extrair do intelligence
        "empathy_score": calculate_empathy(result.get("response", "")),
        "clarity_score": calculate_clarity(result.get("response", "")),
        "actionability_score": calculate_actionability(result.get("response", ""))
    }
    
    # Determinar sucesso
    success = determine_success(metrics, request.scenario_id)
    
    return DojoResponse(
        response=result.get("response", ""),
        intent=result.get("intent", "unknown"),
        confidence=result.get("intent_confidence", 0),
        processing_time_ms=round(processing_time, 2),
        metrics=metrics,
        success=success,
        feedback=None
    )

@router.post("/feedback")
async def submit_feedback(scenario_id: str, success: bool, rating: int, comment: str = ""):
    """Salva feedback humano para evolução."""
    from app.integrations.supabase_client import get_supabase
    db = get_supabase()
    
    db.table("dojo_feedback").insert({
        "scenario_id": scenario_id,
        "success": success,
        "rating": rating,  # 1-5
        "comment": comment,
        "created_at": "now()"
    }).execute()
    
    return {"status": "saved"}

@router.get("/metrics/summary")
async def get_dojo_summary():
    """Retorna resumo das métricas do Dojo."""
    from app.integrations.supabase_client import get_supabase
    db = get_supabase()
    
    # Buscar últimas 100 execuções
    results = db.table("dojo_feedback").select("*").order("created_at", desc=True).limit(100).execute()
    
    total = len(results.data)
    success_rate = sum(1 for r in results.data if r.get("success")) / total if total > 0 else 0
    avg_rating = sum(r.get("rating", 0) for r in results.data) / total if total > 0 else 0
    
    return {
        "total_tests": total,
        "success_rate": round(success_rate * 100, 1),
        "avg_rating": round(avg_rating, 2),
        "maturity_score": await calculate_maturity_score()
    }
```

---

### **Frontend: Arena Dojo**

```tsx
// frontend/app/dojo/page.tsx

"use client";

import { useState } from 'react';
import useSWR from 'swr';
import { Brain, Zap, Target, Smile, AlertCircle, CheckCircle } from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

export default function DojoArena() {
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
  const [selectedPersona, setSelectedPersona] = useState<string | null>(null);
  const [customMessage, setCustomMessage] = useState("");
  const [lastResult, setLastResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const { data: scenarios } = useSWR('/api/dojo/scenarios', fetcher);
  const { data: personas } = useSWR('/api/dojo/personas', fetcher);
  const { data: summary } = useSWR('/api/dojo/metrics/summary', fetcher);

  async function runTest() {
    setLoading(true);
    try {
      const res = await fetch('/api/dojo/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenario_id: selectedScenario,
          persona_id: selectedPersona,
          message: customMessage || "Test message"
        })
      });
      const result = await res.json();
      setLastResult(result);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  }

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[#F8FAFC]">
      <div className="max-w-7xl mx-auto space-y-8">

        {/* Header */}
        <div className="flex items-end justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="h-px w-8 bg-indigo-500" />
              <p className="text-[10px] font-black uppercase tracking-[0.2em] text-indigo-500">
                Training Arena
              </p>
            </div>
            <h1 className="text-4xl font-black text-gray-900 tracking-tighter">
              Dojo Arena 🥋
            </h1>
            <p className="text-gray-500 mt-2 text-sm font-medium">
              Teste a LUNA em cenários controlados
            </p>
          </div>

          {/* Summary Stats */}
          <div className="flex gap-4">
            <StatCard 
              title="Testes" 
              value={summary?.total_tests || 0} 
              icon={Target}
            />
            <StatCard 
              title="Sucesso" 
              value={`${summary?.success_rate || 0}%`} 
              icon={CheckCircle}
              trend={summary?.success_rate > 70 ? 'up' : 'down'}
            />
            <StatCard 
              title="Maturidade" 
              value={`${summary?.maturity_score?.score || 0}/100`} 
              icon={Brain}
            />
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

          {/* Left: Scenario Selection */}
          <div className="space-y-4">
            <h2 className="text-xl font-black text-gray-900">Cenários</h2>
            
            {scenarios?.map((scenario: any) => (
              <ScenarioCard
                key={scenario.id}
                scenario={scenario}
                selected={selectedScenario === scenario.id}
                onSelect={() => setSelectedScenario(scenario.id)}
              />
            ))}
          </div>

          {/* Right: Persona Selection */}
          <div className="space-y-4">
            <h2 className="text-xl font-black text-gray-900">Personas</h2>
            
            {personas?.map((persona: any) => (
              <PersonaCard
                key={persona.id}
                persona={persona}
                selected={selectedPersona === persona.id}
                onSelect={() => setSelectedPersona(persona.id)}
              />
            ))}
          </div>
        </div>

        {/* Test Area */}
        <div className="bg-white rounded-3xl p-8 border border-gray-200 shadow-sm">
          <h3 className="text-lg font-black mb-4">Área de Teste</h3>
          
          <textarea
            value={customMessage}
            onChange={(e) => setCustomMessage(e.target.value)}
            placeholder="Digite uma mensagem de teste ou use um cenário pré-definido..."
            className="w-full h-32 p-4 border border-gray-200 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          
          <button
            onClick={runTest}
            disabled={loading}
            className="mt-4 bg-indigo-600 text-white px-8 py-3 rounded-2xl font-bold hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2"
          >
            {loading ? (
              <>
                <Zap className="w-5 h-5 animate-spin" />
                Processando...
              </>
            ) : (
              <>
                <Brain className="w-5 h-5" />
                Executar Teste
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {lastResult && (
          <div className="bg-gray-900 rounded-3xl p-8 text-white">
            <h3 className="text-xl font-black mb-6">Resultado do Teste</h3>
            
            {/* Response */}
            <div className="mb-6">
              <p className="text-sm text-gray-400 mb-2">Resposta da LUNA:</p>
              <div className="bg-white/10 rounded-2xl p-4">
                {lastResult.response}
              </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-4 gap-4">
              <MetricDisplay 
                label="Tempo" 
                value={`${lastResult.processing_time_ms}ms`}
              />
              <MetricDisplay 
                label="Intent" 
                value={lastResult.intent}
              />
              <MetricDisplay 
                label="Confiança" 
                value={`${(lastResult.confidence * 100).toFixed(0)}%`}
              />
              <MetricDisplay 
                label="Sucesso" 
                value={lastResult.success ? '✅' : '❌'}
              />
            </div>

            {/* Detailed Metrics */}
            <div className="mt-6 grid grid-cols-3 gap-4">
              <MetricBar 
                label="Empatia" 
                value={lastResult.metrics.empathy_score} 
                max={100}
                color="bg-pink-500"
              />
              <MetricBar 
                label="Clareza" 
                value={lastResult.metrics.clarity_score} 
                max={100}
                color="bg-blue-500"
              />
              <MetricBar 
                label="Acionabilidade" 
                value={lastResult.metrics.actionability_score} 
                max={100}
                color="bg-green-500"
              />
            </div>

            {/* Feedback */}
            <div className="mt-6">
              <p className="text-sm text-gray-400 mb-2">Feedback:</p>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((rating) => (
                  <button
                    key={rating}
                    onClick={() => submitFeedback(lastResult.scenario_id, lastResult.success, rating)}
                    className="w-10 h-10 rounded-full bg-white/10 hover:bg-indigo-500 transition-all font-bold"
                  >
                    {rating}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, trend }: any) {
  return (
    <div className="bg-white rounded-2xl p-4 border border-gray-200 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center">
          <Icon className="w-5 h-5 text-indigo-600" />
        </div>
        <div>
          <p className="text-[10px] font-black text-gray-400 uppercase">{title}</p>
          <p className="text-xl font-black text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  );
}

function ScenarioCard({ scenario, selected, onSelect }: any) {
  return (
    <div
      onClick={onSelect}
      className={`p-4 rounded-2xl border-2 cursor-pointer transition-all ${
        selected 
          ? 'border-indigo-500 bg-indigo-50' 
          : 'border-gray-200 bg-white hover:border-indigo-300'
      }`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="font-bold text-gray-900">{scenario.name}</p>
          <p className="text-sm text-gray-500 mt-1">{scenario.description}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-bold ${
          scenario.level === 'beginner' ? 'bg-green-100 text-green-700' :
          scenario.level === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
          'bg-red-100 text-red-700'
        }`}>
          {scenario.level === 'beginner' ? 'Iniciante' :
           scenario.level === 'intermediate' ? 'Intermediário' :
           'Avançado'}
        </span>
      </div>
    </div>
  );
}

function PersonaCard({ persona, selected, onSelect }: any) {
  const moodEmojis: any = {
    happy: "😊",
    frustrated: "😤",
    hurry: "🔥",
    hesitant: "🤔"
  };

  return (
    <div
      onClick={onSelect}
      className={`p-4 rounded-2xl border-2 cursor-pointer transition-all ${
        selected 
          ? 'border-indigo-500 bg-indigo-50' 
          : 'border-gray-200 bg-white hover:border-indigo-300'
      }`}
    >
      <div className="flex items-center gap-3">
        <span className="text-3xl">{moodEmojis[persona.mood]}</span>
        <div className="flex-1">
          <p className="font-bold text-gray-900">{persona.name}</p>
          <p className="text-sm text-gray-500">{persona.description}</p>
        </div>
      </div>
    </div>
  );
}

function MetricDisplay({ label, value }: any) {
  return (
    <div className="bg-white/10 rounded-xl p-3 text-center">
      <p className="text-[10px] text-gray-400 uppercase">{label}</p>
      <p className="text-lg font-black">{value}</p>
    </div>
  );
}

function MetricBar({ label, value, max, color }: any) {
  const percentage = (value / max) * 100;
  
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-gray-400">{label}</span>
        <span className="font-bold">{value}/{max}</span>
      </div>
      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <div 
          className={`h-full ${color} transition-all`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

async function submitFeedback(scenarioId: string, success: boolean, rating: number) {
  await fetch('/api/dojo/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      scenario_id: scenarioId,
      success,
      rating,
      comment: ""
    })
  });
  alert("Feedback salvo! 🙏");
}
```

---

## 🗄️ SCHEMA SUPABASE

```sql
-- Dojo Feedback Table
CREATE TABLE IF NOT EXISTS public.dojo_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    scenario_id TEXT,
    persona_id TEXT,
    message TEXT,
    response TEXT,
    intent TEXT,
    confidence_score FLOAT,
    success BOOLEAN,
    rating INTEGER,  -- 1-5
    comment TEXT,
    metrics JSONB DEFAULT '{}'::jsonb
);

-- Indexes
CREATE INDEX idx_dojo_feedback_scenario ON dojo_feedback(scenario_id);
CREATE INDEX idx_dojo_feedback_created ON dojo_feedback(created_at);
CREATE INDEX idx_dojo_feedback_success ON dojo_feedback(success);
```

---

## 📋 ROADMAP DE IMPLEMENTAÇÃO

### **Fase 1: Core Dojo (4-6 horas)**

| Tarefa | Tempo | Prioridade |
|--------|-------|------------|
| Criar estrutura de pastas | 30min | 🔴 Alta |
| Implementar `scenarios.py` | 1h | 🔴 Alta |
| Implementar `personas.py` | 1h | 🔴 Alta |
| Criar endpoints API | 2h | 🔴 Alta |
| Frontend básico | 2h | 🔴 Alta |

### **Fase 2: Métricas (2-3 horas)**

| Tarefa | Tempo | Prioridade |
|--------|-------|------------|
| Calcular empathy_score | 1h | 🟡 Média |
| Calcular clarity_score | 30min | 🟡 Média |
| Calcular actionability_score | 30min | 🟡 Média |
| Dashboard de métricas | 1h | 🟡 Média |

### **Fase 3: Evolução (2-3 horas)**

| Tarefa | Tempo | Prioridade |
|--------|-------|------------|
| Salvar feedback no Supabase | 1h | 🟢 Baixa |
| Integrar com maturity_score | 1h | 🟢 Baixa |
| Exportar resultados | 1h | 🟢 Baixa |

---

## 🎯 CRITÉRIOS DE SUCESSO

### **Dojo Funcional Quando:**

- [ ] 15+ cenários disponíveis
- [ ] 5+ personas implementadas
- [ ] Métricas em tempo real
- [ ] Feedback humano salvo
- [ ] Maturidade atualiza após teste
- [ ] Dashboard mostra histórico

### **Qualidade Quando:**

- [ ] Success rate > 70%
- [ ] Avg rating > 4.0
- [ ] Response time < 2s
- [ ] Maturity score > 75

---

## 🌟 CONCLUSÃO

**O Dojo Arena é o próximo passo natural para:**

1. **Testar em controle** — Cenários reproduzíveis
2. **Ver em tempo real** — Metadados visíveis
3. **Evoluir com dados** — Feedback humano → aprendizado
4. **Medir maturidade** — Score visível de evolução

**"Não se treina um campeão no ringue. Treina no dojo."**

---

**🌙🥋 MCT OS — Dojo Arena: Onde a LUNA se torna soberana.**
