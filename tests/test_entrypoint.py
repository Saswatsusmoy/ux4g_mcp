import ux4g_mcp.__main__ as entrypoint


def test_console_entrypoint_runs_async_server_main(monkeypatch):
    called = {"value": False}

    async def fake_server_main():
        called["value"] = True

    monkeypatch.setattr(entrypoint, "server_main", fake_server_main)

    entrypoint.main()

    assert called["value"] is True
