# Engineering decisions and checks

Notes from my independent projects: decisions, checks and things that did not work.

## Keep the loss in the postmortem

**Polybow: separate observed cash, reconstructed equity and causal inference.**
The public analysis and browser archive read the same anonymized ledger. The
postmortem distinguishes the observed liquid peak from a higher reconstructed
equity curve, reports the negative lifetime settled trading cash result, and
keeps incomplete bot attribution visible. Archived API-response timings are
scoped as acknowledgements, not fills. A documented exchange upgrade and later
performance deterioration overlap in time, but the evidence does not isolate a
single patch as the cause.

[Analysis and limits](https://github.com/coder058/polybow-case-study) ·
[Filter regression](https://github.com/coder058/polybow-case-study/blob/main/tests/ledger-ui.test.cjs)

## Preserve the original requirement

**Relay: make job research inspectable.** The implementation connects a React
interface, FastAPI service, public job-board data and HTTP/MCP tools. Reviews
retain source quotations and can be exported. Canonical URLs identify duplicates
without discarding changed listing text. A deliberately read-only scope keeps
research separate from submitting an application.

[Implementation and setup](https://github.com/coder058/relay) ·
[Validation and duplicate tests](https://github.com/coder058/relay/blob/main/backend/tests/test_job_evidence.py)

## Keep future candles out of replay

**Pattern Forge: make the chart usable and replay trustworthy.** The product
brief called for less clutter, separate chart/analysis controls and recorded
markets beyond crypto. The resulting workspace uses optional indicators and
recorded metals, index and crypto perpetuals. Replay only supplies candles up to
the cursor; incomplete aggregates are omitted rather than filled with guesses.
This trades apparent completeness for data integrity.

[Interface and trade-offs](https://github.com/coder058/pattern-forge) ·
[Closed-candle and malformed-input tests](https://github.com/coder058/pattern-forge/blob/main/tests/public-market.test.mjs)

## Search results are not a shortlist

**Relay: a keyword hit is not a hiring recommendation.** A real search for
Python returned a product-manager listing; the revised backend query returned
a senior role. Search, review and export worked, but eligibility was not
established. The walkthrough records those failures and the script's new query
option instead of declaring a successful match.

[Observed task, revision and limitations](https://github.com/coder058/relay/blob/main/JOB_SEARCH_WALKTHROUGH.md)

## Include queued work in arrival estimates

**DispatchOps: a small simulation experiment.** A second delivery starts at the
first delivery's destination. Breakdowns requeue unfinished jobs; a zone
restriction delays the affected route and downstream work. Browser testing
included reassignment after a breakdown and a complete shift. The public game
uses browser memory; its Express/SQLite API is a separate local demonstration.

[Queue and incident tests](https://github.com/coder058/dispatchops/blob/main/src/game.test.ts)

I use AI coding tools for implementation, debugging and tests, and review their
output. These are independent projects, not employment or claims of customer
adoption. Using agents during development is distinct from an AI feature in a product.
