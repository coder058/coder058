# Jordi Lluis

Amsterdam. This page is the code index: what each repository does, how the pieces
fit together and the command that runs it. The written-up version, with the
reasoning and the data tables, is on the [portfolio](https://coder058.github.io/profile/).

[Portfolio](https://coder058.github.io/profile/) · [Résumé](https://coder058.github.io/profile/resume.html) · [Engineering notes](ENGINEERING.md)

**Live demos:** [Pattern Forge](https://pattern-forge-five.vercel.app/) · [Info Desk](https://coder058.github.io/info-desk/) · [Relay](https://relay-ten-zeta.vercel.app/) · [Python trading bot archive](https://polybow-archive.vercel.app/)

## Pattern Forge

[![CI](https://github.com/coder058/pattern-forge/actions/workflows/check.yml/badge.svg)](https://github.com/coder058/pattern-forge/actions/workflows/check.yml)

**Result:** replay without look-ahead; CI runs tests, Docker and a PostgreSQL restart. The public demo does not serve that database.

**Architecture:** browser → Next.js candle API → Hyperliquid public quotes. A separate WebSocket carries live mid-price and does not write into replay. Recorded replay uses only the selected prefix; incomplete higher-timeframe groups are omitted, not guessed. Persistence is for local use and CI.

**What I built:** React/TypeScript workspace, validated candle snapshots, Docker build checks and failure-handling tests.

**Code:** [`app/`](https://github.com/coder058/pattern-forge/tree/main/app) · [closed-candle tests](https://github.com/coder058/pattern-forge/blob/main/tests/public-market.test.mjs) · [ingest](https://github.com/coder058/pattern-forge/tree/main/ingest)

```
npm ci && npm test && npm run build
```

## Info Desk

[![CI](https://github.com/coder058/info-desk/actions/workflows/ci.yml/badge.svg)](https://github.com/coder058/info-desk/actions/workflows/ci.yml)

**Result:** OFAC licenses, the White House oil fact sheet and AP quotes on one claims table, each cell carrying the sentence it came from. SQLite writes a note only after a human approves.

**Architecture:** three tools (`fetch_source`, `lookup_license`, `search_prior_notes`) → Python claims table / named quantities / license parse → pending draft → `approve()`. Ollama is optional and off in CI.

**What I built:** the claims table distinguishes *stated*, *attributed*, *not named* and *absent*, so an absent mention is never scored as a denial. Named extractors keep the 65bn field barrels apart from the 46bn U.S. territorial barrels. Six harness cases assert the database state: ranking conflict, OFAC scope gap, single-source royalties, jailbreak, 429 retry and human reject.

**What is public:** the GitHub Pages URL serves a recorded case built from dated captures. The repository also contains a live research workspace (allowlisted connectors, versioned captures, cited retrieval) that runs locally only.

**Code:** [info-desk](https://github.com/coder058/info-desk) · [harness](https://github.com/coder058/info-desk/blob/main/src/infodesk/harness.py)

```
python -m pip install -e ".[dev]" && python -m pytest
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

Merged [Haystack #12635](https://github.com/deepset-ai/haystack/pull/12635). `AutoMergingRetriever`
tested hierarchy metadata for truthiness, so a legitimate `0` — the first level of a
document tree — was read as missing and the merge was skipped. The fix moves both
conditions to key presence, which separates *absent key* from *stored zero*. Three
files, +30/−2, with a regression test and a release note; unit and integration CI
passed on Linux, Windows and macOS. Reviewed and merged by a Haystack maintainer.

## City Gardens (team, 2023)

Le Wagon Barcelona team project. Rails and PostgreSQL, five people, not maintained since.

My merged pull requests: [parcel reservations](https://github.com/justdevelopin/CityGardens/pull/37), [add-event button](https://github.com/justdevelopin/CityGardens/pull/38), [logout](https://github.com/justdevelopin/CityGardens/pull/39), [styles](https://github.com/justdevelopin/CityGardens/pull/47), [fontsize](https://github.com/justdevelopin/CityGardens/pull/50). I also contributed event-index partials, a search bar and Cloudinary for event photos.

[Schema](https://github.com/justdevelopin/CityGardens/blob/master/db/schema.rb)

## Other public exercises

[DispatchOps](https://github.com/coder058/dispatchops) · [Transcript Desk](https://github.com/coder058/transcript-desk) · [Wikinimous](https://github.com/coder058/rails-wikinimous) · [Rails labs](https://github.com/coder058?tab=repositories&q=rails-)
