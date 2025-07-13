import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYWU2MmE5ZC00Y2E3LTRjZjctOGUyNC1jYzgyZTMyYTFlZDYiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImU2NjUyZWU5LTc3OGQtNGM3ZS1iMmUyLWY2OWQzYTUzZTI0NyJ9.PGbrQj1HWyi3acwJydGKn_UYjLPX0tb70v4xUXL87DU" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="wikipedia_searcher",
    description="agent that searches wikipedia"
)
async def wikipedia_searcher(
    agent_context: GenAIContext,
    query: Annotated[str, "The topic or term to search on Wikipedia"]
) -> str:
    logging.info(f"Searching Wikipedia for: {query}")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"

    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return data.get("extract", "No summary found.")
        elif res.status_code == 404:
            return f"No Wikipedia page found for '{query}'."
        else:
            return f"Error: Received status code {res.status_code}"
    except Exception as e:
        logging.error(f"Exception while querying Wikipedia: {e}")
        return "An error occurred while searching Wikipedia."

# ✅ Correct single definition of main
async def main():
    logging.info("Wikipedia Search Agent is running...")
    print("✅ Agent script loaded")
    try:
        await session.process_events()
    except KeyboardInterrupt:
        logging.info("Interrupted. Shutting down agent...")
    finally:
        await session.close()


async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
