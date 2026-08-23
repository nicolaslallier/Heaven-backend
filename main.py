import os
import time
from datetime import datetime, timezone
from typing import Literal

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
    status: Literal["ok"]
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


@app.get("/", response_model=HealthResponse, tags=["health"], include_in_schema=False)
def root() -> HealthResponse:
    """Root also reports service health."""
    return get_health()


def main() -> None:
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
