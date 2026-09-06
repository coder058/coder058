# Jordi Lluis

Software developer in Amsterdam. I build web interfaces and APIs, then test how they fail.

[Portfolio](https://coder058.github.io/profile/) · [Résumé](https://coder058.github.io/profile/resume.html) · [“TAPE”](https://coder058.github.io/profile/tape/) · [“HOST”](https://coder058.github.io/profile/host/) · [Engineering notes](ENGINEERING.md)

## Pattern Forge

**Decision:** replay must not see later candles. Indicators and higher-timeframe aggregates use only the selected prefix; incomplete groups are omitted, not guessed.

**What I built:** React/TypeScript workspace, Next.js candle API, live mid-price on a separate WebSocket, PostgreSQL persistence for local/CI.

**Code:** [`app/`](https://github.com/coder058/pattern-forge/tree/main/app) · [closed-candle tests](https://github.com/coder058/pattern-forge/blob/main/tests/public-market.test.mjs) · [ingest](https://github.com/coder058/pattern-forge/tree/main/ingest)

```
npm ci && npm test && npm run build
```

The public demo does not serve PostgreSQL. CI builds the Docker image and checks that stored rows survive a database restart.

## Relay

**Decision:** keep the original job text next to each mention. Do not ask a model to decide eligibility.

**What I built:** one Python/FastAPI service behind a React UI and four read-only MCP tools. Duplicates keep changed wording.

**Code:** [`backend/`](https://github.com/coder058/relay/tree/main/backend) · [evidence tests](https://github.com/coder058/relay/blob/main/backend/tests/test_job_evidence.py) · [MCP](https://github.com/coder058/relay/blob/main/backend/tests/test_job_mcp.py)

Matching is literal. Coverage is one public board page plus pasted text.

## Python trading bot

**Decision:** publish the loss and keep branch prices distinct. Early tickets were often $0.96–$0.99; StratA used $0.40–$0.72 with 11–15 seconds remaining; UC looked at leftover $0.01–$0.20 asks.

**What is public:** ledger script, timing parser, browser case study. The private bot is not in this repository. Live trading stopped.

**Code:** [`analyze.py`](https://github.com/coder058/polybow-case-study/blob/main/analyze.py) · [EVIDENCE.md](https://github.com/coder058/polybow-case-study/blob/main/EVIDENCE.md)

An API acknowledgement is not a fill. Dublin was not compared with another region.

## City Gardens (team, 2023)

Le Wagon Barcelona. Rails and PostgreSQL. Not sole-authored and not maintained.

My merged pull requests: [parcel reservations](https://github.com/justdevelopin/CityGardens/pull/37), [add-event button](https://github.com/justdevelopin/CityGardens/pull/38), [logout](https://github.com/justdevelopin/CityGardens/pull/39), [styles](https://github.com/justdevelopin/CityGardens/pull/47), [fontsize](https://github.com/justdevelopin/CityGardens/pull/50). I also contributed event-index partials, a search bar and Cloudinary for event photos. That is not the whole schema.

[Schema](https://github.com/justdevelopin/CityGardens/blob/master/db/schema.rb)

## Other public exercises

[DispatchOps](https://github.com/coder058/dispatchops) · [Transcript Desk](https://github.com/coder058/transcript-desk) · [API labs](https://github.com/coder058?tab=repositories&q=js-) · [Rails labs](https://github.com/coder058?tab=repositories&q=rails-)
