import os
import requests
from crewai.tools import tool


@tool("Slack Bot Tool")
def post_to_slack(message: str) -> str:
    """
    Posts a formatted message (headline + summary + link) to the configured
    Slack channel via an Incoming Webhook.

    Args:
        message: The fully formatted text to post to Slack.
    """
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return "Error: SLACK_WEBHOOK_URL is not set."

    try:
        response = requests.post(webhook_url, json={"text": message}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error posting to Slack: {e}"

    return "Message posted to Slack successfully."
