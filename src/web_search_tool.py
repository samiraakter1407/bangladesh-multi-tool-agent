
import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.tools import tool

load_dotenv()

if not os.getenv("TAVILY_API_KEY"):
    raise ValueError(
        "TAVILY_API_KEY is missing. "
        "Add it to your project's .env file."
    )

tavily_search = TavilySearch(max_results=5)


@tool
def web_search_tool(query: str) -> str:
    """Search the web for general knowledge and current information.

    Use for Bangladesh policies, government responsibilities,
    definitions, cultural context, and current facts not
    contained in the local datasets.
    """
    results = tavily_search.invoke({"query": query})

    if isinstance(results, dict):
        results = results.get("results", [results])

    formatted_results = []

    for i, result in enumerate(results, start=1):
        formatted_results.append(
            f"{i}. {result.get('title', 'Untitled')}\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Content: {result.get('content', 'No content available')}"
        )

    return "\n\n".join(formatted_results)


if __name__ == "__main__":
    print(
        web_search_tool.invoke({
            "query": "What is the role of DGHS in Bangladesh?"
        })
    )
