
# Integration Guide

This guide describes how the **Fabric Run Logger pattern** can be integrated into Microsoft Fabric notebooks and pipelines.  
The goal is to create consistent, readable and investigation-friendly execution logs across the data platform.

The integration pattern focuses on:

- consistent stage logging
- structured run tracking
- easier failure investigation
- improved operational observability

---

# 1. Notebook Integration Pattern

A notebook should initialise the logger context at the start of execution and record key milestones during processing.

## Step 1 — Initialise logger context

At the beginning of the notebook run, resolve the basic runtime context.

Typical context values:

- `workspace_name`
- `pipeline_name` (or `job_name`)
- `run_id`

Example:

```python
run_id = get_current_run_id()

log(
    stage="Init",
    status="Started",
    message=f"Run {run_id} started",
    pipeline_name=pipeline_name
)
```

This establishes the beginning of the run narrative.

---

## Step 2 — Log key processing stages

During execution, major processing milestones should be logged.

Examples:

```python
log(stage="ReadSource", status="Started", message="Reading parquet files")
log(stage="Transform", status="Started", message="Applying business rules")
log(stage="Upsert", status="Completed", message="Inserted=X Updated=Y")
```

Typical stages may include:

- Init
- ReadSource
- Transform
- Validate
- Upsert
- Publish
- Notify
- Cleanup

Using consistent stage names helps make logs easier to interpret.

---

## Step 3 — Log failures explicitly

If an exception occurs, the failure should be logged with a clear stage and error message.

Example:

```python
log(
    stage="Transform",
    status="Failed",
    level="ERROR",
    message=str(e)
)
```

This allows operational teams to quickly identify the exact stage where the run failed.

---

## Step 4 — Persist structured run metadata (optional)

In addition to text-based logs, the run outcome can be recorded in a structured Delta table such as `System_Run_Log`.

Example:

```python
insert_system_run_log(
    ...,
    status="Failed",
    result_message="...",
    additional_metadata={...}
)
```

This enables:

- run history tracking
- monitoring dashboards
- operational reporting
- trend analysis

---

# 2. Pipeline Integration Pattern

Pipelines can integrate with the logger by calling logging notebooks or logging utilities at key orchestration points.

## Recommended approach

A pipeline typically:

1. Calls the logging notebook at the start of the run.
2. Executes activities such as copy operations, notebook execution or SQL steps.
3. Logs completion or failure of each stage.
4. Writes a final run summary.

Example pipeline structure:

```
Pipeline Start
↓
Logger Notebook (Run Start)
↓
Copy Activity
↓
Processing Notebook
↓
Validation Step
↓
Logger Notebook (Run End)
```

---

## Activity-level logging

Each activity should log important operational information such as:

- activity name
- start time
- end time
- number of records processed
- key metrics
- errors if any

Example:

```python
log(stage="CopyActivity", status="Completed", message="RowsCopied=12345")
```

This makes pipeline behaviour much easier to understand during troubleshooting.

---

# 3. Optional: Resolving Trigger Metadata

In some scenarios it may be useful to capture additional metadata about the trigger that started the run.

For example:

- trigger type (manual, schedule, event)
- triggering user
- parent pipeline

Microsoft Fabric environments may allow retrieving this information through platform helpers or Microsoft Graph integration.

However:

- this step is **optional**
- tokens or credentials should **never be persisted in logs**
- sensitive metadata should be handled carefully

---

# 4. Logging Reliability Considerations in Microsoft Fabric

One of the practical challenges encountered during the design of the Fabric Run Logger was the reliability of persisting log entries to file storage in Microsoft Fabric.

In normal conditions, appending a log line to a run log file is straightforward. However, during testing and operational use, there were cases where file append behaviour appeared inconsistent or non-deterministic.

Observed scenarios included:

- the append operation returning an exception even though the entry was eventually written
- the append call completing, but the log line not immediately visible when the file was read back
- delayed visibility of appended content
- repeated writes requiring verification to avoid silent failure or duplicate entries

Because of this behaviour, the logger design adopted a **defensive persistence strategy** rather than assuming that a single append operation would always succeed reliably.

---

# 5. Reliability Strategy

To mitigate intermittent or abnormal Fabric file-write behaviour, the logging framework applies several safeguards:

1. Ensure the target log folder exists before writing
2. Ensure the log file exists before append operations
3. Introduce a short random delay before writing to reduce write collisions
4. Attempt file append with bounded retries
5. Verify that the written log entry is actually present by reading the file back
6. Handle the case where append reports an error but the log entry was successfully persisted
7. Stop retrying if verification becomes uncertain, to avoid duplicated log lines

These mechanisms make the logging framework more resilient and increase confidence in the reliability of run logs.

---

# 6. Design Implication

The Fabric Run Logger is not simply a message formatter.

It acts as a **reliability wrapper around Fabric file persistence**, ensuring that operational logs remain dependable even when file-write behaviour is inconsistent.

This design makes the logger suitable for:

- production support
- operational monitoring
- pipeline failure investigation
- long-term run history analysis
