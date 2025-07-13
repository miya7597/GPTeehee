import asyncio
from typing import Annotated
import logging
from typing import Annotated, Literal, Optional
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5ZjU0ZTQwOC04MjRjLTQ4YjQtOTA5MS0yZDI0N2UxMGVmZDAiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImU2NjUyZWU5LTc3OGQtNGM3ZS1iMmUyLWY2OWQzYTUzZTI0NyJ9.CtnesGceOntQwWGD7b4AfYcnbLrq4FS40qtZj2_I06k" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="explainer",
    description="Agent that explains text at different complexities (e.g. kid, adult, expert)"
)
async def explainer(
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
