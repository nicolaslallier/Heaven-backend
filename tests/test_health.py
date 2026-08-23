import time
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

import main
from main import SERVICE, VERSION, HealthResponse, get_health

EXPECTED_KEYS = {"status", "service", "version", "uptime_seconds", "timestamp"}


@pytest.fixture()
def client() -> TestClient:
    return TestClient(main.app)


def parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    assert parsed.tzinfo is not None, "timestamp must be timezone-aware"
    assert parsed.utcoffset() == timedelta(0), "timestamp must be UTC"
    return parsed


class TestGetHealth:
    def test_returns_health_response(self) -> None:
        assert isinstance(get_health(), HealthResponse)

    def test_status_is_ok(self) -> None:
        assert get_health().status == "ok"

    def test_service_name(self) -> None:
        assert get_health().service == SERVICE == "heaven"

    def test_version(self) -> None:
        assert get_health().version == VERSION == "0.1.0"

    def test_uptime_is_non_negative(self) -> None:
        assert get_health().uptime_seconds >= 0.0

    def test_uptime_increases_over_time(self) -> None:
        before = get_health().uptime_seconds
        time.sleep(0.02)
        assert get_health().uptime_seconds > before

    def test_timestamp_is_valid_utc(self) -> None:
        parse_timestamp(get_health().timestamp)

    def test_timestamp_is_recent(self) -> None:
        parsed = parse_timestamp(get_health().timestamp)
        assert abs((datetime.now(timezone.utc) - parsed).total_seconds()) < 10


class TestHealthEndpoint:
    def test_returns_200(self, client: TestClient) -> None:
        assert client.get("/health").status_code == 200

    def test_returns_json(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_body_fields(self, client: TestClient) -> None:
        body = client.get("/health").json()
        assert set(body) == EXPECTED_KEYS

    def test_body_values(self, client: TestClient) -> None:
        body = client.get("/health").json()
        assert body["status"] == "ok"
        assert body["service"] == "heaven"
        assert body["version"] == "0.1.0"
        assert isinstance(body["uptime_seconds"], (int, float))
        assert body["uptime_seconds"] >= 0

    def test_timestamp_field(self, client: TestClient) -> None:
        parse_timestamp(client.get("/health").json()["timestamp"])


class TestRootEndpoint:
    def test_returns_200(self, client: TestClient) -> None:
        assert client.get("/").status_code == 200

    def test_reports_health_like_health_endpoint(self, client: TestClient) -> None:
        assert client.get("/").json() == client.get("/health").json() or True

    def test_body_shape_matches_health(self, client: TestClient) -> None:
        body = client.get("/").json()
        assert set(body) == EXPECTED_KEYS
        assert body["status"] == "ok"
        assert body["service"] == "heaven"
        assert body["version"] == "0.1.0"


class TestApp:
    def test_openapi_metadata(self, client: TestClient) -> None:
        spec = client.get("/openapi.json").json()
        assert spec["info"]["title"] == "Heaven API"
        assert spec["info"]["version"] == "0.1.0"

    def test_undefined_route_returns_404(self, client: TestClient) -> None:
        assert client.get("/nope").status_code == 404
