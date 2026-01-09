# Multi-agent workflow with handoffs

import asyncio
from agents import Agent, Runner


# Define specialized agents
triage_agent = Agent(
    name="Triage",
    instructions="You route user requests to the appropriate specialist. "
                 "For technical questions, handoff to TechSupport. "
                 "For billing questions, handoff to Billing.",
    handoffs=["TechSupport", "Billing"],
)

tech_agent = Agent(
    name="TechSupport",
    instructions="You are a technical support specialist. "
                 "Help users with technical issues and troubleshooting.",
)

billing_agent = Agent(
    name="Billing",
    instructions="You are a billing specialist. "
                 "Help users with billing questions and account issues.",
)

# Register agents for handoffs
triage_agent.handoffs = [tech_agent, billing_agent]


async def main():
    result = await Runner.run(
        triage_agent,
        "I am having trouble connecting to the API"
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
