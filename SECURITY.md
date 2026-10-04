# Security policy

## Reporting a vulnerability

Please **do not** open a public issue. Report privately through GitHub's private vulnerability reporting on the affected repository (**Security → Report a vulnerability**), or via the hub repo: <https://github.com/Blockchains/blockchains.github.io/security/advisories/new>.

Include the affected repo/URL, impact, and steps to reproduce. We aim to acknowledge within 3 working days and to fix or mitigate critical issues within 14 days, and we will credit you unless you prefer otherwise.

## Scope

- Hub, tools, data API, SDK, MCP server, monitors and their GitHub Actions workflows.
- Smart contracts in `blockchainlab-labs` and `forge-example-*` are **intentionally educational** (several contain deliberate vulnerabilities for teaching). Reports about those are welcome but are not treated as security incidents.

## Supported versions

Only the latest `main` branch and the latest tagged release of the SDK and MCP server receive fixes.
