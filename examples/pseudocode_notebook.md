# Example pseudocode

```python
# at start
run_id = get_current_job_instance_id()  # or pipeline run id
log(stage="Init", status="Started", level="INFO", message=f"Run {run_id} started", pipeline_name=pipeline_name)

try:
    log(stage="ReadSource", status="Started", message="Reading parquet...", pipeline_name=pipeline_name)
    df = spark.read.parquet(source_path)

    log(stage="Transform", status="Started", message="Applying business rules...", pipeline_name=pipeline_name)
    df2 = transform(df)

    log(stage="Upsert", status="Started", message="Upserting to Delta...", pipeline_name=pipeline_name)
    upsert(df2)

    log(stage="Notify", status="Completed", message="Email sent", pipeline_name=pipeline_name)

    insert_system_run_log(..., status="Succeeded", result_message="Completed", start_time=..., duration=...)
except Exception as e:
    log(stage="Run", status="Failed", level="ERROR", message=str(e), pipeline_name=pipeline_name)
    insert_system_run_log(..., status="Failed", result_message=str(e))
    raise
```
