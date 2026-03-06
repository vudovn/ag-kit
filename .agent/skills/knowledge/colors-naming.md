# 🎨 Color Naming Convention — LUNA OS

**Created:** 2026-02-27  
**Status:** 🔴 Active Discussion  
**Related:** `tailwind.config.js`

---

## Problema

O `tailwind.config.js` tem dualidade de nomes:

```js
colors: {
  bamboo: { 50-950 },  // Nome primário
  luna: { 50-900 }     // Alias (mesma cor)
}
```

No código, encontramos:
- `bg-luna-500` (comum)
- `bg-bamboo-500` (raro)
- `bg-primary` (inexistente)

---

## Impacto

1. **Confusão para devs novos**: Qual nome usar?
2. **Inconsistência**: Alguns arquivos usam `luna`, outros `bamboo`
3. **Manutenção**: Se mudarmos a cor, precisamos atualizar 2 lugares

---

## Soluções Consideradas

### Opção A: Manter Aliases (Recomendada)
```js
colors: {
  // Cor primária da marca
  brand: {
    50: '#f2f8f0',
    500: '#3d8c34',
    600: '#2e6f28',
    // ...
  },
  // Manter referências legadas
  bamboo: { /* mesma cor */ },
  luna: { /* mesma cor */ },
  // Semânticas
  success: { /* ... */ },
  warning: { /* ... */ },
  error: { /* ... */ },
}
```

**Prós:**
- ✅ Padrão claro (`brand` é o primário)
- ✅ Não quebra código existente (aliases)
- ✅ Adiciona cores semânticas

**Contras:**
- ⚠️ Ainda tem 3 nomes para mesma cor
- ⚠️ Requer documentação

---

### Opção B: Migrar Tudo para `bamboo`
```js
// Passos:
1. Adicionar `bamboo` como `primary` no tailwind.config.js
2. Buscar todos os usos de `luna-*` no código
3. Substituir por `primary-*` ou `bamboo-*`
4. Remover alias `luna`
```

**Prós:**
- ✅ Nome único (bamboo)
- ✅ Mais semântico (bamboo = bambu verde)

**Contras:**
- 🔴 Quebra código existente
- 🔴 Requer refatoração de todos os arquivos
- 🔴 Risco de bugs visuais

---

## Decisão

**Adotar Opção A (Manter Aliases com Padrão Claro)**

### Implementação

1. **Adicionar `brand` como cor primária**
2. **Manter `bamboo` e `luna` como aliases**
3. **Documentar em STYLEGUIDE.md**

```js
// tailwind.config.js
colors: {
  // Brand (primário)
  brand: {
    50: '#f2f8f0',
    100: '#e0f0db',
    200: '#bcddb4',
    300: '#8ec484',
    400: '#60a853',
    500: '#3d8c34',   // Main
    600: '#2e6f28',   // Hover
    700: '#245820',
    800: '#1b421a',
    900: '#102a0f',
    950: '#081508',
  },
  // Aliases (legado)
  bamboo: { /* ... */ },
  luna: { /* ... */ },
  // Semânticas
  success: { /* ... */ },
  warning: { /* ... */ },
  error: { /* ... */ },
  info: { /* ... */ },
}
```

---

## Guia de Uso

### ✅ Use
```tsx
// Componentes novos
className="bg-brand-500 text-white"
className="text-success-600"
className="border-error-200"

// Componentes legados (não quebrar)
className="bg-luna-500"  // OK, funciona
className="bg-bamboo-600"  // OK, funciona
```

### ❌ Evite
```tsx
// Inventar cores
className="bg-green-500"    // Não usa brand
className="bg-red-500"      // Não usa error
className="bg-amber-500"    // Não usa warning
```

---

## Próximos Passos

1. [ ] Atualizar `tailwind.config.js` com estrutura acima
2. [ ] Criar `STYLEGUIDE.md` com guia de cores
3. [ ] Adicionar lint rule para evitar `bg-red-*`, `bg-green-*`, etc.
4. [ ] Documentar em `/knowledge/colors-naming.md` (este arquivo)

---

**Referências:**
- [Tailwind Colors](https://tailwindcss.com/docs/customizing-colors)
- [WCAG Contrast Requirements](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
