import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZGIzZWI5NS04NzhlLTQwMDctODc0ZS1hZDgzNjZhNDJlMzAiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImU2NjUyZWU5LTc3OGQtNGM3ZS1iMmUyLWY2OWQzYTUzZTI0NyJ9.rlwqhJHWQSzYgoDyh3TfIAwwIO4Bwy5Aj5xpJb9jEFg" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="text_summarizer",
    description="Agent that summarizes a block of text.",
)
async def text_summarizer(
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
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
