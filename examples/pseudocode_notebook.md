
# Fabric Run Logger – Public Interface Design

This document provides the **public architecture and interface design** for the Fabric Run Logger pattern.
The actual implementation is intentionally excluded from the public repository.

---

# -----------------------------------------------------------------------------
# 1. Core Logging API
# -----------------------------------------------------------------------------

```python
def log(
    stage: str,
    status: str,
    message: str,
    level: str = "INFO",
    pipeline_name: str | None = None,
    workspace_name: str | None = None,
    log_file_path: str | None = None,
    print_to_console: bool = True,
    write_to_file: bool = True
) -> None:
    """Write a standardised high‑level log entry for a Fabric pipeline or notebook run."""


def build_log_line(
    timestamp: str,
    level: str,
    workspace_name: str,
    stage: str,
    status: str,
    message: str
) -> str:
    """Construct a standard log line using the agreed logging format."""


def write_log_to_file(
    log_file_path: str,
    log_line: str,
    append: bool = True
) -> None:
    """Persist a log line to a OneLake / Files-based log target."""


def print_log(
    log_line: str
) -> None:
    """Print a formatted log line to notebook output for immediate visibility."""
```

---

# -----------------------------------------------------------------------------
# 2. Runtime Context
# -----------------------------------------------------------------------------

```python
def initialise_logger_context(
    workspace_name: str,
    object_name: str,
    object_type: str,
    run_id: str,
    parent_pipeline_name: str | None = None,
    trigger_type: str | None = None,
    triggered_by: str | None = None,
    log_base_path: str | None = None
) -> dict:
    """Create and return the runtime context required by the logging framework."""


def get_current_run_id() -> str:
    """Resolve the current notebook job ID or pipeline run ID."""


def get_current_workspace_name() -> str:
    """Resolve the current Fabric workspace name."""


def get_trigger_metadata() -> dict:
    """Resolve trigger metadata such as trigger type and user context."""


def build_log_file_path(
    log_base_path: str,
    pipeline_name: str,
    run_date: str,
    run_id: str | None = None
) -> str:
    """Build the target path for a run log file."""
```

---

# -----------------------------------------------------------------------------
# 3. Structured Run Logging (Delta Table)
# -----------------------------------------------------------------------------

```python
def insert_system_run_log(
    run_id: str,
    workspace_name: str,
    object_type: str,
    object_name: str,
    status: str,
    start_time: str,
    end_time: str | None = None,
    duration_seconds: float | None = None,
    trigger_type: str | None = None,
    triggered_by: str | None = None,
    result_message: str | None = None,
    additional_metadata: dict | None = None,
    log_pipeline_name: str | None = None
) -> None:
    """Insert a structured run‑level record into the System_Run_Log Delta table."""


def ensure_system_run_log_table_exists(
    table_name: str,
    schema_definition: dict | None = None
) -> None:
    """Ensure the System_Run_Log Delta table exists."""


def build_system_run_log_record(
    run_id: str,
    workspace_name: str,
    object_type: str,
    object_name: str,
    status: str,
    start_time: str,
    end_time: str | None,
    duration_seconds: float | None,
    result_message: str | None,
    additional_metadata: dict | None = None
) -> dict:
    """Build a structured run metadata record ready for persistence."""
```

---

# -----------------------------------------------------------------------------
# 4. Time Utilities
# -----------------------------------------------------------------------------

```python
def get_current_timestamp() -> str:
    """Return the current timestamp in the framework's standard format."""


def calculate_duration_seconds(
    start_time: str,
    end_time: str
) -> float:
    """Calculate execution duration in seconds."""


def format_duration(
    duration_seconds: float
) -> str:
    """Convert raw duration seconds into a readable string."""
```

---

# -----------------------------------------------------------------------------
# 5. Error Handling
# -----------------------------------------------------------------------------

```python
def log_exception(
    exc: Exception,
    stage: str,
    pipeline_name: str | None = None,
    workspace_name: str | None = None
) -> None:
    """Log an exception using the framework's standard error format."""


def extract_error_message(
    exc: Exception
) -> str:
    """Extract and normalise an exception message."""


def build_failure_summary(
    stage: str,
    error_message: str,
    run_id: str | None = None
) -> str:
    """Build a concise failure summary."""
```

---

# -----------------------------------------------------------------------------
# 6. Log Analysis
# -----------------------------------------------------------------------------

```python
def read_log_file(
    log_file_path: str
) -> list[str]:
    """Read a previously written run log file."""


def filter_log_lines_by_time_window(
    log_lines: list[str],
    start_time: str,
    end_time: str
) -> list[str]:
    """Restrict log lines to a target execution window."""


def find_run_start(
    log_lines: list[str]
) -> str | None:
    """Detect run start time."""


def find_run_end(
    log_lines: list[str]
) -> str | None:
    """Detect run end time."""


def detect_run_status(
    log_lines: list[str]
) -> str:
    """Determine whether the run succeeded or failed."""


def find_failure_point(
    log_lines: list[str]
) -> dict | None:
    """Identify the stage where the run failed."""


def build_run_investigation_summary(
    log_lines: list[str]
) -> dict:
    """Produce a troubleshooting summary."""
```

---

# -----------------------------------------------------------------------------
# 7. Reporting Helpers
# -----------------------------------------------------------------------------

```python
def build_copy_activity_html(
    copy_activity_records: list[dict]
) -> str:
    """Build an HTML summary table for copy activities."""


def build_delta_activity_html(
    delta_activity_records: list[dict]
) -> str:
    """Build an HTML summary table for Delta operations."""


def build_run_summary_html(
    run_summary: dict
) -> str:
    """Build an HTML run summary."""
```

---

# -----------------------------------------------------------------------------
# 8. Example Orchestration Flow
# -----------------------------------------------------------------------------

```python
def run_pipeline_with_logging():

    run_id = get_current_run_id()

    log(stage="Init", status="Started", message=f"Run {run_id} started")

    try:

        log(stage="ReadSource", status="Started", message="Reading data")
        df = spark.read.parquet("source_path")

        log(stage="Transform", status="Started", message="Applying rules")
        df2 = transform(df)

        log(stage="Upsert", status="Started", message="Writing to Delta")
        upsert(df2)

        log(stage="Notify", status="Completed", message="Email sent")

        insert_system_run_log(
            run_id=run_id,
            workspace_name="workspace",
            object_type="Notebook",
            object_name="example",
            status="Succeeded",
            start_time="..."
        )

    except Exception as e:

        log(stage="Run", status="Failed", level="ERROR", message=str(e))

        insert_system_run_log(
            run_id=run_id,
            workspace_name="workspace",
            object_type="Notebook",
            object_name="example",
            status="Failed",
            start_time="...",
            result_message=str(e)
        )

        raise
```

---

# High‑Level Architecture

Pipeline / Notebook  
↓  
Initialise Logger Context  
↓  
Write Run Start Log  
↓  
Log Each Stage (Read → Transform → Upsert → Validate → Notify)  
↓  
Capture Errors  
↓  
Write Final Run Status  
↓  
Insert Structured Run Record (System_Run_Log)  
↓  
Optional Reporting / Monitoring
