# Fabric Pipeline Logger (Public)

A pattern for building **high-level, A-to-Z run observability** in Microsoft Fabric pipelines and notebooks—focused on *your* business stages, not Fabric’s internal engine steps.

This public repository shares the **procedure, architecture, and templates** (not the full implementation).

## Why
Fabric’s default logs are great for internal execution details, but for operational support you often need:
- a single, readable run narrative (start → finish)
- consistent stage/status messages across pipelines + notebooks
- a structured run table for querying failures, durations, and trends

## Key components
1. **Text log writer (OneLake Files)**
   - Writes lines like:
     - `[timestamp] [LEVEL] [workspace] Stage: X | Status: Y | Message: Z`
   - Stored by pipeline and date for easy retrieval.

2. **Structured run table (Delta)**
   - A `System_Run_Log` Delta table (or similar) to support BI/reporting and governance.

3. **Run analyser**
   - Reads log files for a given pipeline/run window and extracts:
     - duration, errors, failure hints
     - summaries of copy activities and delta-table operations (optional)

## Repository layout
- `docs/` – setup guide, schema, and recommended conventions
- `templates/` – example schemas and log-line conventions
- `examples/` – how to embed the pattern in pipelines/notebooks (pseudocode)

## What’s intentionally not included
- Environment-specific paths/names
- Full code implementation
- Any organisation-specific logic, identifiers, or secrets

## Implementation

The full implementation of the Fabric Run Logger framework is maintained in a private repository.

This public repository provides:
- architecture
- design patterns
- logging conventions
- example usage

The goal is to share the implementation approach without exposing environment-specific production code.
