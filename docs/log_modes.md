## Log modes and usage patterns

The Fabric Run Logger supports multiple log modes to standardise how different execution events are recorded. Each mode is designed for a specific operational scenario.

### Supported log modes

| Log Mode | Purpose | Typical Usage |
|----------|---------|---------------|
| 1 | Pipeline start | Records pipeline start event and trigger metadata |
| 2 | Waiting state | Indicates the pipeline is in a waiting or polling state |
| 3 | File save success | Logs successful save of a parquet or file-based output |
| 4 | Table write success | Logs successful copy or load into a Delta table |
| 5 | Copy activity details | Records detailed copy activity metadata such as duration, data movement and errors |
| 6 | Custom log message | General-purpose custom logging for arbitrary messages |
| 7 | Custom formatted message | Used for multi-line or specially formatted log content |
| 8 | Stage completion with separator | Logs stage completion and adds visual separation in the log |
| 9 | Successful end | Records successful completion of the pipeline run |
| 10 | Failure end | Records failure summary and error-related information |
| 11 | Script activity metadata | Logs script execution metadata such as rows returned, affected records and execution duration |

### Why log modes matter

The purpose of log modes is to avoid inconsistent free-text logging and provide a predictable structure across pipelines and notebooks.

This gives several operational benefits:

- consistent run narratives from start to finish
- easier troubleshooting during failed runs
- clearer separation between business stages and technical steps
- simpler parsing for downstream monitoring and reporting
- reusable logging behaviour across many notebooks and pipelines

### Recommended usage

In practice, log modes should be used as reusable event templates rather than one-off messages. For example:

- use mode 1 at the start of every orchestrated pipeline run
- use mode 5 when recording copy activity telemetry
- use mode 6 for targeted custom status updates
- use mode 8 when marking major milestones
- use mode 9 or 10 to clearly close the run with a final state

This structure helps make the run log readable for both developers and operational support teams.
