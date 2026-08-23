import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture()
def client() -> TestClient:
    return TestClient(main.app)


def run_main(monkeypatch: pytest.MonkeyPatch) -> dict:
    calls: dict = {}

    def fake_run(app, **kwargs):
        calls["app"] = app
        calls.update(kwargs)

    monkeypatch.setattr(main.uvicorn, "run", fake_run)
    main.main()
    return calls


class TestMain:
    def test_uses_defaults(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("HOST", raising=False)
        monkeypatch.delenv("PORT", raising=False)
        calls = run_main(monkeypatch)
        assert calls["host"] == "0.0.0.0"
        assert calls["port"] == 8000

    def test_honors_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HOST", "127.0.0.1")
        monkeypatch.setenv("PORT", "9000")
        calls = run_main(monkeypatch)
        assert calls["host"] == "127.0.0.1"
        assert calls["port"] == 9000

    def test_port_is_int(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("PORT", "8080")
        calls = run_main(monkeypatch)
        assert isinstance(calls["port"], int)

    def test_passes_app(self, monkeypatch: pytest.MonkeyPatch) -> None:
        calls = run_main(monkeypatch)
        assert calls["app"] is main.app
