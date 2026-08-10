from crewai import Task

from agents import news_fetcher_agent, summarizer_agent, distributor_agent


def build_tasks(topics: list[str]) -> list[Task]:
    topics_str = ", ".join(topics)

    fetch_task = Task(
        description=(
            f"Fetch the latest trending news articles for these topics: {topics_str}. "
            "Use the News Fetcher Tool once per topic and combine all results into "
            "a single list."
        ),
        expected_output=(
            "A combined list of articles with title, url, and snippet for each topic."
        ),
        agent=news_fetcher_agent,
    )

    summarize_task = Task(
        description=(
            "Take the fetched articles and produce a deduplicated list of short, "
            "structured summaries using the Intelligent Summarizer Tool. Each "
            "entry must include Headline, Summary, and Source fields."
        ),
        expected_output=(
            "A list of entries, each with Headline, Summary, and Source fields."
        ),
        agent=summarizer_agent,
        context=[fetch_task],
    )

    distribute_task = Task(
        description=(
            "For every summarized entry: post it to Slack via the Slack Bot Tool "
            "(headline + summary + link, formatted for quick reading), and log it "
            "to Google Sheets via the Sheets Logger Tool (Date, Headline, Summary, "
            "Source URL)."
        ),
        expected_output=(
            "Confirmation that all entries were posted to Slack and logged to Sheets."
        ),
        agent=distributor_agent,
        context=[summarize_task],
    )

    return [fetch_task, summarize_task, distribute_task]
