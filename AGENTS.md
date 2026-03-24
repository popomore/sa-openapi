# AGENTS.md

Guidelines for AI agents working on this repository.

## Project Overview

`sa-openapi` is a Python SDK and CLI for the SensorsData Analytics (神策分析) OpenAPI.
It wraps four service groups — Dashboard, Channel, Dataset, Model — and exposes them as
both a typed Python client and a `sa-openapi` CLI command.

## Repository Layout

```
src/sa_openapi/
  __init__.py          # public exports
  client.py            # SensorsAnalyticsClient (sync, wraps async via background thread)
  async_client.py      # AsyncSensorsAnalyticsClient
  _auth.py             # injects api-key / sensorsdata-project headers
  _config.py           # ClientConfig + ConfigManager (~/.sa-openapi.toml)
  _transport.py        # AiohttpTransport — HTTP + error mapping
  _exceptions.py       # exception hierarchy
  models/              # Pydantic v2 models (one file per service group)
  services/            # async service classes (one file per service group)
  cli/                 # Click CLI (one file per service group + main.py, config.py, output.py)
docs/openapi/          # upstream OpenAPI JSON specs (source of truth for new endpoints)
tests/                 # pytest test suite
```

## Development Commands

```bash
# install dependencies
uv sync

# run tests
uv run pytest

# lint (must pass before committing)
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# auto-fix and format
uv run ruff check src/ tests/ --fix
uv run ruff format src/ tests/

# type-check
uv run mypy src/

# run all checks at once
uv run ruff check src/ tests/ && uv run ruff format --check src/ tests/ && uv run mypy src/ && uv run pytest

# CLI (dev)
uv run sa-openapi --help
```

## Adding a New API Endpoint

1. **Check the spec** — `docs/openapi/` contains the authoritative OpenAPI JSON files.
   Find the request/response schemas before writing any code.

2. **Add Pydantic models** in `src/sa_openapi/models/<service>.py`.
   - Use `Field(alias="camelCase")` for API fields that differ from Python naming.
   - Add `model_config = {"populate_by_name": True}` to every model.
   - Prefer `X | None` over `Optional[X]`.

3. **Add the async service method** in `src/sa_openapi/services/<service>.py`.
   - The method must be `async`.
   - Use `self._transport.post/get(...)` and parse `response.json()["data"]`.
   - `SensorsAnalyticsClient` (sync) automatically wraps every async method via `_SyncServiceProxy`.

4. **Add a CLI command** in `src/sa_openapi/cli/<service>.py`.
   - Use Click decorators; register the command on the existing group.
   - Help strings must use ASCII punctuation only (ruff RUF001 forbids fullwidth chars like `，（）`).
   - Support `--format [table|json]` at minimum.

5. **Run all checks** and fix any issues before committing.

## Code Style Rules

- Line length: **100** characters (`ruff` enforces this).
- Help strings in Click options: use **ASCII punctuation only** — no `，（）：` etc.
- Import order is managed by ruff (isort rules); run `ruff check --fix` after adding imports.
- Type annotations: remove unnecessary string quotes (`UP037`); use `X | Y` unions.
- Always run `ruff format` before committing — CI runs `ruff format --check` and will fail otherwise.

## Base URLs

| Service group           | Base path                        |
|-------------------------|----------------------------------|
| Dashboard / Channel / Dataset | `{base_url}/api/v3/analytics/v1` |
| Model                   | `{base_url}/api/v3/analytics/v1` |

Both paths are exposed as `config.dashboard_v1_base_url` and `config.model_v1_base_url`.

## Error Handling

`AiohttpTransport._handle_response` maps HTTP status codes and API `code` fields to
typed exceptions in `_exceptions.py`. Do not catch `Exception` broadly in service
methods — let transport exceptions propagate to the CLI layer.

## Testing

- Tests live in `tests/` and use `pytest`.
- Mock HTTP with `aioresponses`.
- Coverage target: **90%+** (CLI layer is excluded from coverage via `pyproject.toml`).
- Run `uv run pytest` to execute the full suite with coverage report.

## Configuration

The CLI reads `~/.sa-openapi.toml` (managed by `sa-openapi config init`).
Environment variables `SA_BASE_URL`, `SA_API_KEY`, `SA_PROJECT` override the file.
