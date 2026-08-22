import time
from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

SERVICE = "heaven"
VERSION = "0.1.0"
START_TIME = time.monotonic()

app = FastAPI(
    title="Heaven API",
    description="Heaven backend API",
    version=VERSION,
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    uptime_seconds: float
    timestamp: str


def get_health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=SERVICE,
        version=VERSION,
        uptime_seconds=round(time.monotonic() - START_TIME, 3),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    """Liveness/health check endpoint."""
    return get_health()


@app.get("/", response_model=HealthResponse, tags=["health"])
def root() -> HealthResponse:
    """Root also reports service health."""
    return get_health()


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
