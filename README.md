# Heaven Backend

FastAPI service for Heaven.

## Quickstart

```sh
uv sync          # install dependencies
uv run main.py   # start the server on http://0.0.0.0:8000
```

## API

| Method | Path      | Description                          |
|--------|-----------|--------------------------------------|
| GET    | `/health` | Liveness/health check                |
| GET    | `/`       | Also reports service health          |

Interactive docs (Swagger UI) are available at `http://localhost:8000/docs`.

### Example

```sh
curl http://localhost:8000/health
```

```json
{
  "status": "ok",
  "service": "heaven",
  "version": "0.1.0",
  "uptime_seconds": 0.365,
  "timestamp": "2026-08-22T20:53:20.843503+00:00"
}
```
