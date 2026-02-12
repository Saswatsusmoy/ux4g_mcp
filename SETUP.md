# UX4G MCP Server Setup

## Quick Setup

Run these commands in your terminal:

```bash
cd /Users/saswatsusmoy/test/ux4g_mcp

# Install dependencies using your pyenv Python
/Users/saswatsusmoy/.pyenv/versions/3.12.9/bin/pip3 install -r requirements.txt

# Verify installation
/Users/saswatsusmoy/.pyenv/versions/3.12.9/bin/python3 -c "from ux4g_mcp.server import main; print('✓ Server ready')"
```

## Verify MCP Configuration

The server **must** be run as a module (`python -m ux4g_mcp`), not by executing `server.py` directly, because it uses relative imports. Using `server.py` as the entrypoint causes connection failures in Cursor/Cursor CLI.

**Cursor IDE & Cursor CLI** both read MCP config from:

- **Global:** `~/.cursor/mcp.json`
- **Project (when this repo is the workspace):** `.cursor/mcp.json` in this repo (already included)

Your global Cursor MCP config (`~/.cursor/mcp.json`) should have:

```json
{
  "mcpServers": {
    "ux4g": {
      "command": "/path/to/python",
      "args": ["-m", "ux4g_mcp"],
      "cwd": "/path/to/ux4g_mcp"
    }
  }
}
```

Use the **full path** to the Python that has the project dependencies (e.g. `venv/bin/python` or your pyenv/python3), and set `cwd` to the repo root (the folder containing `ux4g_mcp/` and `requirements.txt`). Do **not** use `args`: `[".../server.py"]` — that will fail in Cursor.

## After Setup

1. **Restart Cursor completely** (quit and reopen)
2. The UX4G MCP tools should appear:
   - `ux4g_get_version`
   - `ux4g_list_components`
   - `ux4g_get_component`
   - `ux4g_generate_snippet`
   - `ux4g_refine_snippet`
   - `ux4g_validate_snippet`
   - `ux4g_list_tokens`

## Troubleshooting

If you see `ModuleNotFoundError` or Cursor/Cursor CLI can't connect:
- Run the server as a module: `args` must be `["-m", "ux4g_mcp"]`, not a path to `server.py`.
- Ensure dependencies are installed: `pip3 install -r requirements.txt` (in the repo root or in your venv).
- Ensure `cwd` in the config is the repo root (folder that contains `ux4g_mcp/`).

If you see Pydantic errors:
- Ensure Pydantic v2 is installed: `pip3 install "pydantic>=2,<3"`
- Reinstall MCP SDK: `pip3 install --upgrade mcp`
