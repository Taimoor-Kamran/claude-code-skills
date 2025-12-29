---
name: pytest
description: Scaffold and manage pytest projects with tox integration. Use when users want to create new test projects, add test files, configure tox environments, run tests with coverage, or follow pytest best practices. Triggers on requests like "create a pytest project", "add tests", "set up tox", "run coverage", or any pytest/tox development task.
---

# Pytest with Tox

Scaffold and manage pytest projects using tox for multi-environment testing.

## Quick Start: New Project

```bash
python scripts/scaffold.py my-project --path /target/directory
```

Creates:
```
my-project/
├── pyproject.toml      # pytest + coverage config
├── tox.ini             # multi-env test runner
├── src/my_project/     # source code (src layout)
└── tests/
    ├── conftest.py     # shared fixtures
    ├── unit/
    └── integration/
```

## Tox Commands

| Task | Command |
|------|---------|
| Run all envs | `tox` |
| Specific Python | `tox -e py312` |
| With coverage | `tox -e coverage` |
| Lint check | `tox -e lint` |
| Parallel | `tox -p auto` |
| Pass pytest args | `tox -- -k test_name` |

## Adding Tests

### Test File Template
```python
import pytest

class TestFeature:
    def test_basic(self, sample_data):
        assert sample_data["key"] == "value"

    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
    ])
    def test_parametrized(self, input, expected):
        assert input * 2 == expected
```

### Adding Fixtures (conftest.py)
```python
@pytest.fixture
def api_client():
    client = create_client()
    yield client
    client.close()
```

## Running Tests

```bash
# Direct pytest
pytest                          # all tests
pytest tests/unit/              # specific directory
pytest -k "test_name"           # by name pattern
pytest -m "not slow"            # exclude markers
pytest --cov=src                # with coverage

# Via tox
tox                             # all environments
tox -e py312                    # single environment
tox -e coverage                 # coverage report
```

## References

- **Patterns**: See [references/patterns.md](references/patterns.md) for fixtures, parametrize, mocking, async tests
- **Tox Config**: See [references/tox-config.md](references/tox-config.md) for environment setup, CI integration
