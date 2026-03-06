
# System_Run_Log Schema

This document describes the **recommended schema** for storing structured run metadata produced by the Fabric Run Logger pattern.

The purpose of the `System_Run_Log` table is to capture **run-level execution metadata** for Microsoft Fabric pipelines and notebooks so that runs can be:

- queried
- monitored
- audited
- analysed
- reported

This structured record complements the text-based run logs written to OneLake files.

---

# 1. Purpose of the Table

The `System_Run_Log` table provides a **structured operational record** of pipeline and notebook executions.

Typical use cases include:

- tracking pipeline execution history
- identifying failed runs
- analysing execution duration
- building operational dashboards
- supporting production troubleshooting

While file-based logs provide detailed step-by-step messages, this table provides **high-level structured metadata for each run**.

---

# 2. Recommended Table Type

The table should be implemented as a **Delta table** within a Fabric Lakehouse.

Benefits include:

- ACID transactions
- schema evolution support
- efficient querying
- compatibility with Spark and SQL workloads

Example table location:

```
Lakehouse / Tables / System_Run_Log
```

---

# 3. Suggested Columns

The following columns are recommended for a flexible and operationally useful run log schema.

| Column | Type | Description |
|------|------|-------------|
| RUN_ID | string | Unique run identifier (pipeline run id or notebook job instance id) |
| WORKSPACE_NAME | string | Fabric workspace where the run executed |
| OBJECT_TYPE | string | Type of object (Pipeline / Notebook) |
| OBJECT_NAME | string | Name of the pipeline or notebook |
| OBJECT_SUBTYPE | string | Logical grouping (e.g. Lander / Silver / Gold / BAU) |
| STATUS | string | Run status (Started / Succeeded / Failed / Warning / Cancelled) |
| TRIGGER_TYPE | string | Run trigger (Manual / Schedule / Event / API) |
| TRIGGERED_BY | string | User or service principal that initiated the run |
| START_TIME | timestamp | Run start timestamp |
| END_TIME | timestamp | Run end timestamp |
| DURATION_SEC | double | Execution duration in seconds |
| DURATION_STR | string | Optional formatted duration string |
| RESULT_MESSAGE | string | Short run summary or final error message |
| ADDITIONAL_METADATA | string / map / struct | Flexible metadata stored as JSON |
| TAGS | array<string> | Optional classification labels |
| DESCRIPTION | string | Free-text description |
| LOG_PIPELINE_NAME | string | Parent pipeline name if this entry represents a child object |

---

# 4. Example Record

Example run entry:

```
RUN_ID: 43c7d6f2
WORKSPACE_NAME: <WORKSPACE_NAME>
OBJECT_TYPE: Pipeline
OBJECT_NAME: PL_Brz_Opt_Lander
OBJECT_SUBTYPE: Bronze
STATUS: Succeeded
TRIGGER_TYPE: Schedule
TRIGGERED_BY: <SERVICE_PRINCIPAL>
START_TIME: 2026-03-10 12:01:11
END_TIME: 2026-03-10 12:04:33
DURATION_SEC: 202
RESULT_MESSAGE: Pipeline completed successfully
```

This record represents a **single pipeline run summary**.

---

# 5. Relationship to File-Based Logs

The `System_Run_Log` table stores **run-level metadata**, while detailed execution messages are written to **file-based logs**.

Typical relationship:

| Layer | Storage |
|------|------|
| Run metadata | Delta table (`System_Run_Log`) |
| Detailed execution log | OneLake Files |
| Stage-level messages | File-based log |
| Run summary | Structured table record |

This separation ensures:

- fast structured queries
- detailed investigation when needed

---

# 6. Additional Metadata

The `ADDITIONAL_METADATA` field allows storing structured JSON metadata.

Examples:

```
{
  "records_inserted": 145,
  "records_updated": 32,
  "copy_duration": 14.3,
  "source_system": "Optomate"
}
```

Using flexible metadata prevents the schema from needing constant structural changes.

---

# 7. Timezone Considerations

To avoid confusion across environments, timestamps should follow a consistent policy.

Recommended approaches:

Option 1:

Store timestamps in **UTC**.

Option 2:

Store timestamps in local time and include a timezone reference.

Example:

```
2026-03-10T12:01:11Z
```

Consistency is more important than the specific format chosen.

---

# 8. Query Examples

Example: Retrieve failed runs

```sql
SELECT *
FROM System_Run_Log
WHERE STATUS = 'Failed'
ORDER BY START_TIME DESC
```

Example: Average pipeline duration

```sql
SELECT
    OBJECT_NAME,
    AVG(DURATION_SEC) AS avg_duration
FROM System_Run_Log
GROUP BY OBJECT_NAME
```

Example: Runs triggered manually

```sql
SELECT *
FROM System_Run_Log
WHERE TRIGGER_TYPE = 'Manual'
```

---

# 9. Best Practices

### Keep RESULT_MESSAGE concise

Store only the final summary or error message.

Verbose logs should remain in the file-based logs.

---

### Ensure RUN_ID uniqueness

The run identifier should uniquely represent the execution instance.

---

### Avoid storing sensitive information

Do not store credentials, tokens, or sensitive identifiers in this table.

---

### Use structured metadata carefully

If metadata becomes large or complex, consider extracting key metrics into separate columns.

---

# 10. Why This Table Matters

Without structured run metadata, operational troubleshooting often requires manually searching log files.

The `System_Run_Log` table enables:

- quick failure identification
- historical run tracking
- operational dashboards
- SLA monitoring
- pipeline reliability analysis

Together with the Fabric Run Logger file logs, it forms a **complete operational logging system** for Fabric data platforms.
