import asyncio
import os
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load .env if needed
load_dotenv()

AGENT_JWT = os.getenv("AGENT_JWT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Make sure this is set

# Create GenAI session
session = GenAISession(jwt_token=AGENT_JWT)

# OpenAI client
openai = AsyncOpenAI(api_key=OPENAI_API_KEY)

@session.bind(
    name="summarize_text",
    description="Agent that summarizes a block of text.",
)
async def summarize_text(
    agent_context: Annotated[GenAIContext, "Agent context object"],
    text: Annotated[str, "The text to summarize"]
) -> str:
    agent_context.logger.info("Summarizing text...")

    try:
        response = await openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following:\n\n{text}"}
            ],
            temperature=0.5
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        agent_context.logger.error(f"Error during summarization: {e}")
        return "Sorry, I couldn't summarize that."

async def main():
    print(f"Summarizer agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
