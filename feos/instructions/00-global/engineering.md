# L1 Global — Engineering Standards

## Code
- Prefer clarity over cleverness; small, single-purpose modules (target < 300 lines/file, < 40 lines/function).
- Follow the project's formatter and linter; never disable a rule inline without a comment `// feos-exception: <reason> <ticket>`.
- Dependency injection over static/global state. No hidden I/O in constructors.
- All external calls: timeouts, retries with jittered backoff where idempotent, structured error handling.
- Async/non-blocking I/O where the platform supports it.
- No dead code, commented-out code, or TODO without a `TK-###`.
- New dependencies require: licence check (OSI-approved, no strong copyleft unless approved), maintenance signal, and a line in the task evidence.

## APIs
- Contract first (OpenAPI 3.1 / AsyncAPI / GraphQL SDL) committed before implementation.
- Versioned (`/v1/`), errors as RFC 9457 Problem Details, correlation ID propagated (`traceparent`).
- Pagination, idempotency keys for unsafe retries, input validation at the boundary.

## Testing
- Test pyramid: unit (fast, isolated) > integration (real dependencies via containers/emulators) > E2E (critical journeys only).
- Line coverage ≥ `feos.config.yaml > quality.min_coverage` on changed code; every FR has ≥ 1 test tagged `@covers FR-###`.
- Include negative-path, boundary and authorisation tests for every endpoint.
- Tests must be deterministic: no sleeps, no real network to third parties, seeded randomness, frozen clocks.

## Observability
- Structured logs (JSON), OpenTelemetry traces and metrics; no PII/secrets in logs.
- Every service exposes health/readiness endpoints and emits RED metrics (rate, errors, duration).

## Version control
- Trunk-based, short-lived branches `feat/TK-###-slug`, Conventional Commits referencing `TK-###`.
- One task = one PR. PR template must be completed.
