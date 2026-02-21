import json

import ux4g_mcp.registry.builder as registry_builder


def _write_minimal_sources(tmp_path, description: str):
    metadata_dir = tmp_path / "metadata"
    cache_dir = tmp_path / "cache"
    css_dir = tmp_path / "css"
    js_dir = tmp_path / "js"

    metadata_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)

    (metadata_dir / "components.yaml").write_text(
        f"""
components:
  - id: button
    name: Button
    category: component
    description: "{description}"
    tags: [form, action]
    requires_js: false
    required_classes: [btn]
    default_markup_skeleton: |
      <button type="button" class="btn btn-primary">Button</button>
""".strip()
        + "\n",
        encoding="utf-8",
    )

    css_main = css_dir / "ux4g.css"
    css_grid = css_dir / "ux4g-grid.css"
    css_misc = css_dir / "ux4g-misc.css"
    js_main = js_dir / "ux4g.esm.js"

    css_main.write_text(
        ":root { --primary-color: #123456; }\n.btn { color: var(--primary-color); }\n",
        encoding="utf-8",
    )
    css_grid.write_text(
        "@media (min-width: 768px) { .row { display: flex; } }\n",
        encoding="utf-8",
    )
    css_misc.write_text("", encoding="utf-8")
    js_main.write_text("", encoding="utf-8")

    css_files = {
        "main": css_main,
        "utilities": css_misc,
        "grid": css_grid,
        "reboot": css_misc,
        "datetime": css_misc,
    }
    js_files = {
        "main": js_main,
        "bundle": js_main,
        "datetime": js_main,
        "chart": js_main,
        "map": js_main,
    }
    return metadata_dir, cache_dir, css_files, js_files


def _patch_registry_sources(monkeypatch, tmp_path, description: str):
    metadata_dir, cache_dir, css_files, js_files = _write_minimal_sources(
        tmp_path, description
    )
    monkeypatch.setattr(registry_builder, "METADATA_DIR", metadata_dir)
    monkeypatch.setattr(registry_builder, "CACHE_DIR", cache_dir)
    monkeypatch.setattr(registry_builder, "CSS_FILES", css_files)
    monkeypatch.setattr(registry_builder, "JS_FILES", js_files)
    return metadata_dir, cache_dir


def test_registry_cache_invalidates_when_metadata_changes(monkeypatch, tmp_path):
    metadata_dir, cache_dir = _patch_registry_sources(monkeypatch, tmp_path, "First")

    builder = registry_builder.RegistryBuilder()
    first_registry = builder.build(use_cache=True)
    assert first_registry.get_component("button").description == "First"

    cache_file = cache_dir / "registry_cache.json"
    first_cache = json.loads(cache_file.read_text(encoding="utf-8"))
    first_digest = first_cache["source_fingerprint"]["digest"]

    (metadata_dir / "components.yaml").write_text(
        (metadata_dir / "components.yaml")
        .read_text(encoding="utf-8")
        .replace('description: "First"', 'description: "Second"'),
        encoding="utf-8",
    )

    rebuilt = registry_builder.RegistryBuilder().build(use_cache=True)
    assert rebuilt.get_component("button").description == "Second"

    second_cache = json.loads(cache_file.read_text(encoding="utf-8"))
    second_digest = second_cache["source_fingerprint"]["digest"]
    assert first_digest != second_digest


def test_registry_force_rebuild_bypasses_cached_payload(monkeypatch, tmp_path):
    _, cache_dir = _patch_registry_sources(monkeypatch, tmp_path, "Source Truth")

    initial = registry_builder.RegistryBuilder().build(use_cache=True)
    assert initial.get_component("button").description == "Source Truth"

    cache_file = cache_dir / "registry_cache.json"
    cache_data = json.loads(cache_file.read_text(encoding="utf-8"))
    cache_data["components"]["button"]["description"] = "CORRUPTED_CACHE_VALUE"
    cache_file.write_text(json.dumps(cache_data, indent=2), encoding="utf-8")

    from_cache = registry_builder.RegistryBuilder().build(use_cache=True)
    assert from_cache.get_component("button").description == "CORRUPTED_CACHE_VALUE"

    rebuilt = registry_builder.RegistryBuilder().build(
        use_cache=True, force_rebuild=True
    )
    assert rebuilt.get_component("button").description == "Source Truth"


def test_get_registry_honors_env_force_rebuild_flag(monkeypatch, tmp_path):
    metadata_dir, _ = _patch_registry_sources(monkeypatch, tmp_path, "Before")
    original_registry_instance = registry_builder._registry_instance
    original_force_rebuild = registry_builder.FORCE_REBUILD_REGISTRY_CACHE

    try:
        registry_builder._registry_instance = None
        monkeypatch.setattr(registry_builder, "FORCE_REBUILD_REGISTRY_CACHE", False)
        initial = registry_builder.get_registry()
        assert initial.get_component("button").description == "Before"

        (metadata_dir / "components.yaml").write_text(
            (metadata_dir / "components.yaml")
            .read_text(encoding="utf-8")
            .replace('description: "Before"', 'description: "After"'),
            encoding="utf-8",
        )

        monkeypatch.setattr(registry_builder, "FORCE_REBUILD_REGISTRY_CACHE", True)
        rebuilt = registry_builder.get_registry()
        assert rebuilt.get_component("button").description == "After"
    finally:
        registry_builder._registry_instance = original_registry_instance
        monkeypatch.setattr(
            registry_builder, "FORCE_REBUILD_REGISTRY_CACHE", original_force_rebuild
        )
