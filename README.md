# Jordi Lluis

Amsterdam. Market-data interfaces, HTTP APIs and small developer tools. React and TypeScript on the front, Python or Rails on the back.

[Portfolio](https://coder058.github.io/profile/) · [Résumé](https://coder058.github.io/profile/resume.html) · [Engineering notes](ENGINEERING.md)

**Live demos:** [Pattern Forge](https://pattern-forge-five.vercel.app/) · [Relay](https://relay-ten-zeta.vercel.app/) · [Python trading bot archive](https://polybow-archive.vercel.app/)

## Pattern Forge

[![CI](https://github.com/coder058/pattern-forge/actions/workflows/check.yml/badge.svg)](https://github.com/coder058/pattern-forge/actions/workflows/check.yml)

**Architecture:** browser → Next.js candle API → Hyperliquid public quotes. A separate WebSocket carries live mid-price and does not write into replay. Recorded replay uses only the selected prefix; incomplete higher-timeframe groups are omitted, not guessed. The public demo does not serve PostgreSQL; persistence is for local use and CI.

**What I built:** React/TypeScript workspace, validated candle snapshots, Docker build checks and failure-handling tests.

**Code:** [`app/`](https://github.com/coder058/pattern-forge/tree/main/app) · [closed-candle tests](https://github.com/coder058/pattern-forge/blob/main/tests/public-market.test.mjs) · [ingest](https://github.com/coder058/pattern-forge/tree/main/ingest)

```
npm ci && npm test && npm run build
```

## Relay

[![CI](https://github.com/coder058/relay/actions/workflows/check.yml/badge.svg)](https://github.com/coder058/relay/actions/workflows/check.yml)

**Architecture:** React UI → stateless FastAPI → one deterministic matcher, also exposed as four read-only MCP tools. Returns quoted sentences, not a hiring score. Paste is the real input; Arbeitnow is a bounded demo snapshot.

**What I built:** `search_job_board`, `summarize_job_board`, `review_job_evidence`, `export_job_review`. Duplicates keep changed wording.

**Code:** [`backend/`](https://github.com/coder058/relay/tree/main/backend) · [evidence tests](https://github.com/coder058/relay/blob/main/backend/tests/test_job_evidence.py) · [MCP](https://github.com/coder058/relay/blob/main/backend/tests/test_job_mcp.py)

Matching is literal. An agent that calls these tools can still summarise; Relay does not decide eligibility.

## Python trading bot

**Decision:** publish the loss and keep branch prices distinct. Early tickets were often $0.96–$0.99; StratA used $0.40–$0.72 with 11–15 seconds remaining; UC looked at leftover $0.01–$0.20 asks.

**What is public:** ledger script, timing parser, browser case study. The private bot is not in this repository. Live trading stopped.

**Code:** [`analyze.py`](https://github.com/coder058/polybow-case-study/blob/main/analyze.py) · [EVIDENCE.md](https://github.com/coder058/polybow-case-study/blob/main/EVIDENCE.md)

An API acknowledgement is not a fill. Dublin was not compared with another region.

## Open source

Merged [Haystack #12635](https://github.com/deepset-ai/haystack/pull/12635): AutoMergingRetriever now treats `0` as a stored hierarchy value, not missing metadata. That is one accepted fix, not Haystack product work.

## City Gardens (team, 2023)

Le Wagon Barcelona. Rails and PostgreSQL. Not sole-authored and not maintained.

My merged pull requests: [parcel reservations](https://github.com/justdevelopin/CityGardens/pull/37), [add-event button](https://github.com/justdevelopin/CityGardens/pull/38), [logout](https://github.com/justdevelopin/CityGardens/pull/39), [styles](https://github.com/justdevelopin/CityGardens/pull/47), [fontsize](https://github.com/justdevelopin/CityGardens/pull/50). I also contributed event-index partials, a search bar and Cloudinary for event photos. That is not the whole schema.

[Schema](https://github.com/justdevelopin/CityGardens/blob/master/db/schema.rb)

## Other public exercises

[DispatchOps](https://github.com/coder058/dispatchops) · [Transcript Desk](https://github.com/coder058/transcript-desk) · [Wikinimous](https://github.com/coder058/rails-wikinimous) · [API labs](https://github.com/coder058?tab=repositories&q=js-) · [Rails labs](https://github.com/coder058?tab=repositories&q=rails-)
