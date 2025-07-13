import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OWZmOWYzMy1mZDBmLTRhZjgtYjhhMS01ZDgyN2IzMjBmNDIiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImU2NjUyZWU5LTc3OGQtNGM3ZS1iMmUyLWY2OWQzYTUzZTI0NyJ9.rOoX1yJdvZCtnq3LSZN87aPeewd3ywJQbEcbkTjJn2k" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="scholar",
    description="agent that searches academic papers"
)
async def scholar(
    agent_context,
    query: Annotated[str, "The academic topic or question to search for"]
) -> dict[str, Any]:
    agent_context.logger.info("Inside scholar")
    base_url = "https://api.semanticscholar.org/graph/v1"

    async with httpx.AsyncClient() as client:
        # Step 1: Search for papers
        search_params = {
            "query": query,
            "limit": 5,
            "fields": "title,authors,url,citationCount,paperId"
        }
        search_resp = await client.get(f"{base_url}/paper/search", params=search_params)
        search_data = search_resp.json()

        if not search_data.get("data"):
            return {"message": "No papers found for that query."}

        # Step 2: Get most cited paper
        most_cited = max(search_data["data"], key=lambda p: p.get("citationCount", 0))
        paper_id = most_cited["paperId"]

        # Step 3: Fetch detailed info
        detail_fields = "title,authors,url,citationCount,year,venue,abstract"
        detail_resp = await client.get(f"{base_url}/paper/{paper_id}", params={"fields": detail_fields})
        paper = detail_resp.json()

    # Format authors
    authors = paper.get("authors", [])
    author_names = [a.get("name", "") for a in authors]
    if len(author_names) > 3:
        formatted_authors = ", ".join(author_names[:3]) + ", et al."
    else:
        formatted_authors = ", ".join(author_names)

    # Format citation
    citation = (
        f"{formatted_authors} ({paper.get('year')}). "
        f"*{paper.get('title')}*. {paper.get('venue')}. "
        f"{paper.get('url')}"
    )

    return {
        "summary": paper.get("abstract", "No abstract available."),
        "citation": citation
    }


async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
