
# Security and Redaction Guidelines (Public Repository)

This document provides guidance on **what must be removed or sanitised** before publishing any code, documentation, or examples related to the Fabric Run Logger pattern.

The purpose is to ensure that the public repository shares **architecture and design patterns** without exposing environment-specific information, credentials, or sensitive operational details.

---

# 1. Principle

The public repository should contain **design knowledge**, not **environment details**.

Safe content includes:

- architecture explanations
- logging conventions
- pseudocode examples
- interface definitions
- schema design
- integration patterns

Sensitive or environment-specific information must **never be published**.

---

# 2. Items That Must Be Removed or Sanitised

Before publishing any content, verify that the following items are **not present in the public repository**.

### Environment Names

Remove or replace:

- Fabric workspace names
- Lakehouse names
- Environment labels (e.g. DEV / TEST / PROD naming conventions)

Example replacement:

```
<WORKSPACE_NAME>
<LAKEHOUSE_NAME>
```

---

### Storage and Path Information

Do not expose:

- OneLake paths
- storage account names
- container names
- internal directory structures

Example replacement:

```
<LOG_BASE_PATH>
<ONELAKE_PATH>
```

---

### Cloud Identifiers

Remove identifiers such as:

- Tenant IDs
- Subscription IDs
- Client IDs
- Service principal identifiers

These identifiers should **never appear in public documentation or examples**.

---

### Credentials and Tokens

Never publish:

- access tokens
- bearer tokens
- API keys
- connection strings
- secrets
- authentication headers

Even expired tokens should be removed to avoid accidental exposure patterns.

---

### API Responses Containing User Data

Avoid publishing raw responses from APIs such as:

- Microsoft Graph responses
- identity metadata
- user profile information
- email addresses

If examples are necessary, replace values with placeholders.

---

### Internal Table or Schema Names

In some organisations, table names can reveal business structures or internal systems.

If necessary, replace them with generic examples such as:

```
<System_Run_Log>
<DATA_TABLE>
<PIPELINE_LOG_TABLE>
```

---

# 3. Use Placeholders Instead of Real Values

When examples require identifiers, always use placeholders.

Recommended placeholders:

```
<WORKSPACE_NAME>
<LAKEHOUSE_NAME>
<PIPELINE_NAME>
<RUN_ID>
<LOG_BASE_PATH>
<STORAGE_PATH>
```

Example pseudocode:

```python
log(
    stage="Init",
    status="Started",
    message="Run started",
    pipeline_name="<PIPELINE_NAME>"
)
```

Using placeholders ensures that examples remain understandable without exposing environment details.

---

# 4. Code Examples in Public Documentation

The public repository should only contain:

- simplified pseudocode
- interface signatures
- architecture diagrams

Avoid publishing:

- full implementation code
- environment-specific configuration
- real production paths

Example:

Safe:

```python
run_id = get_current_run_id()
log(stage="Init", status="Started", message="Run started")
```

Avoid:

```python
log_file_path = "/lakehouse/default/Files/system_logs/prod_pipeline_log.txt"
```

---

# 5. Repository Scope

The public repository intentionally focuses on:

- architectural design
- logging conventions
- system run log schema
- integration patterns
- reliability considerations

The **complete implementation** of the Fabric Run Logger framework should remain in a **private repository**.

---

# 6. Final Checklist Before Publishing

Before committing new documentation or examples, confirm that:

- no workspace names appear
- no storage paths appear
- no cloud identifiers appear
- no tokens or credentials appear
- no internal system details are exposed
- all identifiers use placeholders

If any of these appear, they must be replaced or removed before publishing.

---

# 7. Why This Matters

Sharing architecture patterns publicly can benefit the community, but exposing internal infrastructure details can create security risks.

Applying a strict redaction process ensures that the repository:

- remains safe to publish
- protects internal environments
- still communicates valuable design knowledge

This approach allows the Fabric Run Logger pattern to be shared responsibly while keeping the full operational implementation private.
