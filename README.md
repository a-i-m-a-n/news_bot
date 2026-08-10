# AI News Automation Bot

A multi-agent pipeline, built with CrewAI, that fetches trending news, summarizes it with Gemini, posts it to Slack, and archives it in Google Sheets — running on a schedule with no manual trigger.

## How it works

Three agents run in sequence, each backed by a custom tool built directly on its underlying API (no CrewAI built-in tools):

| Agent | Tool | API |
|---|---|---|
| News Fetcher | `fetch_news` | Tavily Search |
| Summarizer | `summarize_articles` | Gemini (`gemini-3.1-flash-lite`) |
| Distributor | `post_to_slack`, `log_to_sheet` | Slack Incoming Webhook, Google Sheets |

## Project structure

```
ai-news-bot/
├── agents.py                      # agent definitions
├── tasks.py                       # fetch → summarize → distribute task chain
├── crew.py                        # crew assembly
├── main.py                        # run() entry point
├── tools/
│   ├── news_fetcher_tool.py
│   ├── summarizer_tool.py
│   ├── slack_tool.py
│   └── sheets_tool.py
├── .github/workflows/news_bot.yml # scheduled run, every 6 hours
├── requirements.txt
└── .env.example
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Populate `.env`:

| Variable | Source |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio |
| `TAVILY_API_KEY` | tavily.com |
| `SLACK_WEBHOOK_URL` | Slack → Apps → Incoming Webhooks |
| `GOOGLE_SHEET_ID` | Target sheet's URL |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Service account key, minified to one line |

The target spreadsheet needs a `Sheet1` tab and must be shared with the service account's `client_email` as an Editor.

## Run

```bash
python main.py
```

Runs the pipeline once end-to-end. Verify a message lands in Slack and a row lands in the Sheet before automating.

## Automation

The pipeline runs unattended via GitHub Actions (`.github/workflows/news_bot.yml`), on a 6-hour cron schedule.

1. Push this repo to GitHub.
2. Add the five `.env` variables as repository secrets (**Settings → Secrets and variables → Actions**).
3. The workflow runs automatically, or on demand via **Actions → AI News Bot → Run workflow**.

## Deployment

Deployment is intentionally out of scope for now. `run()` in `main.py` has no CLI coupling, so it can later sit behind a Vercel serverless handler without changes to the agents, tasks, or tools. Note that Vercel's free tier caps cron at once daily — GitHub Actions should remain the scheduler even after deployment.
