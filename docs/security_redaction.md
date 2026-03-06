# Security and redaction checklist (public repo)

Before publishing anything:
- Remove/replace:
  - workspace/lakehouse names
  - OneLake paths and storage account names
  - tenant IDs, subscription IDs, client IDs
  - any tokens, bearer headers, API responses containing user info
  - internal table names if they reveal business structure (optional)
- Prefer placeholders:
  - `<WORKSPACE_NAME>`, `<LAKEHOUSE_NAME>`, `<PIPELINE_NAME>`, `<RUN_ID>`
- Keep the public repo focused on:
  - architecture, patterns, schema, conventions
  - minimal safe snippets (pseudocode)
