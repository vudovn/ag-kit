# Débitos Técnicos — LUNA OS Frontend

**Gerado em:** Março de 2026
**Status do Build:** ✅ Aprovado (Next.js 14.1.0)
**Bundle Size Total:** ~84.2 kB (shared) + páginas estáticas

---

## 📊 Resumo Executivo

| Categoria           | Quantidade | Severidade | Prioridade |
| ------------------- | ---------- | ---------- | ---------- |
| Tipos `any`         | 45         | 🟡 Média   | P2         |
| Console logs        | 5          | 🟢 Baixa   | P3         |
| Componentes grandes | 3          | 🟡 Média   | P2         |
| Falta de testes     | ∞          | 🔴 Alta    | P1         |
| Dependências        | 0          | 🟢 OK      | -          |

---

## 🔴 Alta Prioridade (P1)

### 1. Ausência de Testes Automatizados

**Status:** ❌ Nenhum teste implementado

**Impacto:**
- Regressões não detectadas
- Refatorações arriscadas
- Deploy sem segurança

**Solução Sugerida:**
```bash
npm install -D @testing-library/react @testing-library/jest-dom jest @types/jest
```

**Estrutura recomendada:**
```
__tests__/
  components/
    Sidebar.test.tsx
    KPICard.test.tsx
  pages/
    Dashboard.test.tsx
    Brain.test.tsx
  utils/
    helpers.test.ts
```

**Estimativa:** 2-3 sprints para cobertura de 70%

---

## 🟡 Média Prioridade (P2)

### 2. Tipos `any` Espalhados

**Total:** 45 ocorrências

**Arquivos críticos:**

| Arquivo                           | Ocorrências | Impacto |
| --------------------------------- | ----------- | ------- |
| `app/dojo/page.tsx`               | 8           | 🟡      |
| `app/intelligence/page.tsx`       | 7           | 🟡      |
| `app/analytics-super/page.tsx`    | 7           | 🟡      |
| `app/clients/page.tsx`            | 4           | 🟡      |
| `app/services/page.tsx`           | 4           | 🟡      |
| `app/brain/page.tsx`              | 4           | 🟡      |

**Exemplos problemáticos:**

```tsx
// ❌ RUIM
const moodEmojis: any = { ... }
const levelColors: any = { ... }

// ✅ BOM
const moodEmojis: Record<string, { emoji: string; gradient: string; bg: string }> = { ... }
const levelColors: Record<string, { bg: string; text: string; border: string; gradient: string }> = { ... }
```

**Solução:**
1. Criar arquivo de tipos: `types/index.ts`
2. Definir interfaces para dados da API
3. Substituir gradualmente cada `any`

**Estimativa:** 4-6 horas de refatoração

---

### 3. Componentes Grandes (Monolíticos)

**Arquivos:**

| Componente         | Linhas | Ideal | Status |
| ------------------ | ------ | ----- | ------ |
| `app/brain/page.tsx`    | 846    | 300   | 🟡 Otimizado |
| `app/dojo/page.tsx`     | 780    | 300   | 🟡 Otimizado |
| `app/intelligence/page.tsx` | ~650   | 300   | 🔴 Pendente |
| `app/analytics-super/page.tsx` | ~400   | 300   | 🟡 Aceitável |

**Problemas:**
- Dificuldade de manutenção
- Testabilidade baixa
- Re-renders desnecessários

**Solução:** Extrair sub-componentes

```tsx
// Exemplo: Brain page
// Antes: 846 linhas em 1 arquivo
// Depois:
app/brain/
  ├── page.tsx (50 linhas - orquestração)
  ├── components/
  │   ├── ItemCard.tsx
  │   ├── AddItemForm.tsx
  │   ├── BusinessSection.tsx
  │   └── ChatSimulator.tsx
  └── hooks/
      └── useKnowledge.ts
```

**Estimativa:** 1-2 sprints para refatoração completa

---

### 4. Error Handling Inconsistente

**Localização:**
```tsx
// app/brain/page.tsx:181,265
} catch (e) { console.error(e) }

// app/dojo/page.tsx:133
console.error(e);

// app/conversations/page.tsx:233
console.error('Feedback error:', err)
```

**Problema:**
- Errors apenas logados, não tratados
- Usuário não vê feedback
- Dificuldade de debug em produção

**Solução:**
```tsx
// ❌ RUIM
catch (e) { console.error(e) }

// ✅ BOM
catch (e) {
  const error = e instanceof Error ? e : new Error('Unknown error')
  captureException(error) // Sentry
  toast.error('Falha ao salvar. Tente novamente.')
  // Re-throw se necessário
}
```

**Estimativa:** 2-3 horas

---

## 🟢 Baixa Prioridade (P3)

### 5. Console Logs em Produção

**Ocorrências:** 5 logs de erro

**Problema:**
- Poluição do console
- Possível vazamento de dados

**Solução:**
```tsx
// next.config.js
compiler: {
  removeConsole: process.env.NODE_ENV === 'production'
}
```

Já está configurado ✅, mas logs manuais ainda existem.

**Ação:** Remover ou substituir por sistema de logging estruturado.

---

### 6. Props sem Validação de Tipos

**Exemplos:**
```tsx
// app/settings/page.tsx:10
function Section({ icon: Icon, title, children }: { icon: any; title: string; children: React.ReactNode })

// app/analytics-super/page.tsx:27
function KPICard({ title, value, sub, icon: Icon, trend, color, delay = 0 }: any)
```

**Solução:**
```tsx
interface SectionProps {
  icon: React.ElementType
  title: string
  children: React.ReactNode
}

function Section({ icon: Icon, title, children }: SectionProps) { ... }
```

**Estimativa:** 1-2 horas

---

### 7. Dependências de Tipos não Instaladas

**Status:** TypeScript configurado com `strict: true` ✅

**Porém:**
- Sem ESLint configurado para tipos
- Sem `@typescript-eslint/eslint-plugin`

**Solução:**
```bash
npm install -D @typescript-eslint/eslint-plugin @typescript-eslint/parser
```

```js
// .eslintrc.json
{
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

**Estimativa:** 1 hora

---

## 📋 Plano de Ação

### Sprint 1-2: Fundamentos
- [ ] Configurar ESLint + TypeScript rules
- [ ] Criar sistema de tipos base (`types/index.ts`)
- [ ] Setup do Jest + Testing Library
- [ ] Remover console.logs

### Sprint 3-4: Refatoração
- [ ] Refatorar `intelligence/page.tsx`
- [ ] Substituir 20 tipos `any` críticos
- [ ] Implementar error handling estruturado
- [ ] Criar primeiros testes de componentes

### Sprint 5-6: Consolidação
- [ ] Refatorar componentes restantes
- [ ] Atingir 50% de code coverage
- [ ] Substituir todos `any` restantes
- [ ] Documentar padrões de código

---

## 🛠️ Ferramentas Sugeridas

| Ferramenta                  | Propósito                  | Prioridade |
| --------------------------- | -------------------------- | ---------- |
| ESLint + TypeScript         | Linting de tipos           | 🔴 Alta    |
| Jest + Testing Library      | Testes unitários           | 🔴 Alta    |
| Playwright                  | E2E tests                  | 🟡 Média   |
| Sentry                      | Error tracking             | 🟡 Média   |
| Storybook                   | Component documentation    | 🟢 Baixa   |
| Bundle Analyzer             | Monitorar bundle size      | 🟢 Baixa   |

---

## 📈 Métricas de Sucesso

| Meta                           | Atual     | Target (30d) | Target (90d) |
| ------------------------------ | --------- | ------------ | ------------ |
| Code coverage                  | 0%        | 30%          | 70%          |
| Tipos `any`                    | 45        | 20           | 0            |
| Componentes > 500 linhas       | 3         | 1            | 0            |
| Bugs em produção/mês           | Desconh.  | < 5          | < 2          |
| Tempo médio de review (PR)     | Desconh.  | < 1 dia      | < 4 horas    |

---

## ✅ Pontos Positivos

- ✅ Build passando sem errors
- ✅ TypeScript configurado com `strict: true`
- ✅ Next.js 14.1.0 (versão estável)
- ✅ Performance otimizada (memo, useMemo, useCallback)
- ✅ SWR configurado corretamente
- ✅ Bundle size dentro do esperado (~84kB shared)
- ✅ Sem dependências desatualizadas críticas

---

**Responsável:** Tech Lead
**Próxima Review:** 2 semanas
**Status:** 🟡 Atenção (débitos gerenciáveis)
