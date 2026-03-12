# 🚀 Quick Reference

## Comandos Principais

### Buscar Skills
```bash
# Por termo
python3 brain/query_skills.py search "security"

# Por categoria  
python3 brain/query_skills.py category development

# Skill específica
python3 brain/query_skills.py skill architecture --content
```

### Neural Gateway
```bash
# Ver dashboard
python3 brain/runtime.py dashboard

# Analisar solicitação
python3 brain/runtime.py analyze --request "Criar API com JWT"

# Gateway interativo
./scripts/gateway-start.sh
```

### Atualizar Skills
```bash
python3 scripts/extract_skills.py
python3 scripts/integrate_skills.py
```

---

## Estrutura do Projeto

```
antigravity-kit/
├── docs/           # Documentação
├── brain/          # Cérebro de skills
├── scripts/        # Scripts utilitários
├── .agent/skills/  # Skills ativas
└── projects/       # Projetos
```

---

## Status

✅ Brain: 1.256 skills  
✅ Gateway: Sempre ativo  
✅ Scripts: Organizados  
✅ Docs: Consolidado

---

## Links

- **Docs:** `docs/BRAIN.md`
- **Status:** `docs/PROJECT_STATUS.md`
- **Organização:** `docs/ORGANIZATION_SUMMARY.md`
