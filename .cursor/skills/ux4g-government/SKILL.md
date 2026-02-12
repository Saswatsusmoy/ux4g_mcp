---
name: ux4g-government
description: Build government and citizen-facing UIs using the UX4G design system (Government of India / NeGD). Use when creating or editing pages for government portals, department sites, schemes, forms, dashboards, or any UI that must follow UX4G components and utility-only styling. Ensures UX4G compliance (no custom CSS), accessibility, and correct component usage.
---

# UX4G Design System for Government

Build government portals and citizen-facing interfaces using **UX4G** (UX for Government), the official design system (doc.ux4g.gov.in, NeGD/MeitY). All UI must use **only** UX4G components and utility classes—no custom CSS.

## When to Apply This Skill

- User asks for government portal, department page, scheme page, or citizen service UI
- User mentions UX4G, government design system, or India government UI
- User is editing or generating HTML/React that should look like a government site
- User wants forms, modals, tables, navigation, or landing pages that follow a design system

## Core Rules (Non-Negotiable)

1. **No custom CSS** — No `<style>` blocks, no inline `style="..."`. Use only UX4G utility classes and components.
2. **Only UX4G classes** — Component classes (e.g. `btn`, `card`, `form-control`) and utility classes (e.g. `bg-success`, `py-5`, `mb-3`, `text-center`). No ad-hoc class names.
3. **Canonical markup** — Use the exact structure and classes from UX4G component definitions (e.g. modal with `modal`, `modal-dialog`, `modal-content`, `modal-header`, `modal-body`, `modal-footer`).
4. **Accessibility** — Labels for every form control (`form-label`, `for`/`id`), `alt` on images, semantic structure, ARIA where required (e.g. modals, toasts).
5. **Assets** — Pages must load UX4G CSS and JS (see Dependencies below).

## Dependencies (Include in Every Page)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ux4g@2.0.8/dist/css/ux4g.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ux4g@2.0.8/dist/css/ux4g-grid.css">
<!-- Before </body> for components that need JS (modal, dropdown, carousel, toast): -->
<script src="https://cdn.jsdelivr.net/npm/ux4g@2.0.8/dist/js/ux4g.bundle.min.js"></script>
```

Grid layout requires `ux4g-grid.css`. Interactive components (modal, dropdown, carousel, toast) require `ux4g.bundle.min.js`.

## Component Usage Summary

| Component   | Base class(es)     | Notes |
|------------|--------------------|--------|
| Button     | `btn` + variant    | Always add a variant: `btn-primary`, `btn-secondary`, `btn-success`, `btn-danger`, `btn-warning`, `btn-info`, or `btn-outline-*`, `btn-link`. |
| Card       | `card`, `card-body`, `card-title`, `card-text` | Optional: `card-header`, `card-footer`. |
| Modal      | `modal`, `modal-dialog`, `modal-content`, `modal-header`, `modal-body`, `modal-footer` | Requires `id`, `data-bs-toggle="modal"` on trigger; needs JS bundle. |
| Alert      | `alert` + `alert-primary` / `alert-success` / `alert-danger` / `alert-warning` / `alert-info` | Use `role="alert"`. |
| Form       | `form-label`, `form-control` (input/textarea), `form-select` (select), `form-check` / `form-check-input` (checkbox/radio) | Wrap in `mb-3` or similar; always pair label with control via `for`/`id`. |
| Table      | `table`; optional `table-striped`, `table-bordered`, `table-hover` | Use `<thead>`, `<tbody>`, `scope="col"` / `scope="row"`. |
| Nav        | `nav`, `nav-tabs` or `nav-pills` or `navbar`; `nav-item`, `nav-link` | For navbar: `navbar`, `navbar-expand-lg`, `container` inside. |
| Badge      | `badge` + `bg-primary` / `bg-success` / etc. | |
| Progress   | `progress`, `progress-bar` | Set `style="width: N%"` and `aria-valuenow`, `aria-valuemin`, `aria-valuemax`. |
| Spinner    | `spinner-border` or `spinner-grow` | Include `<span class="visually-hidden">Loading...</span>`. |
| Container  | `container` or `container-fluid` | Rows must be inside a container. |
| Grid       | `row`, `col-*` (e.g. `col-md-6`, `col-sm-12`) | Requires `ux4g-grid.css`. Use `row` only inside `container`/`container-fluid`. |

Dropdown, carousel, toast require JS; use `data-bs-toggle="dropdown"`, `data-bs-ride="carousel"`, etc. as per UX4G patterns. See [reference.md](reference.md) for full markup.

## Utility Classes (Use These for Layout and Styling)

- **Spacing**: `m-*`, `p-*`, `mt-*`, `mb-*`, `ms-*`, `me-*`, `py-*`, `px-*` (0–5), `g-*` (gap on row).
- **Background**: `bg-primary`, `bg-success`, `bg-light`, `bg-dark`, `bg-white`, etc.
- **Text**: `text-primary`, `text-success`, `text-muted`, `text-white`, `text-center`, `text-start`, `text-end`, `fw-bold`, `lead`, `display-4`, `display-5`, `fs-1`–`fs-6`.
- **Display/Flex**: `d-flex`, `d-block`, `d-none`, `flex-column`, `flex-row`, `align-items-center`, `justify-content-between`, `gap-*`.
- **Borders**: `border`, `border-top`, `border-success`, `border-3`, `shadow-sm`.
- **Sizing**: `w-100`, `h-100`.
- **Links**: `text-decoration-none`, `link-primary`, etc.
- **Visibility**: `visually-hidden` for screen-reader-only text.

Use only classes that exist in UX4G (no arbitrary values). Prefer semantic variants: e.g. `btn-success` for success actions, `alert-warning` for warnings.

## Government-Specific Conventions

- **Language**: Prefer `lang="en"` or appropriate `lang` on `<html>`. Use clear, simple language for citizens.
- **Titles**: Page title pattern: `{Section} | Government Portal` or `{Department} | Government of India`.
- **Footer**: Include department/ministry name and “Government of India” / “All Rights Reserved” where appropriate. Use `bg-dark text-white py-5`-style footers with `text-white-50` for secondary text.
- **Hero / CTAs**: Use `bg-success` or `bg-primary` for hero sections; pair with `btn btn-light` or `btn btn-outline-light` for contrast. “Apply for Benefits”, “Track Application”, “Helpline” are common CTA labels.
- **Sections**: Use `<section>` with `id` for in-page navigation (e.g. `#programs`, `#services`, `#contact`). Use `py-5` for section padding, `container` inside each section.
- **Cards for programs/schemes**: Use `card` with `card-body`, `badge bg-success` for status (e.g. ACTIVE), `card-title`, `card-text`, and a primary button (e.g. “Learn More”).
- **No external branding** — Do not introduce non-UX4G logos or styles; keep the look within the design system.

## Framework: HTML vs React

- **HTML**: Use `class="..."` and `for="..."` on labels.
- **React**: Use `className` and `htmlFor`. Convert any generated HTML to JSX when the project is React.

When generating code, choose HTML or React based on project context; do not mix attribute names.

## Validation Checklist (Before Delivering Code)

- [ ] No `<style>` or inline `style` attributes.
- [ ] Every `button` with `btn` has a variant (`btn-primary`, etc.).
- [ ] Every modal has an `id`; trigger has `data-bs-toggle="modal"` and `data-bs-target="#id"`.
- [ ] Every form input/select/textarea has `form-control` or `form-select` and an associated `<label>` with matching `for`/`id`.
- [ ] Every `img` has an `alt` attribute.
- [ ] Every `row` is inside `container` or `container-fluid`.
- [ ] Required UX4G CSS (and JS for interactive components) are included.

## Using MCP Tools (When UX4G MCP Server Is Available)

If the UX4G MCP server is configured, use these tools to stay compliant:

- **ux4g_list_components** — List components (optional filter: category, tag, requires_js). Use to discover IDs and snippets.
- **ux4g_get_component** — Get one component by ID with full snippet (HTML/React). Use this as the single source of truth for markup.
- **ux4g_generate_snippet** — Generate UX4G-compliant code from a natural language description (e.g. “form with email and submit button”). Prefer this for net-new UI.
- **ux4g_refine_snippet** — Refine existing snippet from a change request (e.g. “make buttons outline”).
- **ux4g_validate_snippet** — Validate code for UX4G rules and accessibility. Run after generating or editing.
- **ux4g_list_tokens** — List design tokens (colors, spacing, typography, breakpoints) for reference.
- **ux4g_get_version** — Confirm UX4G version and asset paths (e.g. 2.0.8).

When generating, always prefer snippets returned by `ux4g_get_component` or `ux4g_generate_snippet`; do not invent markup.

## Page-Level Patterns

- **Landing / department homepage**: Navbar (navbar, container, nav links) → Hero (bg-success/bg-primary, display heading, CTAs) → Stats row (col-* with numbers + labels) → Programs (cards in grid) → Services (cards or list) → Footer (bg-dark, multi-column, copyright). All sections use `container` and UX4G utilities only.
- **Form page**: Container → optional heading → `<form>` with `form-label` + `form-control`/`form-select`/`form-check` groups in `mb-3` → primary submit + secondary cancel buttons.
- **Data view**: Container → table with `table` (and optional `table-striped`/`table-hover`) or cards in a grid.

## Common Mistakes to Avoid

- Adding custom CSS or inline styles.
- Using `btn` without a variant class.
- Putting `row` outside `container`/`container-fluid`.
- Form controls without `form-control`/`form-select` or without associated labels.
- Modal without `id` or without including the JS bundle.
- Using non-UX4G class names (e.g. made-up color or spacing classes).
- Mixing React and HTML attribute names in the same file.

## Additional Reference

- Full component list, validation rules, and token types: [reference.md](reference.md)
