# AGENTS.md

Python project managed with `uv`, pinned to Python 3.14.

## Stack
- Python 3.14 — pinned by `.python-version` (`3.14`); `pyproject.toml` sets `requires-python = ">=3.14"`.
- `uv` — env manager, dependency manager, and command runner.
- FastAPI + Uvicorn — the API server. No build backend, and no lint/format/typecheck tooling; `pytest` (dev dependency) for tests.

## Layout
- `main.py` — FastAPI app entry point: defines the app and runs Uvicorn on `0.0.0.0:8000` via `uv run main.py`.
- `tests/` — pytest test suite (currently `test_health.py`).
- `pyproject.toml` — project metadata: name `heaven-backend`, version `0.1.0`, readme `README.md`.
- `uv.lock` — lockfile; commit it.
- `.venv/` — virtual environment; gitignored (see `.gitignore`).
- `Dockerfile` — two-stage build on `ghcr.io/astral-sh/uv:python3.14-bookworm-slim`: deps installed via `uv sync --frozen --no-dev`, runs as non-root `appuser`, `uvicorn` entrypoint, `/health` healthcheck.
- `docker-compose.yml` — local dev/deploy stack; single `api` service on port `8000`, optional `.env` (see `.env.example`).
- `.dockerignore` — keeps VCS/caches/`.venv` out of the build context.
- `README.md` — project overview and API quickstart.

## Commands
Always run through `uv` (it resolves the pinned 3.14 interpreter), never a bare `python`:
- Run the API server: `uv run main.py` (serves on `http://0.0.0.0:8000`; docs at `/docs`, health at `/health`)
- Run the tests: `uv run pytest`
- Run a snippet: `uv run python -c "..."`
- Add a dependency: `uv add <pkg>`
- Add a dev dependency: `uv add --dev <pkg>`
- Remove a dependency: `uv remove <pkg>`
- Re-sync the env to `uv.lock`: `uv sync`
- Run the API in Docker: `docker compose up --build` (serves on `http://localhost:8000`)
- Build the image: `docker build -t heaven-backend .`

## Conventions / open questions
- Flat script layout (single `main.py`), not an installable package: no `src/` package, no `[build-system]`, no console entry point. If Heaven becomes a package/library, add a build backend (e.g. hatchling) and a `src/heaven/` layout.
- The Docker build relies on the virtual-project behavior above (`uv sync` installs dependencies only; `main.py` is copied in, not installed). The runtime image has no `uv` step — it runs `uvicorn` from the copied `.venv`.
- `pytest` is configured as a dev dependency with `[tool.pytest.ini_options]` (`testpaths = ["tests"]`, `pythonpath = ["."]`). No lint/format/typecheck tooling is configured — don't assume `ruff`/`mypy` exist; add them with `uv add --dev <tool>` and a matching `[tool.*]` section first.
- Remote is GitHub `nicolaslallier/Heaven-backend`; default branch `main`.
