---
tags: [dashboard, metrics]
---
# 👑 Sovereign CRM Dashboard

Bem-vindo(a) ao Cérebro de Relacionamento da LUNA. Os dados aqui são sincronizados do Supabase gerando 100% de `Truth in Data` local para os Agentes de IA.

## 🚨 Clientes em Risco de Evasão (Status Atencioso)
Mostrando clientes cujo LTV é significativo mas não retornam há algum tempo.
```dataview
TABLE phone, last_contact, lifetime_value AS "LTV (R$)"
FROM "Clients"
WHERE status != "inactive" AND last_contact != null
SORT last_contact asc
LIMIT 10
```

## 💬 Últimas Interações (Journals)
Últimos logs transcritos pela LUNA e enviados para o Cérebro local.
```dataview
TABLE client_phone, last_interaction, file.mtime AS "Atualizado em"
FROM "Journals"
SORT last_interaction desc
LIMIT 10
```

## 🌟 Top Clientes (LTV)
```dataview
TABLE phone, lifetime_value AS "Investimento Vitalício", status
FROM "Clients"
WHERE lifetime_value > 0
SORT lifetime_value desc
LIMIT 5
```

---
*Linked to [[000_MCT_MASTER_INDEX]]*
