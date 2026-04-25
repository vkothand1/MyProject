---
title: "Agentic & Data Engineering Guidelines"
description: |
	Project-level guidance and guardrails for autonomous agents and contributors working
	on the AI Agentic + Data Engineering Python project. Use this file as the discovery
	surface for agent behaviors, coding standards, data engineering best-practices,
	and sample prompts/templates for common tasks.
---

# Agentic & Data Engineering Guide

Purpose: provide a single, detailed source of truth for how automated assistants
and humans should propose, implement, test, and ship changes to this repository.

This file is written for two audiences:
- the autonomous / semi-autonomous agents that assist in code and data work
- engineers onboarding to the project (data engineers, ML engineers, backend)

If you are an automated assistant reading this file, follow the sections below
strictly: ask clarifying questions when a requirement is underspecified, prefer
small iterative changes, always include tests, and never commit secrets.

**Agent persona and constraints**
- Purpose: helpful, conservative, test-first, and explainable.
- Tone: concise, action-oriented, with explicit assumptions and next steps.
- Change policy: do not push breaking changes to main branches without
	human approval. Default target branch for PRs is `feature/agent/*`.
- Safety: never exfiltrate secrets, PII, or credentials. If a task implies
	handling PII, require an explicit user confirmation and a compliance checklist.

**When to act vs when to ask**
- Act (make a PR) for clearly-specified, low-risk tasks: small refactors, lint
	fixes, docstrings, non-production data tests, and unit tests.
- Ask (clarify) for ambiguous or high-impact changes: schema changes, production
	pipeline topology changes, breaking API changes, infra or permission changes.

Repository overview (quick)
- `shopping_app/` — primary application code: config, DB access, emailer, guardrails,
	main entry points, UI and agents.
- `graph/` — state machine and workflow primitives.
- `marketplaces/` — marketplace adapters for Amazon, Costco, Target, Walmart.
- `skills/` — reusable skill assets (domain logic, templates, test helpers).
- `tests/` — test suite (unit + integration data tests).

If your change touches multiple directories above, explain cross-cutting impacts
in the PR description and include an integration test when feasible.

**Project coding guidelines (project style overrides)**
Follow these rules when writing Python in this repo. These are project-specific
decisions — prefer them even if they differ from broader community norms.

- Naming: use camelCase for variables, functions and class names across the repo.
- Naming: use PascalCase for class names that represent domain entities (consistent
	with camelCase decision above for functions/vars).
- Clarity: choose descriptive names that clearly indicate purpose (avoid single-letter
	names except in very small scopes).
- Functions: keep functions small, single-responsibility, and testable.
- Docstrings: add detailed docstrings for functions and classes (describe inputs,
	outputs, side effects, and complexity guarantees). Prefer Google-style or
	numpydoc style consistently.
- Type hints: annotate public functions and methods with type hints.
- Logging: use structured logging for long-running jobs; avoid print statements
	in production code.
- Error handling: prefer explicit exceptions and fail fast; add retry with
	exponential backoff for IO-bound operations.

Formatter and linters (recommended)
- Black for formatting, ruff/flake8 for linting, mypy for optional static typing.
- Add pre-commit hooks where appropriate.

Example local dev commands

```bash
# create and activate virtualenv
source .venv/bin/activate
# install deps
pip install -r requirements.txt
# run tests
pytest -q
# run lint/format
ruff . && black .
```

Data engineering principles and guardrails
- Schema-first: design and version schemas (JSONSchema, Avro, or SQL DDL) before
	transforming or storing data.
- Contracts: define data contracts for each ingestion interface. The contract must
	include field names, types, nullable, cardinality, and freshness expectations.
- Idempotence: all pipeline steps must be idempotent and safe to re-run.
- Incremental loads: prefer to do incremental updates with watermarks or offsets
	rather than full rewrites for large datasets.
- Partitioning & formats: use columnar formats (Parquet) and partition by date or
	logical keys for analytical datasets.
- Quality checks: add automated data quality checks (e.g., Great Expectations)
	for every dataset consumed/produced by a pipeline.
- Observability: emit counts, latency metrics, and error rates. Include sample
	queries/metrics dashboards in PRs that introduce new pipelines.
- Retention & governance: follow the project's retention policy; scrub PII and
	follow the compliance checklist before storing any sensitive fields.
