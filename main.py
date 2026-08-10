from dotenv import load_dotenv

load_dotenv()

from crew import build_crew

DEFAULT_TOPICS = ["AI", "crypto"]


def run(topics: list[str] | None = None):
    """
    Runs the full fetch -> summarize -> distribute pipeline once.
    Kept as a plain function so it can later be called from a Vercel
    serverless handler without any restructuring.
    """
    topics = topics or DEFAULT_TOPICS
    crew = build_crew(topics)
    result = crew.kickoff()
    print(result)
    return result


if __name__ == "__main__":
    run()
