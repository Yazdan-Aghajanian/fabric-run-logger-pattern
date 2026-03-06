# Logging conventions

## Log line format (example)
`[YYYY-MM-DD HH:mm:ss] [LEVEL] [WORKSPACE] Stage: <stage> | Status: <status> | Message: <message>`

## Levels
- INFO: normal progress
- WARNING: unexpected but non-fatal behaviour
- ERROR: failure or high-risk condition

## Status values (example)
- Started
- InProgress
- Completed
- Succeeded
- Failed
- Skipped
- Separator (prints a visual divider)

## Stages
Use a stable set of stages so logs are comparable between runs, e.g.
- Init
- ReadSource
- Transform
- Upsert
- Validate
- Publish
- Notify
- Cleanup
