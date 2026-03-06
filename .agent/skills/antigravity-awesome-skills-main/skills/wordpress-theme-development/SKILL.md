---
name: wordpress-theme-development
description: "WordPress theme development workflow covering theme architecture, template hierarchy, custom post types, block editor support, and responsive design."
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# WordPress Theme Development Workflow

## Overview

Specialized workflow for creating custom WordPress themes from scratch, including modern block editor (Gutenberg) support, template hierarchy, and responsive design.

## When to Use This Workflow

Use this workflow when:
- Creating custom WordPress themes
- Converting designs to WordPress themes
- Adding block editor support
- Implementing custom post types
- Building child themes

## Workflow Phases

### Phase 1: Theme Setup

#### Skills to Invoke
- `app-builder` - Project scaffolding
- `frontend-developer` - Frontend development

#### Actions
1. Create theme directory structure
2. Set up style.css with theme header
3. Create functions.php
4. Configure theme support
5. Set up enqueue scripts/styles

#### Copy-Paste Prompts
```
Use @app-builder to scaffold a new WordPress theme project
```

### Phase 2: Template Hierarchy

#### Skills to Invoke
- `frontend-developer` - Template development

#### Actions
1. Create index.php (fallback template)
2. Implement header.php and footer.php
3. Create single.php for posts
4. Create page.php for pages
5. Add archive.php for archives
6. Implement search.php and 404.php

#### Copy-Paste Prompts
```
Use @frontend-developer to create WordPress template files
```

### Phase 3: Theme Functions

#### Skills to Invoke
- `backend-dev-guidelines` - Backend patterns

#### Actions
1. Register navigation menus
2. Add theme support (thumbnails, RSS, etc.)
3. Register widget areas
4. Create custom template tags
5. Implement helper functions

#### Copy-Paste Prompts
```
Use @backend-dev-guidelines to create theme functions
```

### Phase 4: Custom Post Types

#### Skills to Invoke
- `wordpress-penetration-testing` - WordPress patterns

#### Actions
1. Register custom post types
2. Create custom taxonomies
3. Add custom meta boxes
4. Implement custom fields
5. Create archive templates

#### Copy-Paste Prompts
```
Use @wordpress-penetration-testing to understand WordPress CPT patterns
```

### Phase 5: Block Editor Support

#### Skills to Invoke
- `frontend-developer` - Block development

#### Actions
1. Enable block editor support
2. Register custom blocks
3. Create block styles
4. Add block patterns
5. Configure block templates

#### Copy-Paste Prompts
```
Use @frontend-developer to create custom Gutenberg blocks
```

### Phase 6: Styling and Design

#### Skills to Invoke
- `frontend-design` - UI design
- `tailwind-patterns` - Tailwind CSS

#### Actions
1. Implement responsive design
2. Add CSS framework or custom styles
3. Create design system
4. Implement theme customizer
5. Add accessibility features

#### Copy-Paste Prompts
```
Use @frontend-design to create responsive theme design
```

### Phase 7: Testing

#### Skills to Invoke
- `playwright-skill` - Browser testing
- `webapp-testing` - Web app testing

#### Actions
1. Test across browsers
2. Verify responsive breakpoints
3. Test block editor
4. Check accessibility
5. Performance testing

#### Copy-Paste Prompts
```
Use @playwright-skill to test WordPress theme
```

## Theme Structure

```
theme-name/
├── style.css
├── functions.php
├── index.php
├── header.php
├── footer.php
├── sidebar.php
├── single.php
├── page.php
├── archive.php
├── search.php
├── 404.php
├── comments.php
├── template-parts/
├── inc/
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── languages/
```

## Quality Gates

- [ ] All templates working
- [ ] Block editor supported
- [ ] Responsive design verified
- [ ] Accessibility checked
- [ ] Performance optimized
- [ ] Cross-browser tested

## Related Workflow Bundles

- `wordpress` - WordPress development
- `wordpress-plugin-development` - Plugin development
- `wordpress-woocommerce` - WooCommerce
