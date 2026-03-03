# 🌌 LUNA OS - Dashboard Executivo (Mega DB)

> **"Poder invisível, simplicidade visível."**

---

## 🏎️ Status da Operação
- **Última Atualização**: `$= dv.date('now').toLocaleString()`
- **Total de Clientes Ativos**: `$= dv.pages('"Clients"').length`
- **Conversas Registradas**: `$= dv.pages('"Journals"').length`
- **Itens de Inteligência**: `$= dv.pages('"Intelligence"').length`

---

## 🔥 Clientes VIP & Em Risco
> Clientes com alto "Lifetime Value" gerados pelo Supabase.

```dataview
TABLE phone as "Telefone", status as "Status", lifetime_value as "LTV (R$)", last_contact as "Último Contato"
FROM "Clients"
WHERE lifetime_value > 0 OR status = "risk"
SORT lifetime_value DESC
LIMIT 5
```

---

## 💬 Últimas Interações (Journals)
> Logs cronológicos do Cérebro Contínuo.

```dataview
TABLE client_phone as "Cliente", last_interaction as "Data da Conversa"
FROM "Journals"
SORT last_interaction DESC
LIMIT 5
```

---

## 🧠 Navegação Rápida
- [[000_MCT_MASTER_INDEX]] - Central de Dados
- [[Intelligence/Prompts/LUNA_SYSTEM_PROMPT|A Personalidade da LUNA]]

---
MCT OS v3.0 | [Suporte MCT](https://mycodingteam.com)
