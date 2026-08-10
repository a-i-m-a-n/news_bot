# AI News Automation Bot

CrewAI-based multi-agent pipeline that fetches trending news, summarizes it with
Gemini, posts it to Slack, and logs it to Google Sheets. All four tools are
built from scratch on top of the raw APIs (no CrewAI built-in tools).

## Project structure

```
ai-news-bot/
├── agents.py                  # News Fetcher, Summarizer, Distributor agents
├── tasks.py                   # fetch -> summarize -> distribute task chain
├── crew.py                    # assembles the Crew (sequential process)
├── main.py                    # run() entry point — plain function, reusable later
├── tools/
│   ├── news_fetcher_tool.py   # Tavily Search API, called directly
│   ├── summarizer_tool.py     # Gemini API (gemini-3.1-flash-lite), called directly
│   ├── slack_tool.py          # Slack Incoming Webhook, called directly
│   └── sheets_tool.py         # Google Sheets API, called directly
├── .github/workflows/news_bot.yml   # runs the pipeline every 6 hours
├── requirements.txt
└── .env.example
```

## 1. Local setup

```bash
cd ai-news-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:

| Variable | Where to get it |
|---|---|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/) |
| `TAVILY_API_KEY` | [tavily.com](https://tavily.com) |
| `SLACK_WEBHOOK_URL` | Slack → Apps → Incoming Webhooks |
| `GOOGLE_SHEET_ID` | The ID in your Sheet's URL |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Full JSON key of a service account with Sheets API access, minified to one line |

The target Sheet needs a `Sheet1` tab (or adjust the range in
`tools/sheets_tool.py`) and must be shared with the service account's
`client_email` as an Editor.

## 2. Run it locally

```bash
python main.py
```

This runs the pipeline once, end-to-end, and prints the final crew output.
Confirm messages land in Slack and rows land in the Sheet before automating.

## 3. Automate with GitHub Actions

Once local runs work:

1. Push this project to a GitHub repo.
2. In the repo, go to **Settings → Secrets and variables → Actions** and add
   the same five variables from `.env` as repository secrets.
3. The workflow at `.github/workflows/news_bot.yml` runs automatically every
   6 hours (`cron: "0 */6 * * *"`), or on demand via **Actions → AI News Bot →
   Run workflow**.

## 4. Vercel deployment (later)

`main.py`'s `run()` function is a plain callable with no CLI coupling, so
when you're ready to deploy, it can be dropped behind a serverless handler
(e.g. `api/run.py` importing and calling `run()`) without changing any of
the agents, tasks, or tools. Note: Vercel's free Hobby tier only supports
once-a-day cron cadence, so GitHub Actions should stay the scheduler even
after deployment — Vercel would just host a callable endpoint (useful for
manual/on-demand triggers or a future UI).
