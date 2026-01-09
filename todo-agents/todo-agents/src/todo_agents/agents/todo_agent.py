"""Todo management agent with custom tools."""

import asyncio
from agents import Agent, Runner

from ..tools.todo_tools import (
    create_todo, list_todos, get_todo, update_todo, delete_todo, toggle_todo
)


# Create the todo management agent with tools
todo_agent = Agent(
    name="TodoAssistant",
    instructions="""
    You are a helpful todo management assistant. You can help users manage their todos by:
    1. Creating new todo items
    2. Listing existing todo items with various filters
    3. Getting details of a specific todo
    4. Updating existing todo items
    5. Deleting todo items
    6. Toggling completion status of todo items

    Always be helpful and friendly. Ask clarifying questions if the user's request is ambiguous.
    When creating todos, always ask for a title if not provided.
    When updating or performing actions on specific todos, ask for the todo ID if not provided.
    For due dates, accept common date formats like YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS.
    """,
    tools=[
        create_todo,
        list_todos,
        get_todo,
        update_todo,
        delete_todo,
        toggle_todo
    ],
)


async def main():
    """Run a conversation with the todo agent."""
    print("Todo Assistant ready! You can ask me to manage your todos.")
    print("Examples: 'Create a todo to buy groceries', 'List my todos', 'Mark todo 1 as complete'")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break

        if not user_input:
            continue

        try:
            result = await Runner.run(todo_agent, user_input)
            print(f"Assistant: {result.final_output}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())