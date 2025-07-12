import asyncio
import os
import requests
import logging
from dotenv import load_dotenv
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Get the token from .env
AGENT_JWT = os.getenv("AGENT_JWT")
session = GenAISession(jwt_token=AGENT_JWT)

@session.bind(
    name="wikipedia_search",
    description="Searches Wikipedia for a given query and returns the summary."
)
async def wikipedia_search(
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

async def main():
    logging.info("Wikipedia Search Agent is running...")
    try:
        await session.process_events()
    except KeyboardInterrupt:
        logging.info("Interrupted. Shutting down agent...")
    finally:
        await session.close()

async def main():
    logging.info("Wikipedia Search Agent is running...")
    print("✅ Agent script loaded")
    try:
        await session.process_events()
    except KeyboardInterrupt:
        logging.info("Interrupted. Shutting down agent...")
    finally:
        await session.close()
        
if __name__ == "__main__":
    asyncio.run(main())