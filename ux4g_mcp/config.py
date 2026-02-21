"""Configuration for UX4G MCP Server."""

import os
from pathlib import Path
from typing import Literal


def _env_bool(name: str, default: bool = False) -> bool:
    """Parse truthy/falsey environment variable values."""
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


# Default paths
WORKSPACE_ROOT = Path(__file__).parent.parent
UX4G_ASSET_ROOT = WORKSPACE_ROOT / "ux4g_2.0.8"
UX4G_VERSION = "2.0.8"

# Allow override via environment variables
UX4G_ASSET_ROOT = Path(os.getenv("UX4G_ASSET_ROOT", str(UX4G_ASSET_ROOT))).resolve()

DEFAULT_FRAMEWORK: Literal["html", "react"] = os.getenv(
    "UX4G_DEFAULT_FRAMEWORK", "html"
)
FORCE_REBUILD_REGISTRY_CACHE = _env_bool("UX4G_FORCE_REBUILD", False)

# Paths to key assets
CSS_DIR = UX4G_ASSET_ROOT / "css"
JS_DIR = UX4G_ASSET_ROOT / "js"
FONTS_DIR = UX4G_ASSET_ROOT / "fonts"

# Key CSS files to parse
CSS_FILES = {
    "main": CSS_DIR / "ux4g.css",
    "utilities": CSS_DIR / "ux4g-utilities.css",
    "grid": CSS_DIR / "ux4g-grid.css",
    "reboot": CSS_DIR / "ux4g-reboot.css",
    "datetime": CSS_DIR / "ux4g-date-time.css",
}

# Key JS files to analyze
JS_FILES = {
    "main": JS_DIR / "ux4g.esm.js",
    "bundle": JS_DIR / "ux4g.bundle.js",
    "datetime": JS_DIR / "ux4g-date-time-1.js",
    "chart": JS_DIR / "ux4g-chart.js",
    "map": JS_DIR / "ux4g-map.js",
}

# Metadata directory (curated component definitions)
METADATA_DIR = Path(__file__).parent / "metadata"

# Template directory
TEMPLATE_DIR = Path(__file__).parent / "templates"

# Cache directory for parsed registry
CACHE_DIR = Path(__file__).parent / ".cache"
CACHE_DIR.mkdir(exist_ok=True)
