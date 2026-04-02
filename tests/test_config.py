def test_settings_defaults(monkeypatch):
    monkeypatch.delenv("AIOPS_PORT", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    from aiopsx.config.settings import Settings
    s = Settings()
    assert s.gateway.port == 8000
    assert "sqlite" in s.database.url

def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("AIOPS_PORT", "9000")
    monkeypatch.setenv("DATABASE_URL", "postgresql://...")
    from aiopsx.config.settings import Settings
    s = Settings()
    assert s.gateway.port == 9000
    assert s.database.url == "postgresql://..."
