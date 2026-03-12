# 🧪 LUNA OS - Test Suite

**Data:** 2026-03-11  
**Status:** ✅ Implementando

---

## 📋 O Que Vamos Testar

### Prioridade 1: Crítico
- [x] Health check da API
- [ ] Conexão com Supabase
- [ ] Conexão com Windmill
- [ ] Envio de WhatsApp (Evolution)

### Prioridade 2: Importante
- [ ] Criação de scripts
- [ ] Execução de flows
- [ ] Agendamentos

### Prioridade 3: Nice-to-have
- [ ] UI do frontend
- [ ] Integrações completas
- [ ] Performance

---

## 🚀 Como Rodar os Testes

```bash
# 1. Vá para o backend
cd backend

# 2. Rode todos os testes
python -m pytest tests/ -v

# 3. Rode testes específicos
python -m pytest tests/test_health.py -v
python -m pytest tests/test_integrations.py -v

# 4. Com coverage
python -m pytest tests/ --cov=app --cov-report=html
```

---

## 📊 Estrutura de Testes

```
backend/tests/
├── conftest.py              # Configuração dos testes
├── test_health.py           # Health checks
├── test_integrations.py     # Integrações (Supabase, Windmill)
├── test_windmill_client.py  # Cliente Windmill
├── test_automation.py       # Automações
└── fixtures/
    ├── sample_scripts.py    # Scripts de exemplo
    └── sample_flows.py      # Flows de exemplo
```

---

## ✅ Checklist de Validação

Antes de cada deploy:

```
[ ] Todos os testes passam
[ ] Health check retorna OK
[ ] Integrações principais funcionam
[ ] Logs não mostram erros críticos
```
