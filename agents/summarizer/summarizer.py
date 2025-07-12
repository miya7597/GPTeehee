import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWNjZjMzOS0yODg0LTQzZjgtOGY1Yy02OWQ4OTYwYTQzNTUiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImJiYmNiMTRhLWQyYTAtNDViMC04YTcyLWZmMjUyOTQ3YjZiNCJ9.zvcHXv9d0vsNsPUWL9WuD74lW58LIwiNmIKWU0GCU00" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="summarizer",
    description="Summarizes text"
)
async def summarizer(
    agent_context: GenAIContext,
    test_arg: Annotated[
        str,
        "This is a test argument. Your agent can have as many parameters as you want. Feel free to rename or adjust it to your needs.",  # noqa: E501
    ],
):
    """Summarizes text"""
    return "Hello, World!"


async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
