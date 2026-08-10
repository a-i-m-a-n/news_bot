import os
import requests
from crewai.tools import tool

TAVILY_API_URL = "https://api.tavily.com/search"


@tool("News Fetcher Tool")
def fetch_news(topic: str, max_results: int = 5) -> str:
    """
    Fetches the latest news articles for a given topic using the Tavily Search API.
    Returns a list of articles with title, url, and a short content snippet.

    Args:
        topic: The subject to search news for (e.g. "AI", "crypto", "finance").
        max_results: Maximum number of articles to return (default 5).
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY is not set."

    payload = {
        "api_key": api_key,
        "query": f"latest {topic} news",
        "search_depth": "basic",
        "topic": "news",
        "max_results": max_results,
        "include_answer": False,
    }

    try:
        response = requests.post(TAVILY_API_URL, json=payload, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error fetching news for '{topic}': {e}"

    results = response.json().get("results", [])
    if not results:
        return f"No news found for topic: {topic}"

    formatted = [f"Topic: {topic}"]
    for r in results:
        formatted.append(
            f"- Title: {r.get('title')}\n"
            f"  URL: {r.get('url')}\n"
            f"  Snippet: {(r.get('content') or '')[:300]}"
        )
    return "\n".join(formatted)
