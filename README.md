# UX4G MCP Server

An MCP (Model Context Protocol) server that provides comprehensive access to the UX4G design system, enabling AI code editors (Claude, Cursor, etc.) to generate UX4G-compliant UI components without manual reference to documentation.

## Features

- **Component Discovery**: List and query UX4G components with filtering
- **Code Generation**: Generate HTML/React code from natural language descriptions
- **Code Refinement**: Refine existing UX4G code based on change requests
- **Validation**: Validate code against UX4G design system rules
- **Design Tokens**: Access colors, spacing, typography, and breakpoint tokens
- **Framework Support**: Generate both plain HTML and React JSX

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure UX4G assets are in the `ux4g_2.0.8/` directory (already included)

## Usage

### Running the MCP Server

```bash
python -m ux4g_mcp.server
```

### MCP Tools

The server exposes the following tools:

- `ux4g.get_version` - Get UX4G version and asset information
- `ux4g.list_components` - List available components with optional filtering
- `ux4g.get_component` - Get detailed component information and markup
- `ux4g.generate_snippet` - Generate code from natural language description
- `ux4g.refine_snippet` - Refine existing code based on change request
- `ux4g.validate_snippet` - Validate code against UX4G rules
- `ux4g.list_tokens` - List design tokens (colors, spacing, typography, breakpoints)

### Configuration

Set environment variables to customize behavior:

- `UX4G_ASSET_ROOT` - Path to UX4G assets (default: `ux4g_2.0.8/`)
- `UX4G_DEFAULT_FRAMEWORK` - Default output framework: `html` or `react` (default: `html`)

## Architecture

- **Registry Layer**: Parses CSS/JS files and loads curated component metadata
- **Generation Layer**: Converts natural language to UX4G-compliant code
- **Validation Layer**: Validates code against design system rules
- **Template System**: Provides canonical markup skeletons for components

## Project Structure

```
ux4g_mcp/
├── ux4g_mcp/
│   ├── server.py          # MCP server entrypoint
│   ├── config.py          # Configuration
│   ├── registry/          # Component registry and parsing
│   ├── tools/             # MCP tool implementations
│   ├── generator/         # Code generation logic
│   └── metadata/          # Curated component definitions
├── ux4g_2.0.8/           # UX4G design system assets
└── requirements.txt       # Python dependencies
```

## License

MIT
