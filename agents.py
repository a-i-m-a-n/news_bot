import os
from crewai import Agent, LLM

from tools.news_fetcher_tool import fetch_news
from tools.summarizer_tool import summarize_articles
from tools.slack_tool import post_to_slack
from tools.sheets_tool import log_to_sheet

gemini_llm = LLM(
    model="gemini/gemini-3.1-flash-lite",
    api_key=os.environ.get("GEMINI_API_KEY"),
)

news_fetcher_agent = Agent(
    role="News Fetcher",
    goal="Find the latest, most relevant news articles for the given topics.",
    backstory=(
        "A tireless researcher who scans the web for breaking news the moment "
        "it's published, filtering out noise and irrelevant results."
    ),
    tools=[fetch_news],
    llm=gemini_llm,
    verbose=True,
)

summarizer_agent = Agent(
    role="News Summarizer",
    goal="Turn raw articles into short, clear, deduplicated summaries.",
    backstory=(
        "A sharp news editor who can distill a wall of text into the handful "
        "of sentences that actually matter."
    ),
    tools=[summarize_articles],
    llm=gemini_llm,
    verbose=True,
)

distributor_agent = Agent(
    role="News Distributor",
    goal="Deliver summarized news to Slack and log it to Google Sheets.",
    backstory=(
        "A reliable operator who makes sure every summary reaches the team "
        "channel and is archived for later reference."
    ),
    tools=[post_to_slack, log_to_sheet],
    llm=gemini_llm,
    verbose=True,
)
