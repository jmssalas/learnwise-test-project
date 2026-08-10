# learnwise-test-project

Python and FastAPI project scaffold.

## Setup

Create and activate a virtual environment, then install the project with its
development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
```

## Run the API

```bash
uvicorn app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>. Interactive OpenAPI
documentation is available at `/docs`, and the readiness endpoint is
available at `/health`.

## Test

```bash
pytest
```

## Database migrations

Apply pending SQLite migrations with:

```bash
alembic upgrade head
```

The database path defaults to `learnwise.db` and can be configured with
`DATABASE_URL`.

Generate a migration after changing the SQLAlchemy models with:

```bash
alembic revision --autogenerate -m "describe the change"
```

Review the generated file in `alembic/versions` and then apply it with
`alembic upgrade head`.
