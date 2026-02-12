# UX4G Government — Reference

## Component Registry (IDs and Categories)

Use these IDs with `ux4g_get_component` when using the MCP server. All markup should match the canonical snippets from the registry.

| ID | Name | Category | Requires JS |
|----|------|----------|--------------|
| button | Button | component | No |
| card | Card | component | No |
| modal | Modal | component | Yes |
| alert | Alert | component | No |
| badge | Badge | component | No |
| form | Form | form | No |
| table | Table | component | No |
| nav | Navigation | navigation | No |
| dropdown | Dropdown | component | Yes |
| carousel | Carousel | component | Yes |
| toast | Toast | component | Yes |
| progress | Progress | component | No |
| spinner | Spinner | component | No |
| container | Container | layout | No |
| grid | Grid | layout | No (needs ux4g-grid.css) |

**Button variants**: primary, secondary, success, danger, warning, info, outline-primary, outline-secondary, link.

**Form variants**: input (form-control), select (form-select), checkbox (form-check-input), radio (form-check-input).

**Table variants**: default, striped (table-striped), bordered (table-bordered), hover (table-hover).

**Nav variants**: tabs (nav-tabs), pills (nav-pills), navbar.

## Validation Issue Codes

When running `ux4g_validate_snippet`, issues may include:

| Code | Severity | Meaning | Fix |
|------|----------|---------|-----|
| EMPTY_CODE | error | No code provided | Provide snippet to validate. |
| PARSE_ERROR | error | Invalid HTML/JSX | Fix syntax. |
| MISSING_BUTTON_VARIANT | warning | Button has `btn` but no variant | Add e.g. `btn-primary` or `btn-secondary`. |
| MISSING_MODAL_ID | error | Modal element has no `id` | Add unique `id`; use it in trigger’s `data-bs-target`. |
| MISSING_FORM_CLASS | warning | Input/select/textarea without form class | Add `form-control` or `form-select`. |
| MISSING_LABEL | warning | Form control has `id` but no matching label | Add `<label for="...">` matching the control’s `id`. |
| MISSING_ALT_TEXT | warning | Image has no `alt` | Add descriptive `alt`. |
| ROW_WITHOUT_CONTAINER | warning | `row` not inside container | Wrap in `<div class="container">` or `container-fluid`. |

Resolve all **error**-severity issues before considering the snippet valid.

## Design Tokens (Token Types)

Use `ux4g_list_tokens` with optional `token_type` to list tokens. Types:

- **color** — Primary, secondary, success, danger, warning, info, light, dark; CSS variables and utility classes.
- **spacing** — Margin/padding scale (e.g. 0–5); classes like `m-3`, `p-2`, `py-5`.
- **typography** — Font sizes, weights, line heights; classes like `fw-bold`, `lead`, `display-4`.
- **breakpoint** — Responsive breakpoints (sm, md, lg, xl, xxl) for grid and utilities.
- **radius** — Border radius (e.g. rounded, rounded-lg).
- **other** — Miscellaneous tokens.

Use token values and CSS class names from the design system; do not invent new values.

## Canonical Markup Examples

### Button (primary)

```html
<button type="button" class="btn btn-primary">Button</button>
```

### Form group (input with label)

```html
<div class="mb-3">
  <label for="exampleInput" class="form-label">Label</label>
  <input type="text" class="form-control" id="exampleInput">
</div>
```

### Modal (structure)

```html
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">Modal body content</div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save</button>
      </div>
    </div>
  </div>
</div>
```

Trigger: `data-bs-toggle="modal" data-bs-target="#exampleModal"`. Page must load `ux4g.bundle.min.js`.

### Table (basic)

```html
<table class="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Header</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Data</td>
    </tr>
  </tbody>
</table>
```

### Nav (tabs)

```html
<ul class="nav nav-tabs">
  <li class="nav-item">
    <a class="nav-link active" aria-current="page" href="#">Active</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#">Link</a>
  </li>
</ul>
```

### Card (with body)

```html
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Card content</p>
  </div>
</div>
```

### Grid (two columns on md+)

```html
<div class="container">
  <div class="row">
    <div class="col-md-6">Column 1</div>
    <div class="col-md-6">Column 2</div>
  </div>
</div>
```

### Alert

```html
<div class="alert alert-primary" role="alert">Alert message</div>
```

### Progress bar

```html
<div class="progress">
  <div class="progress-bar" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">25%</div>
</div>
```

### Spinner (loading)

```html
<div class="spinner-border" role="status">
  <span class="visually-hidden">Loading...</span>
</div>
```

## Asset Paths (v2.0.8)

- CSS: `https://cdn.jsdelivr.net/npm/ux4g@2.0.8/dist/css/ux4g.min.css`
- Grid: `https://cdn.jsdelivr.net/npm/ux4g@2.0.8/dist/css/ux4g-grid.css`
- JS bundle: `https://cdn.jsdelivr.net/npm/ux4g@2.0.8/dist/js/ux4g.bundle.min.js`

For RTL or other builds, see the UX4G package on jsDelivr. Always pin version (e.g. 2.0.8) in production.
