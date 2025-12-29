# Tox Configuration Reference

## Basic tox.ini

```ini
[tox]
env_list = py310, py311, py312
isolated_build = true

[testenv]
deps = pytest>=8.0
commands = pytest {posargs}
```

## Common Environments

### Testing with Coverage
```ini
[testenv:coverage]
deps =
    pytest>=8.0
    pytest-cov>=4.0
commands =
    pytest --cov=src --cov-report=term-missing --cov-report=html {posargs}
```

### Linting
```ini
[testenv:lint]
skip_install = true
deps = ruff>=0.1.0
commands =
    ruff check src tests
    ruff format --check src tests
```

### Type Checking
```ini
[testenv:typecheck]
deps =
    mypy>=1.0
    types-requests
commands = mypy src
```

### Documentation
```ini
[testenv:docs]
deps =
    sphinx>=7.0
    sphinx-rtd-theme
commands = sphinx-build -b html docs docs/_build
```

## Tox Commands

| Command | Description |
|---------|-------------|
| `tox` | Run all environments |
| `tox -e py312` | Run specific environment |
| `tox -e py310,py311` | Run multiple environments |
| `tox -p auto` | Run in parallel |
| `tox --recreate` | Recreate virtualenvs |
| `tox -- -k test_name` | Pass args to pytest |
| `tox -l` | List environments |

## Environment Variables

```ini
[testenv]
setenv =
    PYTHONPATH = {toxinidir}/src
    DATABASE_URL = sqlite:///test.db
passenv =
    HOME
    CI
    GITHUB_*
```

## Dependencies

```ini
[testenv]
# From requirements file
deps = -r requirements-test.txt

# Specific packages
deps =
    pytest>=8.0
    httpx>=0.25.0

# Editable install of project
usedevelop = true
```

## Matrix Testing

```ini
[tox]
env_list = py{310,311,312}-{django42,django50}

[testenv]
deps =
    django42: Django>=4.2,<4.3
    django50: Django>=5.0,<5.1
    pytest-django
```

## CI Integration

### GitHub Actions
```yaml
- name: Run tox
  run: |
    pip install tox
    tox -e py${{ matrix.python-version }}
```

### With tox-gh-actions
```ini
[gh-actions]
python =
    3.10: py310
    3.11: py311
    3.12: py312, lint, typecheck
```
