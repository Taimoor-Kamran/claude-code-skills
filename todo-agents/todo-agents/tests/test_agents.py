# Example test for agents

import pytest
from agents import Agent


class TestBasicAgent:
    def test_agent_creation(self):
        agent = Agent(
            name="TestAgent",
            instructions="Test instructions"
        )
        assert agent.name == "TestAgent"

    def test_agent_with_tools(self):
        from agents import function_tool

        @function_tool
        def dummy_tool() -> str:
            return "result"

        agent = Agent(
            name="ToolAgent",
            instructions="Agent with tools",
            tools=[dummy_tool]
        )
        assert len(agent.tools) == 1


class TestAgentIntegration:
    @pytest.mark.asyncio
    async def test_basic_run(self, mock_runner):
        # Test with mocked runner
        mock_runner.return_value.final_output = "Test response"

        agent = Agent(name="Test", instructions="Test")
        result = await mock_runner(agent, "Hello")

        assert result.final_output == "Test response"
