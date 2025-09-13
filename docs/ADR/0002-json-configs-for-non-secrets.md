# ADR 0002 — Use environment-specific JSON files for non-secret settings

- Date: 2025-09-04
- Status: Accepted
- Deciders: Bijo (repo owner)
- Related: src/orange_hrm/config/dev.json, conftest.py
- Related: [dev.json](../../src/orange_hrm/config/dev.json) & [conftest.py](../../tests/conftest.py)
- Cross-References: ADR 0001 (Pydantic for secrets)
- Status History:
  - 2025-09-04: Proposed
  - 2025-09-04: Accepted
  - 2025-09-04: Implemented

## Context
We need a simple mechanism to change non-sensitive settings (timeouts, base URLs, thresholds) per environment (dev/staging/prod). Tests should be reproducible both locally and in CI.

## Decision
Keep non-secret settings in environment-specific JSON files in `src/orange_hrm/config/` and load them via `importlib.resources.read_text()` within a session-scoped pytest fixture selected by `--env` flag.

## Rationale
- JSON is human readable and language-agnostic.
- Package resources ensure values are available after packaging/install.
- Keeping secrets out of JSON avoids accidental leakage.

## Technical Constraints
- Must work with Python's built-in libraries (no additional parsing dependencies)
- Configuration must be packaged with the application using importlib.resources
- Must integrate seamlessly with pytest fixture system
- Environment selection via CLI argument (--env flag)
- Maintain separation of concerns with ADR 0001 (secrets vs non-secrets)

## Alternatives considered
* YAML files — similar but we'd add another dependency. JSON is fine and built-in.
* Single config file with sections — manageable but more error-prone if keys drift across envs.

## Success Metrics
- Configuration loading time < 100ms for any environment
- Zero configuration-related test failures due to missing keys
- 100% schema consistency across all environment JSON files
- Easy environment switching via single CLI parameter
- Clear separation between secret and non-secret configuration

## Consequences
- Must keep JSON shape consistent across envs; add schema tests.
- Changing keys requires updating code and tests consuming them.

## Implementation notes
- Files: `dev.json`, `staging.json`, `prod.json`
- Fixture: `json_env_config` in `conftest.py`
- Add test: `tests/test_config_schema.py` to assert top-level keys.
