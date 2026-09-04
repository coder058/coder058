# Engineering decisions and checks

Independent full-stack development, with AI coding tools involved in task
breakdown, implementation, debugging, refactoring and verification. The work
is not represented as unaided manual authorship or employment at these projects.
I set product priorities and review results against source evidence and tests.

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

## From a product goal to working software

**Relay: make job research inspectable.** The implementation connects a React
interface, FastAPI service, public job-board data and HTTP/MCP tools. Reviews
retain source quotations and can be exported. Canonical URLs identify duplicates
without discarding changed listing text. A deliberately read-only scope keeps
research separate from submitting an application.

[Implementation and setup](https://github.com/coder058/relay) ·
[Validation and duplicate tests](https://github.com/coder058/relay/blob/main/backend/tests/test_job_evidence.py)

## Feedback, experimentation and technical trade-offs

**Pattern Forge: make the chart usable and replay trustworthy.** The product
brief called for less clutter, separate chart/analysis controls and recorded
markets beyond crypto. The resulting workspace uses optional indicators and
recorded metals, index and crypto perpetuals. Replay only supplies candles up to
the cursor; incomplete aggregates are omitted rather than filled with guesses.
This trades apparent completeness for data integrity.

[Interface and trade-offs](https://github.com/coder058/pattern-forge) ·
[Closed-candle and malformed-input tests](https://github.com/coder058/pattern-forge/blob/main/tests/public-market.test.mjs)

## Critical validation, not acceptance of plausible output

**Relay: a keyword hit is not a hiring recommendation.** A real search for
Python returned a product-manager listing; the revised backend query returned
a senior role. Search, review and export worked, but eligibility was not
established. The walkthrough records those failures and the script's new query
option instead of declaring a successful match.

[Observed task, revision and limitations](https://github.com/coder058/relay/blob/main/JOB_SEARCH_WALKTHROUGH.md)

These are inspectable engineering examples, not measured productivity gains,
customer-adoption claims or proof of unattended AI reliability. Using agents to
build software is distinct from adding an AI feature to the product.
