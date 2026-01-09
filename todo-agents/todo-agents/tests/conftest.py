# Pytest fixtures for OpenAI Agents testing

import pytest
from unittest.mock import AsyncMock, patch


@pytest.fixture
def mock_openai_response():
    # Mock OpenAI API response
    return {
        "choices": [
            {"message": {"content": "Mocked response"}}
        ]
    }


@pytest.fixture
def mock_runner():
    # Mock the Runner for testing
    with patch("agents.Runner.run", new_callable=AsyncMock) as mock:
        yield mock
