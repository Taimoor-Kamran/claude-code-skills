# Basic agent example

import asyncio
from agents import Agent, Runner


# Define your agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Be concise and clear in your responses.",
)


async def main():
    # Run a simple conversation
    result = await Runner.run(agent, "Hello! What can you help me with?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
