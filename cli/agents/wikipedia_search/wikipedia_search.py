import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyOTQ4YzhkZi1hZDFlLTRjZWEtYWJkMC0wOTdlMjI0OGIwMzYiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjdhMmRlYTkwLWY2ODktNGYzYi04ZTZjLWZiMGFkZmI3Mjg0ZSJ9.k9ZKSLqNS6npYQahr6gqt5nRG8_yus8N8ESQazwr12s" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="wikipedia_search",
    description="Agent that searches on wikipedia"
)
async def wikipedia_search(
    agent_context: GenAIContext,
    test_arg: Annotated[
        str,
        "This is a test argument. Your agent can have as many parameters as you want. Feel free to rename or adjust it to your needs.",  # noqa: E501
    ],
):
    """Agent that searches on wikipedia"""
    return "Hello, World!"


async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
