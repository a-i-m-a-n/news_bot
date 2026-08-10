from crewai import Crew, Process

from agents import news_fetcher_agent, summarizer_agent, distributor_agent
from tasks import build_tasks


def build_crew(topics: list[str]) -> Crew:
    tasks = build_tasks(topics)
    return Crew(
        agents=[news_fetcher_agent, summarizer_agent, distributor_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
