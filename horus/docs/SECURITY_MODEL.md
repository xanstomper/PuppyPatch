# Security Model

- Destructive commands require approval.
- Protected files cannot be edited by write tools.
- Secrets are redacted from logs.
- Push/deploy/delete are classified destructive.
- All file writes create checkpoints.
