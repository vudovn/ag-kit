# 🎨 LUNA LUX Design System — Premium Gold & Dark

**Versão:** 1.0.0  
**Data:** 2026-03-12  
**Tema:** Premium Gold & Dark

---

## 🎨 **PALETA DE CORES**

### **Gold (Primária)**

| Cor | Hex | Uso |
|-----|-----|-----|
| Gold 50 | `#FDF9E6` | Fundos claros |
| Gold 100 | `#F9F1D0` | Highlights |
| Gold 200 | `#F4DF89` | Hover states |
| Gold 300 | `#E8CC5C` | Secondary |
| **Gold 400** | `#D4AF37` | **Premium Gold (Primary)** |
| Gold 500 | `#AA8C2C` | Deep Gold |
| Gold 600 | `#8B7324` | Active states |
| Gold 700 | `#6B5A1E` | Dark gold |
| Gold 800 | `#4A3F17` | Shadows |
| Gold 900 | `#2A2310` | Deep shadows |

### **Dark (Background)**

| Cor | Hex | Uso |
|-----|-----|-----|
| Dark 50 | `#2D2D2D` | Cards |
| Dark 100 | `#1F1F1F` | Surfaces |
| Dark 200 | `#1A1A1A` | Main bg |
| Dark 300 | `#141414` | Deep bg |
| **Dark 400** | `#0F0F0F` | **Pure Dark** |
| Dark 500 | `#0A0A0A` | Black |

### **Accent Colors**

| Cor | Hex | Uso |
|-----|-----|-----|
| Navy | `#1E3A5F` | Secondary accent |
| Burgundy | `#4A0E4E` | Premium accent |
| Emerald | `#043927` | Success deep |

### **Status Colors**

| Status | Light | Dark |
|--------|-------|------|
| Success | `#10B981` | `#059669` |
| Warning | `#F59E0B` | `#D97706` |
| Error | `#EF4444` | `#DC2626` |
| Info | `#3B82F6` | `#2563EB` |

---

## 🎯 **COMPONENTES**

### **Buttons**

```tsx
// Primary Gold Button
<button className="btn btn-primary">
  <Zap className="w-5 h-5" />
  <span>Ação Principal</span>
</button>

// Secondary Button
<button className="btn btn-secondary">
  <span>Ação Secundária</span>
</button>

// Ghost Button
<button className="btn btn-ghost">
  <span>Cancelar</span>
</button>
```

**Estados:**
- Hover: `transform: translateY(-2px)` + glow gold
- Active: `transform: translateY(0)`
- Disabled: `opacity: 0.5`

---

### **Cards**

```tsx
<div className="card group">
  <div className="card-header">
    <h3 className="card-title">
      <Brain className="w-6 h-6 text-gold" />
      <span>Título do Card</span>
    </h3>
  </div>
  <div className="card-body">
    Conteúdo do card
  </div>
</div>
```

**Efeitos:**
- Hover: `border-color: rgba(212, 175, 55, 0.3)` + `shadow-gold`
- Transform: `translateY(-4px)`

---

### **Badges**

```tsx
<span className="badge badge-gold">Gold</span>
<span className="badge badge-success">Success</span>
<span className="badge badge-warning">Warning</span>
<span className="badge badge-error">Error</span>
```

---

### **Inputs**

```tsx
<input 
  type="text" 
  className="input" 
  placeholder="Digite aqui..."
/>

<select className="input select">
  <option>Opção 1</option>
  <option>Opção 2</option>
</select>
```

**Focus:** `border-color: var(--gold-400)` + gold glow

---

## 🎬 **ANIMAÇÕES**

### **Pulse Gold**
```tsx
<div className="animate-pulse-gold">
  <Crown className="w-20 h-20 text-gold" />
</div>
```

### **Shimmer**
```tsx
<div className="animate-shimmer">
  Loading...
</div>
```

### **Glow**
```tsx
<div className="animate-glow">
  <Brain className="w-10 h-10 text-gold" />
</div>
```

---

## 📐 **SPACING**

| Nome | Valor | Uso |
|------|-------|-----|
| xs | `0.25rem` (4px) | Micro spacing |
| sm | `0.5rem` (8px) | Tight spacing |
| md | `1rem` (16px) | Base spacing |
| lg | `1.5rem` (24px) | Section spacing |
| xl | `2rem` (32px) | Large sections |
| 2xl | `3rem` (48px) | Hero sections |

---

## 🔤 **TYPOGRAPHY**

### **Fontes**

```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
```

### **Tamanhos**

| Nome | Tamanho | Peso | Uso |
|------|---------|------|-----|
| xs | `0.75rem` (12px) | 400 | Labels, badges |
| sm | `0.875rem` (14px) | 400 | Body text |
| base | `1rem` (16px) | 400 | Default |
| lg | `1.125rem` (18px) | 600 | Subtitles |
| xl | `1.25rem` (20px) | 600 | Card titles |
| 2xl | `1.5rem` (24px) | 700 | Section titles |
| 3xl | `1.875rem` (30px) | 700 | Page titles |

---

## 🎨 **GRADIENTS**

### **Gradient Gold**
```css
background: linear-gradient(135deg, #D4AF37 0%, #AA8C2C 100%);
```

### **Gradient Dark**
```css
background: linear-gradient(180deg, #1A1A1A 0%, #0F0F0F 100%);
```

### **Gradient Premium**
```css
background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 50%, #1A1A1A 100%);
```

### **Gradient Gold Dark**
```css
background: linear-gradient(135deg, #1A1A1A 0%, #D4AF37 50%, #1A1A1A 100%);
```

---

## 🌟 **SHADOWS**

### **Gold Shadows**
```css
--shadow-gold: 0 0 20px rgba(212, 175, 55, 0.3);
--shadow-gold-lg: 0 0 40px rgba(212, 175, 55, 0.4);
```

### **Standard Shadows**
```css
--shadow-sm: 0 1px 2px 0 rgba(212, 175, 55, 0.05);
--shadow-md: 0 4px 6px -1px rgba(212, 175, 55, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(212, 175, 55, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(212, 175, 55, 0.1);
```

---

## 📱 **RESPONSIVE**

### **Breakpoints**

| Nome | Min Width | Uso |
|------|-----------|-----|
| sm | 640px | Mobile landscape |
| md | 768px | Tablets |
| lg | 1024px | Laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large screens |

### **Mobile First**

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {/* Cards */}
</div>
```

---

## 🎯 **BEST PRACTICES**

### **1. Use Gold Sparingly**

```tsx
// ✅ Good - Accent only
<h1 className="text-gold">Título</h1>

// ❌ Bad - Too much gold
<div className="bg-gold text-gold">Everything gold</div>
```

### **2. Maintain Contrast**

```tsx
// ✅ Good - High contrast
<div className="bg-dark text-gold">Readable</div>

// ❌ Bad - Low contrast
<div className="bg-gold-dark text-gold">Hard to read</div>
```

### **3. Consistent Spacing**

```tsx
// ✅ Good - Consistent
<div className="gap-6 mb-8">
  <div className="p-6">Card 1</div>
  <div className="p-6">Card 2</div>
</div>

// ❌ Bad - Inconsistent
<div className="gap-4 mb-10">
  <div className="p-5">Card 1</div>
  <div className="p-7">Card 2</div>
</div>
```

---

## 🎨 **EXAMPLES**

### **Dashboard Card**

```tsx
<div className="card group">
  <div className="card-header">
    <h3 className="card-title">
      <Brain className="w-6 h-6 text-gold" />
      <span>Smart Caching</span>
    </h3>
    <CheckCircle className="w-6 h-6 text-success" />
  </div>
  <div className="space-y-2">
    <p className="text-3xl font-bold bg-gradient-gold bg-clip-text text-transparent">
      95.23%
    </p>
    <p className="text-gold-light text-sm">Hit Rate</p>
  </div>
</div>
```

### **Premium Button**

```tsx
<button className="btn btn-primary group">
  <Zap className="w-5 h-5 group-hover:rotate-12 transition-transform" />
  <span>Execute Action</span>
</button>
```

### **Status Badge**

```tsx
<span className="badge badge-gold">
  <CheckCircle className="w-3 h-3" />
  Verified
</span>
```

---

## 🔗 **FILES**

| File | Description |
|------|-------------|
| `design-system.css` | Complete CSS variables |
| `page.tsx` | Dashboard example |
| `handoffs/page.tsx` | Handoff Queue example |
| `dna-editor/page.tsx` | DNA Editor example |

---

**MCT LTDA 2026** | LUNA LUX Design System  
**Version:** 1.0.0  
**Theme:** Premium Gold & Dark
