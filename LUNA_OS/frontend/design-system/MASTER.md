# Design System: LUNA OS — Beauty & Spa

> Gerado por UI UX Pro Max Skill v2.0 Indústria: Beauty/Spa/Salon/Wellness

---

## Pattern

- **Nome:** Hero-Centric + Social Proof
- **CTA:** Above fold, repetido após testimonials
- **Seções:** Hero > Features > CTA

## Style

- **Nome:** Soft UI Evolution
- **Keywords:** Subtle depth, modern aesthetics, accessibility-focused, improved
  shadows, hybrid
- **Performance:** ⚡ Excellent
- **Acessibilidade:** ✓ WCAG AA+

## Colors

| Papel      | Hex       | Nome       |
| ---------- | --------- | ---------- |
| Primary    | `#EC4899` | Pink-500   |
| Secondary  | `#F9A8D4` | Pink-300   |
| CTA        | `#8B5CF6` | Violet-500 |
| Background | `#FDF2F8` | Pink-50    |
| Text       | `#831843` | Pink-900   |

> Soft pink + lavender luxury

## Typography

| Uso     | Font        | Peso    |
| ------- | ----------- | ------- |
| Heading | **Lora**    | 400-700 |
| Body    | **Raleway** | 300-700 |

**Mood:** calm, wellness, health, relaxing, natural, organic

```css
@import url("https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Raleway:wght@300;400;500;600;700&display=swap");
```

## Key Effects

- Improved shadows (softer than flat, clearer than neumorphism)
- Transitions 200-300ms
- Focus visible for keyboard nav
- WCAG AA/AAA

## Anti-Patterns (NUNCA USAR)

- ❌ Bright neon colors
- ❌ Harsh animations
- ❌ Dark mode (para salon/spa)
- ❌ AI purple/pink gradients genéricos

## Pre-Delivery Checklist

- [ ] No emojis as icons (use SVG: Heroicons/Lucide)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard nav
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px
