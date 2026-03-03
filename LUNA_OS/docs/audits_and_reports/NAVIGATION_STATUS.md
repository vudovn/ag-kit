# 🧭 Navegação LUNA OS - Páginas Disponíveis

**Data**: 2026-02-27  
**Status**: ✅ Sidebar Atualizado

---

## 📊 Páginas Existentes vs Menu

### ✅ Adicionadas ao Menu

#### Inteligência Operacional
| Página | Rota | Ícone | Badge | Status |
|--------|------|-------|-------|--------|
| Dashboard | `/` | LayoutDashboard | - | ✅ |
| Conversas | `/conversations` | MessageSquare | - | ✅ |
| Analytics | `/analytics` | BarChart3 | - | ✅ |
| Analytics + | `/analytics-super` | TrendingUp | `PRO` | ✅ |
| Clientes | `/clients` | Users | - | ✅ |
| Campanhas | `/campaigns` | Megaphone | - | ✅ |
| **Dojo Arena** | `/dojo` | Swords | `NOVO` | ✅ |
| Brain | `/brain` | Brain | - | ✅ |
| Knowledge | `/knowledge` | Sparkles | - | ✅ |
| Intelligence | `/intelligence` | Lightbulb | - | ✅ |
| Persona | `/persona` | UserCircle2 | - | ✅ |

#### Configuração Soberana
| Página | Rota | Ícone | Status |
|--------|------|-------|--------|
| WhatsApp | `/whatsapp` | Smartphone | ✅ |
| Conexões | `/connections` | Wifi | ✅ |
| Configurações | `/settings` | Settings | ✅ |

---

## 🎯 Estrutura do Menu

### Seção: Inteligência Operacional

```
📊 Dashboard
💬 Conversas
📈 Analytics
📈 Analytics + [PRO]
👥 Clientes
📢 Campanhas
⚔️ Dojo Arena [NOVO]
🧠 Brain
✨ Knowledge
💡 Intelligence
👤 Persona
```

### Seção: Configuração Soberana

```
📱 WhatsApp
📡 Conexões
⚙️ Configurações
```

---

## 🎨 Badges

| Badge | Cor | Uso |
|-------|-----|-----|
| `NOVO` | Pink → Purple | Dojo Arena (novo lançamento) |
| `PRO` | Pink → Purple | Analytics Super (features avançadas) |

---

## 📱 Ícones

Todos os ícones usam `lucide-react`:

```tsx
import {
  LayoutDashboard,      // Dashboard
  MessageSquare,        // Conversas
  BarChart3,            // Analytics
  TrendingUp,           // Analytics+
  Users,                // Clientes
  Megaphone,            // Campanhas
  Swords,               // Dojo Arena
  Brain,                // Brain
  Sparkles,             // Knowledge
  Lightbulb,            // Intelligence
  UserCircle2,          // Persona
  Smartphone,           // WhatsApp
  Wifi,                 // Conexões
  Settings,             // Configurações
} from 'lucide-react'
```

---

## 🔧 Como Adicionar Nova Página

1. **Criar pasta e arquivo**
   ```bash
   mkdir app/nova-pagina
   touch app/nova-pagina/page.tsx
   ```

2. **Adicionar ao menu** (Sidebar.tsx)
   ```tsx
   import { NewIcon } from 'lucide-react'

   const mainNav = [
     // ...
     { name: 'Nova Página', href: '/nova-pagina', icon: NewIcon },
   ]
   ```

3. **Adicionar badge (opcional)**
   ```tsx
   { name: 'Nova Página', href: '/nova-pagina', icon: NewIcon, badge: 'NOVO' }
   ```

---

## 🎯 URLs Completas

Assumindo `http://localhost:3001` como base:

| Página | URL Completa |
|--------|--------------|
| Dashboard | http://localhost:3001/ |
| Conversas | http://localhost:3001/conversations |
| Analytics | http://localhost:3001/analytics |
| Analytics + | http://localhost:3001/analytics-super |
| Clientes | http://localhost:3001/clients |
| Campanhas | http://localhost:3001/campaigns |
| Dojo Arena | http://localhost:3001/dojo |
| Brain | http://localhost:3001/brain |
| Knowledge | http://localhost:3001/knowledge |
| Intelligence | http://localhost:3001/intelligence |
| Persona | http://localhost:3001/persona |
| WhatsApp | http://localhost:3001/whatsapp |
| Conexões | http://localhost:3001/connections |
| Configurações | http://localhost:3001/settings |

---

## ✅ Checklist de Verificação

- [x] **Dojo Arena** adicionado ao menu
- [x] **Badge NOVO** no Dojo Arena
- [x] **Knowledge** adicionado ao menu
- [x] **Intelligence** adicionado ao menu
- [x] **Analytics Super** como "Analytics +" com badge PRO
- [x] **WhatsApp** movido para Configuração Soberana
- [x] **Conexões** renomeado de "API WhatsApp"
- [x] **Todos ícones** atualizados
- [x] **Badges** com gradiente pink → purple

---

## 🎨 Estilo dos Badges

```tsx
<span className="ml-auto px-2 py-0.5 
  bg-gradient-to-r from-pink-500 to-purple-500 
  text-white 
  text-[9px] 
  font-black 
  uppercase 
  tracking-wider 
  rounded-full 
  shadow-lg shadow-purple-500/30">
  {badge}
</span>
```

---

## 🚀 Próximas Melhorias

1. [ ] Adicionar tooltips nos ícones
2. [ ] Ordenar por frequência de uso
3. [ ] Adicionar atalhos de teclado
4. [ ] Menu de favoritos
5. [ ] Histórico de páginas recentes
6. [ ] Busca de páginas (Cmd+K)

---

**MCT OS v2.0 | Truth in Data | Haven Escovaria**

*Todos as páginas agora estão visíveis no menu!* 🎯
