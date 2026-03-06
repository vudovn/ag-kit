# 🎨 WCAG Contrast Requirements — LUNA OS

**Created:** 2026-02-27  
**Status:** ✅ Actionable  
**Priority:** 🔴 High (Accessibility)

---

## Requisitos WCAG 2.1 AA

### Níveis de Contraste

| Tipo de Texto | Nível AA | Nível AAA |
|---------------|----------|-----------|
| Texto normal (<18px) | 4.5:1 | 7:1 |
| Texto grande (≥18px ou ≥14px bold) | 3:1 | 4.5:1 |
| UI Components (botões, inputs) | 3:1 | 3:1 |

---

## Cores Atuais (tailwind.config.js)

### Bamboo (Brand)
```
bamboo-500: #3d8c34
bamboo-600: #2e6f28
bamboo-700: #245820
```

**Testes de Contraste:**

| Combinação | Ratio | Status |
|------------|-------|--------|
| bamboo-500 em branco | 4.6:1 | ✅ AA Pass |
| bamboo-600 em branco | 6.2:1 | ✅ AA + AAA Pass |
| bamboo-700 em branco | 8.1:1 | ✅ AAA Pass |
| branco em bamboo-500 | 4.6:1 | ✅ AA Pass |

---

### Gray (Neutral) — PROBLEMA CRÍTICO

```
gray-300: #d4d4d8
gray-400: #a1a1aa  ← ❌ FAIL
gray-500: #71717a  ← ✅ OK
gray-600: #52525b  ← ✅ OK
gray-700: #3f3f46
```

**Testes de Contraste (em fundo branco #FFFFFF):**

| Cor | Ratio | Status |
|-----|-------|--------|
| gray-300 | 1.8:1 | ❌ Fail |
| gray-400 | 2.5:1 | ❌ Fail |
| gray-500 | 4.6:1 | ✅ AA Pass |
| gray-600 | 7.2:1 | ✅ AAA Pass |
| gray-700 | 9.5:1 | ✅ AAA Pass |

---

## Problemas Reais no Código

### 1. Dashboard (page.tsx)
```tsx
// ❌ FAIL: gray-400 (2.5:1)
<p className="text-gray-400 mt-2 text-sm font-medium">
  Fluxo em tempo real · <span className="text-luna-500">7 dias de dados</span>
</p>

// ✅ FIX: gray-500 (4.6:1) ou gray-600 (7.2:1)
<p className="text-gray-500 mt-2 text-sm font-medium">
```

**Impacto:** Usuários com baixa visão não conseguem ler subtítulos.

---

### 2. Sidebar (Sidebar.tsx)
```tsx
// ❌ FAIL: gray-500 em fundo transparente
<p className="text-[10px] text-gray-500 font-bold mt-1 uppercase">
  Protocolo Sync Ativo
</p>

// Contexto: Está em badge com bg-primary/5 (quase transparente)
// Contraste real: ~3.8:1 ❌

// ✅ FIX: Aumentar peso ou usar gray-700
<p className="text-[10px] text-gray-700 font-bold mt-1 uppercase">
```

---

### 3. Clientes (clients/page.tsx)
```tsx
// ❌ FAIL: Placeholder com gray-400
<input
  placeholder="Buscar cliente..."
  className="text-gray-400"
/>

// ✅ FIX
<input
  placeholder="Buscar cliente..."
  className="text-gray-600"
/>
```

---

### 4. Conversas (conversations/page.tsx)
```tsx
// ❌ FAIL: Múltiplos gray-400
<p className="text-gray-400 font-medium">
  {conv.client_phone}
</p>

<span className="text-gray-400">
  {timeAgo(conv.started_at)}
</span>

// ✅ FIX
<p className="text-gray-600 font-medium">
<span className="text-gray-500">
```

---

## Ferramentas de Validação

### Online
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Contrast Checker](https://contrast-checker.glitch.me/)

### CLI (Automatizar)
```bash
# Instalar
npm install -g @axe-core/cli

# Rodar auditoria
axe http://localhost:3000
```

### Lighthouse (DevTools)
```
1. Abrir Chrome DevTools
2. Ir em "Lighthouse"
3. Marcar "Accessibility"
4. Rodar auditoria
5. Verificar "Contrast" issues
```

---

## Regras para Novos Componentes

### ✅ Permitido
```tsx
// Texto normal (≥4.5:1)
text-gray-500   // 4.6:1 ✅
text-gray-600   // 7.2:1 ✅
text-gray-700   // 9.5:1 ✅
text-gray-900   // 15:1 ✅

// Texto em fundo colorido (verificar contraste)
bg-brand-500 text-white      // 4.6:1 ✅
bg-brand-600 text-white      // 6.2:1 ✅
bg-brand-700 text-white      // 8.1:1 ✅

// Fundo branco com texto brand
bg-white text-brand-700      // 8.1:1 ✅
```

### ❌ Proibido
```tsx
// Contraste insuficiente (<4.5:1)
text-gray-300   // 1.8:1 ❌
text-gray-400   // 2.5:1 ❌

// Texto fino em fundo colorido (verificar)
bg-brand-400 text-white      // 3.2:1 ❌ (texto normal)
bg-brand-400 text-white      // 3.2:1 ✅ (texto bold ≥18px)
```

---

## Checklist de Validação

Antes de mergar PR:

- [ ] Rodar Lighthouse Accessibility
- [ ] Verificar "Contrast" issues
- [ ] Testar com zoom 200%
- [ ] Testar em modo escuro (se aplicável)
- [ ] Testar com screen reader (VoiceOver/NVDA)

---

## Meta de Acessibilidade

| Métrica | Atual | Meta Semana 1 | Meta Semana 4 |
|---------|-------|---------------|---------------|
| Lighthouse Accessibility | ~55 | 75 | 90+ |
| Contrast Issues | ~15 | 5 | 0 |
| Keyboard Navigation | ~60% | 85% | 100% |

---

## Referências

- [WCAG 2.1 AA Guidelines](https://www.w3.org/WAI/WCAG21/quickref/?versions=2.1)
- [Understanding Success Criterion 1.4.3](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

---

**Action Items:**
1. [ ] Buscar todos os `text-gray-400` no código
2. [ ] Substituir por `text-gray-500` ou `text-gray-600`
3. [ ] Rodar Lighthouse após mudanças
4. [ ] Documentar em STYLEGUIDE.md
