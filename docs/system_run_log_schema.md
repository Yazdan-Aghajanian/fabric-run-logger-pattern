# System_Run_Log schema (suggested)

Use a Delta table to store structured run metadata. Fields can be adapted.

## Suggested columns
- `RUN_ID` (string): unique run identifier (pipeline run id / notebook job instance id)
- `WORKSPACE_NAME` (string)
- `OBJECT_TYPE` (string): Pipeline / Notebook
- `OBJECT_NAME` (string): pipeline/notebook name
- `OBJECT_SUBTYPE` (string): domain grouping (e.g. Lander / Silver / Gold / BAU)
- `STATUS` (string): Started / Succeeded / Failed / Warning / Cancelled
- `TRIGGER_TYPE` (string): Manual / Schedule / Event / API
- `TRIGGERED_BY` (string): user/service principal (if available)
- `START_TIME` (timestamp)
- `END_TIME` (timestamp)
- `DURATION_SEC` (double) or `DURATION_STR` (string)
- `RESULT_MESSAGE` (string): short summary or last error
- `ADDITIONAL_METADATA` (string/struct/map): JSON for flexible metadata
- `TAGS` (array<string>): optional labels
- `DESCRIPTION` (string): free text
- `LOG_PIPELINE_NAME` (string): parent pipeline if this entry is for a child object

## Notes
- Store timestamps in a consistent timezone or store UTC + a display timezone.
- Keep `RESULT_MESSAGE` concise; put verbose logs in OneLake Files.
