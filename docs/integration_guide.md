# Integration guide (pattern)

## In a notebook
1. Initialise logger context:
   - `workspace_name`
   - `pipeline_name` (or `job_name`)
   - `run_id`
2. Log key milestones:
   - `log(stage="Init", status="Started", message="...")`
   - `log(stage="Upsert", status="Completed", message="Inserted=X Updated=Y")`
3. On failure:
   - `log(stage="Transform", status="Failed", level="ERROR", message=str(e))`
4. Optionally write a structured record:
   - `insert_system_run_log(..., status="Failed", result_message="...", additional_metadata={...})`

## In a pipeline
- Call the notebook at the start/end of the pipeline to write a single “pipeline run header/footer”.
- Each activity (copy, notebook, SQL) should log:
  - activity name
  - start/end
  - key counts
  - errors

## Optional: resolve triggering user
In Fabric you can often obtain a Graph token with platform helpers. Keep this optional and do not store tokens.

## Logging reliability considerations in Microsoft Fabric

One of the practical challenges encountered during the design of the Fabric Run Logger was the reliability of persisting log entries to file storage in Microsoft Fabric.

In normal conditions, appending a log line to a run log file is straightforward. However, during testing and operational use, there were cases where file append behaviour appeared inconsistent or non-deterministic. In some scenarios:

- the append operation returned an exception even though the entry was eventually written
- the append call completed, but the log line was not immediately visible when the file was read back
- write visibility appeared delayed, requiring a short pause and re-check
- repeated writes needed verification to avoid either silent failure or duplicate entries

Because of this, the logger design adopted a more defensive persistence strategy rather than assuming that a single append operation was always reliable.

### Reliability strategy

The logging framework was designed with the following safeguards:

1. Ensure the target log folder exists before writing
2. Ensure the log file exists before append operations
3. Introduce a short random delay before writing to reduce write collisions
4. Attempt file append with bounded retries
5. Verify that the written log entry is actually present by reading the file back
6. Handle the case where append reports an error but the log entry was successfully persisted
7. Stop retrying if verification becomes uncertain, to avoid duplicated log lines

This behaviour was introduced to make the logger more resilient to intermittent or abnormal Fabric file-write behaviour and to improve trust in operational run logs.

### Design implication

This means the logger is not just a message formatter; it also acts as a reliability wrapper around Fabric file persistence. The goal is to produce operational logs that are dependable enough for run investigation, production support and failure diagnostics.
