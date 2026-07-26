---
name: brand-identity-extractor
description: Extracts brand visual identity from URLs or images and generates comprehensive design specifications. Creates usage guides for landing pages, presentations, social media posts, and other contexts. Automatically generates a new skill with the brand name containing all design specifications.
---

# Brand Identity Extractor

Captures visual identity from a source (URL or image) and creates comprehensive design specifications and usage guides. Automatically generates a new skill with the brand name for future reference.

## When to Use This Skill

- User wants to extract visual identity from a website or image
- User needs design specifications for a brand
- User wants consistent design guidelines across different contexts
- User mentions "identidade visual", "brand identity", "design system", "visual guidelines"
- User wants to replicate or document a brand's visual style

## Required Input

1. **Source**: URL or image path
2. **Brand Name** (optional): If not provided, extract from the source

## How to Use

### Step 1: Capture Visual Elements

#### From URL:
1. Use browser to navigate to the URL
2. Take a screenshot of the main page
3. Analyze the page for visual elements

#### From Image:
1. View the image file
2. Extract visual elements from the image

### Step 2: Extract Visual Identity Components

Identify and document the following:

#### Colors
- **Primary Color**: Main brand color (hex, RGB, HSL)
- **Secondary Colors**: Supporting colors
- **Accent Colors**: Highlights and CTAs
- **Neutral Colors**: Text, backgrounds, borders
- **Gradients**: If used, document direction and color stops

#### Typography
- **Primary Font**: Headlines (name, weight, style)
- **Secondary Font**: Body text
- **Font Sizes**: Scale system (headings, body, captions)
- **Line Heights**: Spacing ratios
- **Letter Spacing**: If notable

#### Visual Elements
- **Logo**: Description and usage variations
- **Icons**: Style (outlined, filled, rounded)
- **Images**: Photography style, filters, overlays
- **Illustrations**: Style and characteristics
- **Shadows**: Box-shadow values
- **Border Radius**: Rounded corners values
- **Spacing**: Margin/padding scale

#### Brand Personality
- **Tone**: Modern, classic, playful, serious
- **Energy**: Bold, subtle, dynamic, calm
- **Target Audience**: Inferred from design choices

### Step 3: Generate Design Specifications

Create a comprehensive design system document with:

```markdown
# [Brand Name] Design System

## Color Palette

### Primary Colors
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Primary | #XXXXXX | rgb(X,X,X) | Main brand color, CTAs |

### Secondary Colors
...

## Typography

### Font Family
- Headlines: [Font Name]
- Body: [Font Name]

### Type Scale
| Name | Size | Weight | Line Height |
|------|------|--------|-------------|
| H1   | 48px | 700    | 1.2         |
...

## Spacing System
...

## Components
...
```

### Step 4: Generate Context-Specific Guidelines

Create usage guides for each context:

#### Landing Pages
- Hero section layout
- Section structure
- CTA button styles
- Image placement
- Mobile responsive considerations

#### Presentations
- Slide layouts
- Title slides
- Content slides
- Image slides
- Color usage in slides

#### Social Media Posts
- Post dimensions per platform
- Text overlay placement
- Logo placement
- Color combinations for posts
- Story templates

#### Other Contexts (as needed)
- Email templates
- Print materials
- Business cards
- Pitch decks

### Step 5: Create Brand Skill

Create a new skill in the global skills folder with the brand name:

**Location**: `~/.gemini/antigravity/skills/<brand-name>/`

**Structure**:
```
<brand-name>/
├── SKILL.md              # Main instructions
├── resources/
│   ├── colors.md         # Color specifications
│   ├── typography.md     # Typography guide
│   └── components.md     # Component styles
└── contexts/
    ├── landing-pages.md  # Landing page guidelines
    ├── presentations.md  # Presentation guidelines
    └── social-media.md   # Social media guidelines
```

**SKILL.md Template for Brand**:

```markdown
---
name: <brand-name>
description: Design system and visual identity guidelines for [Brand Name]. Use when creating landing pages, presentations, social media posts, or any visual content for this brand.
---

# [Brand Name] Design System

This skill provides the visual identity guidelines for [Brand Name].

## When to Use

- Creating landing pages for [Brand Name]
- Designing presentations
- Creating social media content
- Building any visual asset for the brand

## Quick Reference

### Colors
- Primary: #XXXXXX
- Secondary: #XXXXXX
- Accent: #XXXXXX

### Typography
- Headlines: [Font] - [Weight]
- Body: [Font] - [Weight]

### Key Elements
- Border Radius: Xpx
- Shadow: [shadow value]
- Spacing Base: Xpx

## Resource Files

See the `resources/` folder for detailed specifications:
- `colors.md` - Full color palette
- `typography.md` - Typography system
- `components.md` - Component styles

## Context Guidelines

See the `contexts/` folder for specific usage:
- `landing-pages.md` - Landing page design
- `presentations.md` - Slide design
- `social-media.md` - Social post design
```

### Step 6: Determine Brand Name

If the user doesn't provide a brand name:

1. **From URL**: Look for:
   - Page title
   - Logo text
   - Meta title/description
   - Domain name (last resort)

2. **From Image**: Look for:
   - Text in the image
   - Logo text
   - File name context

3. **Ask User**: If unclear, ask for confirmation

**Brand Name Formatting**:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Example: "My Awesome Brand" → `my-awesome-brand`

## Best Practices

1. **Be Thorough**: Capture all visual elements, even subtle ones
2. **Be Precise**: Use exact values (hex codes, pixel values)
3. **Be Practical**: Include actual CSS/code snippets when helpful
4. **Be Contextual**: Explain when and why to use each element
5. **Include Examples**: Show before/after or good/bad examples

## Output Checklist

Before completing, verify:

- [ ] All colors extracted with hex values
- [ ] Typography identified with fallbacks
- [ ] Spacing system documented
- [ ] Component styles captured
- [ ] Landing page guidelines created
- [ ] Presentation guidelines created
- [ ] Social media guidelines created
- [ ] Brand skill created with proper structure
- [ ] Brand name confirmed or extracted
- [ ] All resource files created

## Example Workflow

**User**: "Capture a identidade visual do site example.com"

1. Navigate to example.com
2. Take screenshot
3. Analyze visual elements
4. Extract colors: Primary #3B82F6, Secondary #10B981...
5. Identify fonts: Inter for headlines, Roboto for body...
6. Document spacing, shadows, borders...
7. Create design system document
8. Generate landing page guidelines
9. Generate presentation guidelines
10. Generate social media guidelines
11. Extract brand name from page: "Example Corp" → `example-corp`
12. Create skill at `~/.gemini/antigravity/skills/example-corp/`
13. Create all resource and context files
