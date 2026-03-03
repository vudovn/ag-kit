# 🌙 LUNA OS v2.1 — MELHORIAS SUGERIDAS (Roadmap Soberano)

**Data:** 26 de Fevereiro de 2026  
**Framework:** AGENT_FLOW.md — Evolução Contínua  
**Status Atual:** **Camada 6 IMPLEMENTADA (100/100)** ✅

---

## 📊 DIAGNÓSTICO ATUAL

| Camada | Score | Status |
|--------|-------|--------|
| Consciência (Brain) | 85/100 | ✅ Blindagem anti-alucinação |
| Memória (Memory) | 80/100 | ✅ Histórico + Contexto |
| Resiliência (Resilience) | 80/100 | ✅ Retry + Fallback |
| Conhecimento (Knowledge) | 75/100 | ✅ 37 serviços, 9 profissionais |
| **Evolução (Evolution)** | **10/100** | ⚠️ **Implementada, 0 interações** |

**SCORE GERAL: 66/100** ⚠️ **EM DESENVOLVIMENTO**

---

## 🎯 PRIORIDADE 1: ATIVAR CICLO DE EVOLUÇÃO (Semana 1)

### **1.1. Integrar Auditoria no Webhook** 🔴

**Problema:** EvolutionEngine existe, mas NÃO está sendo chamada no webhook.

**Solução:**
```python
# backend/app/api/webhooks.py

# IMPORTAR
from app.core.evolution import evolution_engine

# EM handle_message(), após processar resposta:
async def handle_message(remote_jid: str, push_name: str, text: str):
    # ... código existente ...
    
    result = await process_message(...)
    
    # ✅ NOVO: Auditoria em tempo real
    audit = await evolution_engine.audit_response(
        intent=result.get("intent"),
        response=result.get("response"),
        phone=remote_jid
    )
    
    # ✅ NOVO: Log evolução
    await evolution_engine.log_evolution(
        phone=remote_jid,
        intent=result.get("intent"),
        response=result.get("response"),
        audit_data=audit,
        conversation_id=conv_id
    )
```

**Impacto:** Cada mensagem gera aprendizado → maturidade sobe.

**Tempo:** 30 minutos

---

### **1.2. Criar Endpoint de Validação Humana** 🔴

**Problema:** Respostas com `audit_flag: needs_human_review` não têm fluxo de validação.

**Solução:**
```python
# backend/app/api/evolution.py (NOVO ENDPOINT)

@router.post("/validate/{log_id}")
async def validate_interaction(log_id: str, valid: bool, correction: str = None):
    """
    Humano valida resposta auditada.
    Se valid=true → reforça pattern
    Se valid=false + correction → atualiza knowledge
    """
    db = get_supabase()
    
    # Atualizar learning_log
    db.table("learning_log").update({
        "human_feedback": correction,
        "validated": valid,
        "validated_at": datetime.utcnow().isoformat()
    }).eq("id", log_id).execute()
    
    # Se correção, atualizar knowledge_base
    if correction and not valid:
        await knowledge_base.auto_update_from_correction(correction)
    
    return {"status": "validated"}
```

**Frontend:**
```tsx
// frontend/app/evolution/validate/page.tsx (NOVA PÁGINA)

// Lista respostas com audit_flag = "needs_human_review"
// Botões: ✅ Validar | ❌ Corrigir
```

**Impacto:** Feedback humano → aprendizado acelerado.

**Tempo:** 2-3 horas

---

### **1.3. Dashboard de Maturidade em Tempo Real** 🔴

**Problema:** KPI existe, mas mostra apenas "0/100, Aguardando...".

**Solução:**
```tsx
// frontend/app/page.tsx (ATUALIZAR KPI)

const { data: maturity } = useSWR('/api/evolution/maturity', fetcher, {
    refreshInterval: 10000 // 10 segundos
})

// Card de Maturidade (SUBSTITUIR)
<div className="glass-card">
    <h3 className="text-[10px] font-black text-emerald-500/60 uppercase tracking-[0.2em] mb-1">
        Maturidade Sōra
    </h3>
    
    {/* SCORE GRANDE */}
    <p className={`text-5xl font-black ${
        maturity?.score >= 75 ? 'text-green-500' : 
        maturity?.score >= 50 ? 'text-amber-500' : 'text-red-500'
    }`}>
        {maturity?.score ?? 0}/100
    </p>
    
    {/* BREAKDOWN */}
    {maturity?.breakdown && (
        <div className="mt-4 space-y-2">
            <div className="flex justify-between text-[10px]">
                <span className="text-green-500">✅ Validadas:</span>
                <span className="text-white">{maturity.breakdown.validated}</span>
            </div>
            <div className="flex justify-between text-[10px]">
                <span className="text-amber-500">⚠️ Incertas:</span>
                <span className="text-white">{maturity.breakdown.uncertain}</span>
            </div>
            <div className="flex justify-between text-[10px]">
                <span className="text-red-500">🚫 Flagged:</span>
                <span className="text-white">{maturity.breakdown.flagged}</span>
            </div>
        </div>
    )}
    
    {/* RECOMENDAÇÃO */}
    <p className={`text-[10px] font-black mt-3 uppercase tracking-widest ${
        maturity?.score >= 75 ? 'text-green-400' : 'text-slate-500'
    }`}>
        {maturity?.recommendation ?? 'Calculando...'}
    </p>
</div>
```

**Impacto:** Francisco vê evolução em tempo real.

**Tempo:** 1 hora

---

## 🎯 PRIORIDADE 2: AUTO-APRENDIZADO (Semana 2-3)

### **2.1. Auto-Atualização de Knowledge Base** 🟡

**Problema:** Knowledge_base é estática — não aprende com correções humanas.

**Solução:**
```python
# backend/app/core/evolution.py (NOVO MÉTODO)

async def auto_update_knowledge(self, intent: str, correction: str):
    """
    Se humano corrigiu resposta, atualiza knowledge_base automaticamente.
    """
    db = get_supabase()
    
    # Extrair padrão da correção
    # Ex: "Progressiva custa R$250, não R$150"
    price_match = re.search(r"R\$\s*(\d+)", correction)
    
    if price_match and intent == "preco":
        # Atualizar serviço com preço correto
        service = extract_service_name(correction)
        db.table("knowledge_base").upsert({
            "category": "services",
            "key": service,
            "data": {"price": int(price_match.group(1))},
            "source": "auto_learned",
            "learned_at": datetime.utcnow().isoformat()
        }).execute()
        
        logger.info(f"📚 Knowledge atualizado: {service} = R${price_match.group(1)}")
```

**Impacto:** Knowledge_base viva — aprende com cada correção.

**Tempo:** 3-4 horas

---

### **2.2. Sugestão Automática de FAQs** 🟡

**Problema:** Novas perguntas de clientes não viram FAQs automaticamente.

**Solução:**
```python
# backend/app/core/evolution.py (NOVO MÉTODO)

async def suggest_new_faq(self, question: str, answer: str, confidence: float):
    """
    Se mesma pergunta aparece 3x com resposta validada, sugere novo FAQ.
    """
    db = get_supabase()
    
    # Verificar se pergunta já existe
    existing = db.table("knowledge_base")\
        .select("*")\
        .eq("category", "faq")\
        .ilike("key", f"%{question}%")\
        .execute()
    
    if not existing.data:
        # Sugerir novo FAQ
        db.table("knowledge_base").insert({
            "category": "faq_suggestion",
            "key": question,
            "data": {"suggested_answer": answer, "occurrences": 1},
            "source": "auto_suggested"
        }).execute()
        
        # Notificar admin no dashboard
        logger.info(f"💡 Novo FAQ sugerido: {question}")
```

**Impacto:** FAQs surgem organicamente das conversas reais.

**Tempo:** 2-3 horas

---

### **2.3. Métricas de Evolução no Dashboard** 🟡

**Novos KPIs:**
```tsx
// frontend/app/evolution/page.tsx (NOVA PÁGINA)

// 1. Evolução do Score (Gráfico de Linha)
<LineChart data={maturityHistory}>
    <Line dataKey="score" stroke="#10b981" />
</LineChart>

// 2. Top Intenções Auditadas
<BarChart data={topIntents}>
    <Bar dataKey="count" fill="#3b82f6" />
</BarChart>

// 3. Taxa de Validação Humana
<PieChart data={validationRate}>
    <Pie dataKey="validated" fill="#10b981" />
    <Pie dataKey="rejected" fill="#ef4444" />
</PieChart>

// 4. Learning Log (Tabela)
<Table data={learningLogs}>
    <Column header="Data" field="created_at" />
    <Column header="Intent" field="intent" />
    <Column header="Flag" field="audit_flag" />
    <Column header="Score" field="confidence_score" />
    <Column header="Validado" field="human_feedback" />
</Table>
```

**Impacto:** Visibilidade total da evolução.

**Tempo:** 4-5 horas

---

## 🎯 PRIORIDADE 3: ATIVAÇÃO SOBERANA (Semana 4)

### **3.1. Gatilho Automático de Ativação** 🟢

**Problema:** Francisco precisa decidir manualmente quando ativar mode=active.

**Solução:**
```python
# backend/app/core/evolution.py (NOVO MÉTODO)

async def check_activation_readiness(self) -> Dict:
    """
    Verifica se maturidade > 75 e recomenda ativação automática.
    """
    maturity = await self.calculate_maturity_score()
    
    if maturity["score"] >= 75:
        # Enviar notificação para Francisco
        await send_notification(
            type="activation_ready",
            message=f"🌙 LUNA atingiu {maturity['score']}/100 de maturidade. PRONTO PARA ATIVAR!"
        )
        
        return {
            "ready": True,
            "recommendation": "✅ PRONTO PARA ATIVAR",
            "auto_activate_in": "24h (ou confirme agora)"
        }
    
    return {
        "ready": False,
        "recommendation": maturity["recommendation"]
    }
```

**Impacto:** Sistema diz quando está pronto, não humano adivinha.

**Tempo:** 1-2 horas

---

### **3.2. Mode=Active com Fallback Automático** 🟢

**Problema:** Ativar mode=active é binário (tudo ou nada).

**Solução:**
```python
# backend/app/api/webhooks.py (NOVA LÓGICA)

async def handle_message(remote_jid: str, push_name: str, text: str):
    # ... processar mensagem ...
    
    # Obter maturidade atual
    maturity = await evolution_engine.calculate_maturity_score()
    
    # Decisão dinâmica de resposta
    if maturity["score"] >= 75:
        # ✅ Resposta automática (mode=active)
        await evolution.send_text(remote_jid, result["response"])
        
    elif maturity["score"] >= 50:
        # ⚠️ Resposta com confirmação humana
        if audit["audit_flag"] == "validated":
            await evolution.send_text(remote_jid, result["response"])
        else:
            # Flag para humano revisar
            await notify_human_review(conv_id, result["response"])
            
    else:
        # 🔴 mode=observe (só registra)
        logger.info(f"🔇 Mode=observe: maturidade {maturity['score']}/100")
```

**Impacto:** Ativação gradual, não binária.

**Tempo:** 2-3 horas

---

## 🎯 PRIORIDADE 4: EVOLUÇÃO CONTÍNUA (Mês 2)

### **4.1. Personas Sugeridas Automaticamente** 🟢

**Problema:** Personas são criadas manualmente, não aprendem de conversas reais.

**Solução:**
```python
# backend/app/core/evolution.py (NOVO MÉTODO)

async def suggest_personas_from_conversations(self) -> List[Dict]:
    """
    Analisa últimas 100 conversas e sugere personas baseadas em padrões.
    """
    db = get_supabase()
    
    # Buscar últimas 100 conversas
    conversations = db.table("conversations")\
        .select("phone, intent, sentiment, messages(*)")\
        .order("created_at", desc=True)\
        .limit(100)\
        .execute()
    
    # Agrupar por padrão de comportamento
    patterns = {}
    for conv in conversations.data:
        # Ex: "Sempre pergunta preço 3x antes de agendar"
        if conv["messages"].count("preco") >= 3:
            pattern = "sensivel_preco"
            patterns[pattern] = patterns.get(pattern, 0) + 1
    
    # Sugerir personas
    suggestions = []
    for pattern, count in patterns.items():
        if count >= 5:  # Mínimo 5 ocorrências
            suggestions.append({
                "name": f"Cliente {pattern.replace('_', ' ')}",
                "triggers": get_triggers_for_pattern(pattern),
                "confidence": count / 100,
                "sample_count": count
            })
    
    return suggestions
```

**Impacto:** Personas emergem de dados reais, não de suposições.

**Tempo:** 4-5 horas

---

### **4.2. Alertas de Regressão** 🟢

**Problema:** Se maturidade cair, ninguém é notificado.

**Solução:**
```python
# backend/app/core/evolution.py (NOVO MÉTODO)

async def check_regression(self) -> Dict:
    """
    Detecta se maturidade caiu >10% em relação à média histórica.
    """
    db = get_supabase()
    
    # Buscar média dos últimos 7 dias
    history = db.table("evolution_maturity")\
        .select("score, created_at")\
        .gte("created_at", datetime.utcnow() - timedelta(days=7))\
        .execute()
    
    if not history.data:
        return {"regression": False}
    
    avg_score = sum(h["score"] for h in history.data) / len(history.data)
    current_score = (await self.calculate_maturity_score())["score"]
    
    if current_score < (avg_score - 10):
        # Alerta de regressão
        await send_alert(
            type="regression_detected",
            message=f"⚠️ Maturidade caiu de {avg_score:.1f} para {current_score}"
        )
        
        return {
            "regression": True,
            "previous_avg": avg_score,
            "current_score": current_score,
            "drop": avg_score - current_score
        }
    
    return {"regression": False}
```

**Impacto:** Problemas detectados antes de virar crise.

**Tempo:** 2-3 horas

---

### **4.3. Exportação de Learning Log** 🟢

**Problema:** Dados de aprendizado ficam presos no Supabase.

**Solução:**
```python
# backend/app/api/evolution.py (NOVO ENDPOINT)

@router.get("/export")
async def export_learning_log(format: str = "csv"):
    """
    Exporta learning_log para CSV/JSON para análise externa.
    """
    db = get_supabase()
    
    logs = db.table("learning_log")\
        .select("*")\
        .order("created_at", desc=True)\
        .execute()
    
    if format == "csv":
        return convert_to_csv(logs.data)
    else:
        return logs.data
```

**Impacto:** Dados podem ser analisados em BI, Excel, etc.

**Tempo:** 1 hora

---

## 📊 ROADMAP COMPLETO

| Prioridade | Melhoria | Tempo | Impacto | Dificuldade |
|------------|----------|-------|---------|-------------|
| **1.1** | Integrar auditoria no webhook | 30min | 🔴 Alto | 🟢 Baixa |
| **1.2** | Validação humana | 2-3h | 🔴 Alto | 🟡 Média |
| **1.3** | Dashboard maturidade | 1h | 🔴 Alto | 🟢 Baixa |
| **2.1** | Auto-update knowledge | 3-4h | 🟡 Médio | 🟡 Média |
| **2.2** | Sugestão de FAQs | 2-3h | 🟡 Médio | 🟡 Média |
| **2.3** | Métricas de evolução | 4-5h | 🟡 Médio | 🟠 Alta |
| **3.1** | Gatilho de ativação | 1-2h | 🟢 Baixo | 🟢 Baixa |
| **3.2** | Mode=active gradual | 2-3h | 🔴 Alto | 🟠 Alta |
| **4.1** | Personas auto | 4-5h | 🟢 Baixo | 🟠 Alta |
| **4.2** | Alertas regressão | 2-3h | 🟡 Médio | 🟡 Média |
| **4.3** | Exportação logs | 1h | 🟢 Baixo | 🟢 Baixa |

---

## 🎯 RECOMENDAÇÃO DE IMPLEMENTAÇÃO

### **Semana 1 (Ativar Evolução):**
```
✅ 1.1 Integrar auditoria no webhook (30min)
✅ 1.3 Dashboard maturidade (1h)
⏳ 1.2 Validação humana (2-3h)
```

**Resultado:** Ciclo de aprendizado ativado.

---

### **Semana 2-3 (Auto-Aprendizado):**
```
✅ 2.1 Auto-update knowledge (3-4h)
✅ 2.2 Sugestão de FAQs (2-3h)
✅ 2.3 Métricas de evolução (4-5h)
```

**Resultado:** Knowledge_base viva, aprende sozinha.

---

### **Semana 4 (Ativação Soberana):**
```
✅ 3.1 Gatilho de ativação (1-2h)
✅ 3.2 Mode=active gradual (2-3h)
```

**Resultado:** Ativação automática quando maturidade > 75.

---

### **Mês 2 (Evolução Contínua):**
```
✅ 4.1 Personas auto (4-5h)
✅ 4.2 Alertas regressão (2-3h)
✅ 4.3 Exportação logs (1h)
```

**Resultado:** Sistema auto-evolutivo completo.

---

## 🌟 CONCLUSÃO

**STATUS ATUAL:**
```
✅ Camada 6 IMPLEMENTADA (100/100)
⏳ Aguardando primeiras interações
⏳ Aguardando integração no webhook
```

**PRÓXIMO PASSO IMEDIATO:**
```
1. Integrar evolution.audit_response() no webhook (30min)
2. Atualizar dashboard com breakdown (1h)
3. Testar com mensagens reais
```

**VISÃO DE LONGO PRAZO:**
```
LUNA OS não é um sistema que você configura.
É um organismo que EVOLUI com cada interação.

Poder invisível, simplicidade visível.
```

---

**🌙 MCT OS — Evolução Contínua.**
