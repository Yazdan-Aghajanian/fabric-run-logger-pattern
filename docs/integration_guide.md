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
