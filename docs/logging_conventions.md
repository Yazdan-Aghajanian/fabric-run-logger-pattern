
# Logging Conventions

This document defines the **standard logging format and conventions** used by the Fabric Run Logger pattern.

Consistent logging conventions make pipeline and notebook runs easier to read, analyse and troubleshoot.  
All logs should follow the same structure so that engineers and support teams can quickly understand the execution flow.

---

# 1. Log Line Format

Each log entry follows a consistent structure:

```
[YYYY-MM-DD HH:mm:ss] [LEVEL] [WORKSPACE] Stage: <stage> | Status: <status> | Message: <message>
```

Example:

```
[2026-03-10 14:22:11] [INFO] [NP-Fabric-Prod] Stage: Upsert | Status: Completed | Message: Inserted=145 Updated=32
```

This format ensures that logs remain:

- human-readable
- structured enough for parsing
- consistent across pipelines and notebooks

---

# 2. Log Levels

Log levels indicate the **severity and type of event**.

| Level | Purpose |
|-----|-----|
| INFO | Normal execution progress |
| WARNING | Unexpected behaviour that does not stop execution |
| ERROR | Failure condition or high‑risk issue |

### INFO

Used for normal execution steps such as:

- starting a stage
- completing a stage
- reporting record counts
- confirming successful actions

Example:

```
log(stage="ReadSource", status="Started", level="INFO", message="Reading parquet files")
```

---

### WARNING

Used when something unusual happens but execution continues.

Examples:

- optional input not found
- minor validation issue
- retry attempt triggered

Example:

```
log(stage="Validate", status="Warning", level="WARNING", message="Some optional columns were missing")
```

---

### ERROR

Used when execution fails or cannot safely continue.

Examples:

- transformation failure
- data integrity violation
- database write failure

Example:

```
log(stage="Transform", status="Failed", level="ERROR", message=str(e))
```

---

# 3. Status Values

Status values describe **the state of a stage or operation**.

Typical values include:

- Started
- InProgress
- Completed
- Succeeded
- Failed
- Skipped
- Separator

### Started

Indicates that a stage has begun.

Example:

```
Stage: ReadSource | Status: Started
```

---

### InProgress

Used when a long-running process is underway.

Example:

```
Stage: CopyActivity | Status: InProgress
```

---

### Completed

Used when a stage finished normally but is not necessarily the final stage.

Example:

```
Stage: Transform | Status: Completed
```

---

### Succeeded

Typically used for final run status or major milestone completion.

Example:

```
Stage: Run | Status: Succeeded
```

---

### Failed

Indicates that execution has stopped due to an error.

Example:

```
Stage: Upsert | Status: Failed
```

---

### Skipped

Used when a stage is intentionally bypassed.

Example:

```
Stage: Validate | Status: Skipped
```

---

### Separator

Used to visually separate major sections of the log output.

Example:

```
---------------------------------------------------------------
```

This improves readability during long pipeline runs.

---

# 4. Recommended Stage Names

Stages represent **major logical steps in the pipeline or notebook workflow**.

Using a stable set of stage names helps keep logs comparable between runs.

Recommended stages:

- Init
- ReadSource
- Transform
- Validate
- Upsert
- Publish
- Notify
- Cleanup

Example usage:

```
log(stage="Init", status="Started", message="Pipeline execution started")
log(stage="ReadSource", status="Completed", message="Source data loaded")
log(stage="Transform", status="Completed", message="Business rules applied")
log(stage="Upsert", status="Completed", message="Data written to Delta table")
```

---

# 5. Best Practices

### Keep messages concise

Log messages should clearly communicate what happened without excessive detail.

Good:

```
Inserted=145 Updated=32
```

Avoid:

```
Inserted 145 records into table after performing multiple transformations
and validations across different partitions.
```

---

### Log important milestones

Do not log every minor operation. Focus on key stages that help explain the run story.

Good milestones:

- reading data
- transformation completion
- Delta writes
- validations
- notifications

---

### Include key metrics

Whenever possible include metrics such as:

- rows processed
- rows inserted
- rows updated
- duration

Example:

```
Stage: Upsert | Status: Completed | Message: Inserted=1243 Updated=87 Duration=3.4s
```

---

### Use consistent stage naming

Avoid creating many different stage names for the same operation.

Consistency makes logs easier to analyse across pipelines.

---

# 6. Why These Conventions Matter

In large Fabric environments with many pipelines and notebooks, inconsistent logging can quickly become difficult to interpret.

Standard conventions ensure:

- predictable run narratives
- easier failure investigation
- simpler operational support
- reusable logging across projects
- better monitoring and reporting

The Fabric Run Logger pattern promotes these conventions to improve the reliability and clarity of operational logging.
