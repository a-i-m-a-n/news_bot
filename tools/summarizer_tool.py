import os
from crewai.tools import tool
from google import genai

_MODEL_NAME = "gemini-3.1-flash-lite"
_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set.")
        _client = genai.Client(api_key=api_key)
    return _client


@tool("Intelligent Summarizer Tool")
def summarize_articles(articles_text: str) -> str:
    """
    Summarizes a batch of fetched news articles into short, structured updates.
    Deduplicates near-identical stories and highlights the most important points.

    Args:
        articles_text: Raw text containing one or more articles (title, url, snippet).
    """
    client = _get_client()

    prompt = (
        "You are a news editor. Given the raw articles below, produce a "
        "deduplicated list of concise news summaries. For each distinct story, "
        "output exactly this format:\n"
        "Headline: <short headline>\n"
        "Summary: <2-3 sentence summary>\n"
        "Source: <url>\n"
        "---\n"
        "If two articles cover the same story, keep only the clearest one.\n\n"
        f"Articles:\n{articles_text}"
    )

    try:
        response = client.models.generate_content(
            model=_MODEL_NAME,
            contents=prompt,
        )
    except Exception as e:
        return f"Error summarizing articles: {e}"

    return response.text or "No summary generated."