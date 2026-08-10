# Learnwise API

Learnwise is a FastAPI service that receives SMS messages, sends them to an
LLM service, sends the generated answer back through an SMS provider, and
stores the conversation in a SQLAlchemy-managed database.

## Requirements

- Python 3.11 or newer
- A virtual environment
- SQLite for local development

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
```

## Environment Configuration

Create a local environment file:

```bash
cp .env.example .env
```

The default configuration is:

```env
LLM_SERVICE=mock
SMS_PROVIDER=mock
DATABASE_URL=sqlite:///./data/data.db
```

`DATABASE_URL` is a required SQLAlchemy database URL. The `.env` file is
ignored by Git and must not contain committed secrets. The available LLM and
SMS implementations are currently both `mock`.

## Database Migrations

```bash
alembic upgrade head
```

Generate a migration after changing the SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the change"
```

Review the generated file in `alembic/versions` before applying it. Roll back
the latest migration with:

```bash
alembic downgrade -1
```

## Running the API

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

## Testing the SMS Webhook Locally

With the API running, send a request to the webhook:

```bash
curl -X POST http://127.0.0.1:8000/v1/sms/ \
	-H "Content-Type: application/json" \
	-d '{
		"phoneNumber": "+36123456789",
		"body": "How do I reset my password?",
		"messageId": "SM123456789",
		"timestamp": "2026-07-27T12:00:00Z"
	}'
```

With the mock services, the conversation follows:

```text
received -> llmResponded -> completed
```

If message delivery fails, the final state becomes `error`. Invalid or
incomplete payloads return HTTP `422`.

## SMS Providers

### Mock provider

The mock provider is enabled by default:

```env
SMS_PROVIDER=mock
```

It returns `true` without making an external network request, making it useful
for local development and automated tests.

### Twilio

Twilio is not implemented yet. The provider abstraction and factory are ready
for it in:

- `app/services/sms/sms_provider_interface.py`
- `app/services/sms/sms_provider_factory.py`

A future Twilio provider should implement `send_sms(message, phone_number)`,
register the `twilio` factory type, and read credentials from environment
variables. A webhook adapter will also be needed because Twilio sends fields
such as `From`, `Body`, and `MessageSid`, while this API expects
`phoneNumber`, `body`, and `messageId`.

## Feedback Webhook

```bash
curl -X POST http://127.0.0.1:8000/v1/sms/feedback \
	-H "Content-Type: application/json" \
	-d '{
		"phoneNumber": "+36123456789",
		"feedback": "👍"
	}'
```

Accepted values are `👍` or `1` for positive feedback and `👎` or `0` for
negative feedback. The endpoint returns `true` when a conversation is updated
and `false` when none exists for the phone number.

## Admin Endpoints

The current admin endpoint is:

```text
GET /admin/conversations?phoneNumber=+36123456789
```

It currently returns the following placeholder:

```json
[{"status": "@TODO"}]
```

Filtering and authentication are planned improvements.

## Running Tests

Run the complete unit and integration suite:

```bash
pytest
```

The tests cover schemas, factories, SQLite persistence, storage services,
HTTP webhook flows, feedback, and Alembic migrations. They use isolated
in-memory databases and mocked external services.

To treat deprecation warnings as failures:

```bash
pytest -W error::DeprecationWarning
```

## Design Decisions

- **FastAPI** provides the HTTP layer and automatic OpenAPI documentation.
- **Pydantic schemas** are separate from SQLAlchemy ORM models.
- **SQLAlchemy and Alembic** provide persistence and versioned migrations.
- **SQLite** keeps local development simple and dependency-free.
- **Interfaces and factories** isolate replaceable LLM and SMS integrations.
- **The storage service** keeps controllers independent from ORM details.
- **Environment variables** keep database URLs and provider selection outside
	the source code.
- **Mock services** make local workflows deterministic and safe.

## Scope and Timebox

This implementation was completed within a focused four-hour timebox. The
priority was to deliver a coherent, testable end-to-end foundation rather
than to broaden the scope with partially implemented production integrations.

Within that time, the project includes:

- A FastAPI SMS webhook with conversation state transitions.
- Abstract interfaces and factories for LLM and SMS providers.
- Mock LLM and SMS providers for local development and testing.
- SQLAlchemy persistence with SQLite and Alembic migrations.
- Conversation feedback handling.
- Unit and integration tests covering the main workflow.
- Environment-based configuration and local setup documentation.

Production-grade third-party integrations, such as a complete Twilio
integration, require additional work around credentials, webhook validation,
provider-specific payloads, retries, delivery failures, and observability.
Likewise, a complete admin area would require authentication and authorization,
conversation filtering, pagination, auditability, and a defined operational
security model. Those areas were intentionally left as the next stage because
implementing them properly would extend beyond the available four-hour scope.

## Future Improvements

- Implement Twilio with signature validation and secure credentials.
- Add a Twilio payload adapter.
- Replace global controller dependencies with FastAPI dependency injection.
- Use request-scoped database sessions and stronger transaction boundaries.
- Implement admin listing, filtering, pagination, and authentication.
- Add structured error handling and reliable failure-state persistence.
- Add request authentication, rate limiting, and observability.
- Use enums for conversation status and feedback.
- Add PostgreSQL integration tests and CI checks for tests, migrations,
	linting, and type checking.
