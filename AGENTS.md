# AGENTS.md

Python project managed with `uv`, pinned to Python 3.14.

## Stack
- Python 3.14 — pinned by `.python-version` (`3.14`); `pyproject.toml` sets `requires-python = ">=3.14"`.
- `uv` — env manager, dependency manager, and command runner.
- FastAPI + Uvicorn — the API server. No build backend, and no test/lint/format/typecheck tooling.

## Layout
- `main.py` — FastAPI app entry point: defines the app and runs Uvicorn on `0.0.0.0:8000` via `uv run main.py`.
- `pyproject.toml` — project metadata: name `heaven-backend`, version `0.1.0`, readme `README.md`.
- `uv.lock` — lockfile; commit it.
- `.venv/` — virtual environment; gitignored (see `.gitignore`).
- `README.md` — project overview and API quickstart.

## Commands
Always run through `uv` (it resolves the pinned 3.14 interpreter), never a bare `python`:
- Run the API server: `uv run main.py` (serves on `http://0.0.0.0:8000`; docs at `/docs`, health at `/health`)
- Run a snippet: `uv run python -c "..."`
- Add a dependency: `uv add <pkg>`
- Add a dev dependency: `uv add --dev <pkg>`
- Remove a dependency: `uv remove <pkg>`
- Re-sync the env to `uv.lock`: `uv sync`

## Conventions / open questions
- Flat script layout (single `main.py`), not an installable package: no `src/` package, no `[build-system]`, no console entry point. If Heaven becomes a package/library, add a build backend (e.g. hatchling) and a `src/heaven/` layout.
- No test/lint/format/typecheck tooling is configured. Don't assume `pytest`/`ruff`/`mypy` exist — add them with `uv add --dev <tool>` and a matching `[tool.*]` section first.
- Remote is GitHub `nicolaslallier/Heaven`; default branch `main`.
