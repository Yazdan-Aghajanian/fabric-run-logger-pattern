"""
Fabric Run Logger – Public Interface
Reference interface for the Fabric Run Logger pattern.
Implementation intentionally excluded from public repository.
"""

def log(stage: str, status: str, message: str, level: str = "INFO") -> None:
    """Write a standardised log entry."""
    pass


def build_log_line(timestamp: str, level: str, workspace_name: str,
                   stage: str, status: str, message: str) -> str:
    """Construct a standard log line."""
    pass


def get_current_run_id() -> str:
    """Resolve the current notebook job ID or pipeline run ID."""
    pass


def insert_system_run_log(run_id: str, workspace_name: str,
                          object_type: str, object_name: str,
                          status: str, start_time: str) -> None:
    """Insert a structured run log record."""
    pass
