# Agent with custom tools example

import asyncio
from agents import Agent, Runner, function_tool


# Define custom tools using the @function_tool decorator
@function_tool
def get_weather(city: str) -> str:
    # Get weather for a city (mock implementation)
    return f"The weather in {city} is sunny, 72F"


@function_tool
def calculate(expression: str) -> str:
    # Safely evaluate a math expression
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# Create agent with tools
agent = Agent(
    name="ToolAgent",
    instructions="You are a helpful assistant with access to weather and calculator tools.",
    tools=[get_weather, calculate],
)


async def main():
    result = await Runner.run(
        agent,
        "What is the weather in San Francisco? Also, what is 25 * 4?"
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
