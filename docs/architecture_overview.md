
# Architecture Overview

## Purpose

The Fabric Run Logger is designed to provide a **high-level operational logging framework** for Microsoft Fabric pipelines and notebooks.

Microsoft Fabric provides internal execution logs for platform-level activity, but in complex data platforms this is often not enough for day-to-day operational support. Engineers and support teams typically also need a business-readable run narrative that clearly shows:

- when a run started
- which major stages were executed
- what key actions were performed
- where a failure happened
- what the final outcome was

The purpose of the Fabric Run Logger is to complement Fabric’s internal logs with a consistent, structured and investigation-friendly execution trail.

---

## Problem Statement

In many Microsoft Fabric solutions, default logs are useful for internal platform behaviour, but they are not always ideal for answering practical operational questions such as:

- Which stage failed in this run?
- Did the notebook reach the Delta upsert step?
- Did the copy activity complete successfully?
- Was the failure during data read, transformation, persistence or notification?
- What was the full A-to-Z story of this run?

Without a high-level logger, investigation often becomes slower and more manual, especially when multiple pipelines and notebooks are involved.

The Fabric Run Logger was created to solve this gap.

---

## Core Objectives

The framework is designed around the following objectives:

1. **High-level observability**  
   Provide a clear A-to-Z view of each pipeline or notebook run.

2. **Consistent structure**  
   Ensure logs follow a standard pattern across different workloads.

3. **Faster troubleshooting**  
   Make it easier to identify the exact stage and message associated with a failed run.

4. **Operational reporting**  
   Support structured run tracking through a Delta table such as `System_Run_Log`.

5. **Reusable design**  
   Enable the same logging pattern to be reused across multiple Fabric notebooks and pipelines.

---

## Architectural Layers

The Fabric Run Logger can be understood as a set of cooperating layers.

### 1. Runtime Context Layer

This layer is responsible for establishing the execution context for the current run.

Typical responsibilities include:

- identifying the current workspace
- identifying the current pipeline or notebook
- resolving the current run ID
- resolving trigger metadata where available
- determining the target log file path
- preparing shared execution metadata

This layer ensures that every log entry is associated with the correct run context.

---

### 2. Logging Layer

This is the core layer responsible for writing high-level run events.

Typical responsibilities include:

- formatting a standard log line
- applying consistent `stage`, `status`, `level` and `message` conventions
- printing log entries to notebook output
- writing log entries to file storage
- ensuring readable run narratives

This layer turns pipeline and notebook execution into an ordered, human-readable story.

---

### 3. Structured Persistence Layer

This layer stores run metadata in a structured queryable form, typically in a Delta table such as `System_Run_Log`.

Typical responsibilities include:

- recording run start and end state
- storing execution duration
- storing final result status
- storing summary messages
- storing additional run metadata
- supporting reporting, trend analysis and support dashboards

This layer allows operational questions to be answered using structured data rather than raw text logs alone.

---

### 4. Diagnostics and Investigation Layer

This layer helps reconstruct and investigate pipeline and notebook runs after execution.

Typical responsibilities include:

- reading existing log files
- detecting run start and run end
- locating failure points
- identifying the stage of failure
- extracting useful operational summaries
- supporting post-run troubleshooting

This is especially important when investigating failed or partially completed runs.

---

### 5. Reporting Layer

This optional layer converts raw and structured logging outputs into report-friendly formats.

Typical responsibilities include:

- creating HTML summaries
- summarising copy activities
- summarising Delta operations
- supporting email notifications or support reports
- presenting run outcomes in a concise operational format

This layer is useful when the logger is integrated with run reporting or alerting mechanisms.

---

## High-Level Execution Flow

At a high level, the framework follows this execution pattern:

Pipeline / Notebook Run  
↓  
Initialise Logger Context  
↓  
Write Run Start Log  
↓  
Log Each Major Stage (Read → Transform → Validate → Upsert → Notify → Cleanup)  
↓  
Capture Exceptions and Failure Details  
↓  
Write Final Run Status  
↓  
Persist Structured Run Record (System_Run_Log)  
↓  
Optional Reporting / Investigation Output

---

## Logging Reliability Considerations in Microsoft Fabric

One of the practical challenges encountered during the design of the Fabric Run Logger was the reliability of persisting log entries to file storage in Microsoft Fabric.

In normal conditions, appending a log line to a run log file is straightforward. However, during testing and operational use, there were cases where file append behaviour appeared inconsistent or non-deterministic. In some scenarios:

- the append operation returned an exception even though the entry was eventually written
- the append call completed, but the log line was not immediately visible when the file was read back
- write visibility appeared delayed, requiring a short pause and re-check
- repeated writes needed verification to avoid either silent failure or duplicate entries

Because of this, the logger design adopted a more defensive persistence strategy rather than assuming that a single append operation was always reliable.

### Reliability Strategy

The logging framework was designed with the following safeguards:

1. Ensure the target log folder exists before writing
2. Ensure the log file exists before append operations
3. Introduce a short random delay before writing to reduce write collisions
4. Attempt file append with bounded retries
5. Verify that the written log entry is actually present by reading the file back
6. Handle the case where append reports an error but the log entry was successfully persisted
7. Stop retrying if verification becomes uncertain, to avoid duplicated log lines

This behaviour was introduced to make the logger more resilient to intermittent or abnormal Fabric file-write behaviour and to improve trust in operational run logs.

### Design Implication

This means the logger is not just a message formatter; it also acts as a reliability wrapper around Fabric file persistence. The goal is to produce operational logs that are dependable enough for run investigation, production support and failure diagnostics.

---

## Design Principles

The Fabric Run Logger follows several key design principles.

### Readable
Logs should be understandable by developers, support teams and operational stakeholders.

### Consistent
The same logging structure should be applied across pipelines and notebooks.

### Traceable
Every run should be reconstructable from start to finish.

### Operational
The logger should support real production troubleshooting, not just development-time debugging.

### Structured
Where possible, important run information should also be stored in structured form for analysis and reporting.

### Reusable
The architecture should be reusable across multiple projects and environments.

---

## Why This Pattern Matters

A Fabric solution may contain many notebooks, pipelines, copy activities, Delta operations and notification steps. When a run fails, support teams need to quickly identify:

- what was running
- where the run reached
- what failed
- what happened just before failure
- whether the run completed any major business steps

A structured high-level logger reduces investigation time and improves confidence in production operations.

This is the central value of the Fabric Run Logger pattern.

---

## Scope of This Public Repository

This public repository shares the **architecture, design patterns and usage guidance** for the Fabric Run Logger.

It intentionally excludes:

- full implementation code
- environment-specific configuration
- internal paths and storage names
- organisation-specific logic
- secrets, credentials or sensitive identifiers

The goal is to provide a reusable design reference for implementing a similar logging framework in other Microsoft Fabric environments.
