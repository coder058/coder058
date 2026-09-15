# Jordi Lluis

**Python & data software — market data, reconciliation and operational tools.**

Amsterdam · EU citizen. My background is in logistics operations and applied finance; the software below is independent project work, separate from employment.

[Portfolio](https://coder058.github.io/profile/) · [Résumé / ATS PDF](https://coder058.github.io/profile/resume.html) · [Email](mailto:joord918@gmail.com)

## Polybow — operated system, public postmortem

Built and operated a Python trading system on AWS Lightsail: WebSocket books, signed CLOB requests, cached market metadata and daily JSONL recordings. After live trading stopped, I investigated differences between bot records and account activity.

The public repository contains accounting, a timing parser, tests and an evidence map — **not the private bot or raw VPS recordings**. An API acknowledgement is not a fill. Attribution is incomplete and the run does not establish durable profitability.

[Engineering walkthrough](https://coder058.github.io/profile/projects/polybow.html) · [Code and tests](https://github.com/coder058/polybow-case-study) · [Evidence and corrections](https://github.com/coder058/polybow-case-study/blob/main/EVIDENCE.md)

**New, separate demonstrator:** [Reconciliation lab](https://coder058.github.io/profile/projects/reconciliation/) · [Python/PostgreSQL/FastAPI source](https://github.com/coder058/polybow-case-study/tree/main/reconciliation). Atomic imports reject conflicting event IDs; the report preserves partial fills and unknown attribution. [The verified CI run](https://github.com/coder058/polybow-case-study/actions/runs/34887365171) exercised concurrent redelivery, rollback and database restart recovery. The public page is a static export of **synthetic fixtures**, not historical account data or a hosted production API.

## Pattern Forge — time-boundary replay and persistence

React/TypeScript workspace with validated candle snapshots, a separate live quote stream, prefix-only replay and a Python/PostgreSQL ingestion path. Tests exclude future candles and incomplete timeframes; CI checks Docker and persistence across a restart.

[Interactive demo](https://pattern-forge-five.vercel.app/) · [Code](https://github.com/coder058/pattern-forge) · [Ingest](https://github.com/coder058/pattern-forge/tree/main/ingest) · [CI](https://github.com/coder058/pattern-forge/actions/workflows/check.yml)

The public demo uses recordings and temporary process memory, not hosted PostgreSQL. Local/CI database capability is not a claim about the deployed demo.

## Info Desk — evidence retrieval with controlled writes

Python/FastAPI and SQLite: versioned source captures, quoted evidence and human approval before publishing notes. Tests cover invalid citations and interrupted jobs.

[Recorded public case](https://coder058.github.io/info-desk/) · [Code](https://github.com/coder058/info-desk) · [Runnable retrieval evaluation](https://github.com/coder058/info-desk/tree/main/evals)

The live research workspace runs locally. The evaluation publishes cross-language misses and unanswerable-question limitations; it is not a model-accuracy benchmark or proof of a production AI service.

## Open source — merged Haystack contribution

[Haystack #12635](https://github.com/deepset-ai/haystack/pull/12635): fixed hierarchy-metadata validation that treated a stored zero as missing. Added a regression test and release note; reviewed and merged by a maintainer. The diff and review show the scope of this focused contribution.

## Earlier team and additional work

[City Gardens](https://github.com/justdevelopin/CityGardens), Le Wagon team project (2023): my merged work includes [parcel reservations](https://github.com/justdevelopin/CityGardens/pull/37), [add-event button](https://github.com/justdevelopin/CityGardens/pull/38), [logout](https://github.com/justdevelopin/CityGardens/pull/39) and styling. Shared authorship; not maintained as a product.

[Relay](https://github.com/coder058/relay): one Python matcher behind HTTP and MCP. Public backend unavailable; use the repository's local instructions. [DispatchOps](https://github.com/coder058/dispatchops): an operations-inspired prototype, not a deployed warehouse system.

I use AI-assisted development and remain responsible for understanding, testing and reviewing the resulting code. Repository evidence is not a substitute for professional employment years.
