# Agent with context (dependency injection)

import asyncio
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, function_tool


@dataclass
class UserContext:
    # Context object passed to all tools and agents
    user_id: str
    user_name: str
    preferences: dict


@function_tool
def get_user_profile(wrapper: RunContextWrapper[UserContext]) -> str:
    # Access context in tool
    ctx = wrapper.context
    return f"User: {ctx.user_name} (ID: {ctx.user_id})"


@function_tool
def get_preferences(wrapper: RunContextWrapper[UserContext]) -> str:
    # Access user preferences from context
    ctx = wrapper.context
    return f"Preferences: {ctx.preferences}"


agent = Agent(
    name="PersonalAssistant",
    instructions="You are a personal assistant. Use the available tools to help the user.",
    tools=[get_user_profile, get_preferences],
)


async def main():
    # Create context with user data
    context = UserContext(
        user_id="user-123",
        user_name="Alice",
        preferences={"theme": "dark", "language": "en"}
    )

    result = await Runner.run(
        agent,
        "What are my current preferences?",
        context=context
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
