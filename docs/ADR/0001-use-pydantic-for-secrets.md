# ADR 0001 — Use Pydantic (pydantic-settings) to load secrets with SecretStr

- Date: 2025-09-04
- Status: Accepted
- Deciders: Bijo (repo owner)
- Related: [dotenv_config.py](../../src/orange_hrm/config/dotenv_config.py)
- Cross-References: ADR 0002 (JSON configs for non-secrets)
- Status History:
  - 2025-09-04: Proposed
  - 2025-09-04: Accepted
  - 2025-09-04: Implemented

## Context
Tests require credentials (username/password) for the OrangeHRM demo. We must avoid committing secrets to the repository and make it trivial for CI to inject secrets. We also want lightweight validation and consistent API to access secrets.

## Decision
Use `pydantic-settings` (`BaseSettings`) with `SecretStr` fields to load `ORANGEHRM_USERNAME` and `ORANGEHRM_PASSWORD`. Configure via `SettingsConfigDict(env_file='.env', case_sensitive=True, extra='ignore')`. Provide a single accessor function `get_dot_env_secrets()` cached with `@lru_cache(maxsize=1)`.

## Rationale
- `SecretStr` prevents accidental logging and makes intent explicit.
- `BaseSettings` already supports env vars and `.env` files, so minimal code and dependencies.
- Caching reduces repeated parsing and ensures one consistent config per test session.
- Pydantic validation fails fast if secrets are missing — prevents wasted test runs.

## Technical Constraints
- Must work in both local development and CI/CD environments
- No additional infrastructure dependencies for basic functionality
- Must integrate with existing pytest test framework
- Python 3.13+ compatibility requirement
- Windows 11 development environment support

## Alternatives considered
* Use plain `os.environ` + custom helper — cheaper but no validation, more boilerplate.
* Use a third-party secrets manager (HashiCorp Vault) — more secure but adds complexity and infra cost.
* Keep secrets in JSON (REJECT) — unacceptable for security.

## Success Metrics
- Zero accidental secret exposure in logs or error messages
- Test suite fails fast (< 5 seconds) when credentials are missing
- 100% test coverage for credential validation logic
- Zero security incidents related to credential handling
- Developer onboarding time reduced by clear .env.example template

## Consequences
- Tests will fail fast if secrets are missing (good).
- Slight runtime dependency on pydantic (acceptable).
- Everyone must follow `.env` + `.env.example` for local dev and CI secret injection.

## Reversion / Migration plan
If we later move to a vault, deprecate this ADR and add `000X-use-vault-for-secrets.md` explaining migration. Keep `get_dot_env_secrets()` as a thin adapter so swapping backends is easier.

## Implementation notes
- File: `src/orange_hrm/config/dotenv_config.py`
- Usage: `env_settings = get_dot_env_secrets(); env_settings.username.get_secret_value()`
