#!/usr/bin/env python3
"""Scaffold a pytest project with tox integration."""

import argparse
import os
from pathlib import Path

PYPROJECT_TOML = '''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
description = "{description}"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-xdist>=3.0",
    "tox>=4.0",
]

[tool.pytest.ini_options]
addopts = [
    "--import-mode=importlib",
    "-v",
    "--strict-markers",
]
testpaths = ["tests"]
pythonpath = ["src"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
'''

TOX_INI = '''[tox]
env_list = py310, py311, py312, lint, coverage
isolated_build = true

[testenv]
description = Run tests with pytest
deps =
    pytest>=8.0
    pytest-cov>=4.0
commands =
    pytest {posargs}

[testenv:coverage]
description = Run tests with coverage report
deps =
    pytest>=8.0
    pytest-cov>=4.0
commands =
    pytest --cov=src --cov-report=term-missing --cov-report=html {posargs}

[testenv:lint]
description = Run linting checks
skip_install = true
deps =
    ruff>=0.1.0
commands =
    ruff check src tests
    ruff format --check src tests

[testenv:format]
description = Format code
skip_install = true
deps =
    ruff>=0.1.0
commands =
    ruff format src tests
    ruff check --fix src tests
'''

CONFTEST_PY = '''"""Shared pytest fixtures."""

import pytest


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {"key": "value", "count": 42}


@pytest.fixture(scope="session")
def session_resource():
    """Resource shared across all tests in session."""
    resource = setup_resource()
    yield resource
    teardown_resource(resource)


def setup_resource():
    """Setup logic for session resource."""
    return {"initialized": True}


def teardown_resource(resource):
    """Teardown logic for session resource."""
    pass
'''

TEST_EXAMPLE = '''"""Example test module."""

import pytest


class TestExample:
    """Example test class."""

    def test_basic(self, sample_data):
        """Test using fixture."""
        assert sample_data["key"] == "value"
        assert sample_data["count"] == 42

    @pytest.mark.parametrize(
        "input_val,expected",
        [
            (1, 2),
            (2, 4),
            (3, 6),
        ],
    )
    def test_parametrized(self, input_val, expected):
        """Test with parametrized inputs."""
        assert input_val * 2 == expected

    @pytest.mark.slow
    def test_slow_operation(self):
        """Test marked as slow."""
        result = sum(range(1000))
        assert result == 499500
'''

GITIGNORE = '''# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.idea/
.vscode/
*.swp

# Environment
.env
.venv/
venv/
'''


def create_project(name: str, path: Path, description: str = ""):
    """Create pytest project structure with tox."""
    project_path = path / name

    # Create directories
    dirs = [
        project_path / "src" / name.replace("-", "_"),
        project_path / "tests" / "unit",
        project_path / "tests" / "integration",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    init_files = [
        project_path / "src" / name.replace("-", "_") / "__init__.py",
        project_path / "tests" / "__init__.py",
        project_path / "tests" / "unit" / "__init__.py",
        project_path / "tests" / "integration" / "__init__.py",
    ]

    for f in init_files:
        f.write_text('"""Package initialization."""\n')

    # Create main files
    desc = description or f"A Python project: {name}"
    pkg_name = name.replace("-", "_")

    (project_path / "pyproject.toml").write_text(
        PYPROJECT_TOML.format(name=name, description=desc)
    )
    (project_path / "tox.ini").write_text(TOX_INI)
    (project_path / "tests" / "conftest.py").write_text(CONFTEST_PY)
    (project_path / "tests" / "unit" / "test_example.py").write_text(TEST_EXAMPLE)
    (project_path / ".gitignore").write_text(GITIGNORE)

    # Create placeholder module
    (project_path / "src" / pkg_name / "main.py").write_text(
        f'"""Main module for {name}."""\n\n\ndef hello() -> str:\n    """Return greeting."""\n    return "Hello, World!"\n'
    )

    print(f"Created pytest project: {project_path}")
    print(f"\nStructure:")
    print(f"  {name}/")
    print(f"  ├── pyproject.toml")
    print(f"  ├── tox.ini")
    print(f"  ├── .gitignore")
    print(f"  ├── src/{pkg_name}/")
    print(f"  │   ├── __init__.py")
    print(f"  │   └── main.py")
    print(f"  └── tests/")
    print(f"      ├── conftest.py")
    print(f"      ├── unit/")
    print(f"      │   └── test_example.py")
    print(f"      └── integration/")
    print(f"\nNext steps:")
    print(f"  cd {name}")
    print(f"  pip install -e '.[dev]'  # or: uv pip install -e '.[dev]'")
    print(f"  tox                       # run all test environments")
    print(f"  tox -e py312              # run specific environment")
    print(f"  pytest                    # run tests directly")


def main():
    parser = argparse.ArgumentParser(description="Scaffold pytest project with tox")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Parent directory")
    parser.add_argument("--description", default="", help="Project description")

    args = parser.parse_args()
    create_project(args.name, args.path, args.description)


if __name__ == "__main__":
    main()
