import asyncio
import os
import requests
import logging
from dotenv import load_dotenv
from typing import Annotated, Literal, Optional
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext


# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Get the token
AGENT_JWT = os.getenv("AGENT_JWT");
session = GenAISession(jwt_token=AGENT_JWT)

@session.bind(
    name="gpteehee",
    description="Agent that explains text at different complexities (e.g. kid, adult, expert)"
)
async def gpteehee(
    agent_context: GenAIContext,
    text: Annotated[str, "Text you want explained"],
    complexity: Annotated[Optional[Literal["kid", "adult", "expert"]], "complexity"] = None
):
    logging.info(f"Received text: {text}, complexity: {complexity}")

    if not complexity:
        return (
            f"You entered: \"{text}\"\n"
            "Please specify what type of user you are trying to explain to (e.g. kid, adult, expert)."
        )

    # Respond based on complexity
    if complexity == "kid":
        response = f"For a kid: {text} is like a fun game or a toy that helps us understand how things work!"
    elif complexity == "adult":
        response = f"As an adult: {text} refers to a concept explained with practical, real-world examples and logic."
    elif complexity == "expert":
        response = f"For an expert: {text} involves deeper theoretical principles and technical language."

    logging.info(f"Responding with: {response}")
    return response

async def main():
    logging.info("Agent running and waiting for events...")
    try:
        await session.process_events()
    except KeyboardInterrupt:
        logging.info("Interrupted. Shutting down agent...")
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(main())
