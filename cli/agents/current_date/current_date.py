import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
from datetime import datetime

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5YzQyMjhmMC02MDQxLTRjNWMtYTRlNS1jM2M1MzJlZjQ0OTEiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjE0ZTM3ZDExLTEwZTctNDcxNC1iNzRhLTI1OTFkMTE0YWQ3MyJ9.-S2cvoDRxfHgcPY3AnMmNFIvPq48JiyIxu-TrHcxJog" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="current_date",
    description="Agent that returns current date"
)
async def current_date(
    agent_context):
    agent_context.logger.info("Inside get_current_date")
return datetime.now().strftime("%Y-%m-%d")

async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
