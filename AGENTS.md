# AGENTS.md: .github

Instructions for AI coding agents (Grok, Cursor, Claude Code, Codex, Copilot and others) working **in** this repo or **using it as a building block**. Humans: see [README.md](README.md).

## What this is

Org-wide defaults (issue/PR templates, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY) plus the building-block docs: BUILD-WITH-BLOCKS.md, BLOCKS-SCHEMA.md, blocks.schema.json and the workflow that validates every repo's blocks.json.

- Kind: docs, automation · stability: `stable` · licence: NOASSERTION
- Machine-readable manifest: [`blocks.json`](blocks.json) (schema: [BLOCKS-SCHEMA](https://github.com/Blockchains/.github/blob/main/docs/BLOCKS-SCHEMA.md))
- How it fits with the other Blockchains repos: [Build with Blocks](https://github.com/Blockchains/.github/blob/main/docs/BUILD-WITH-BLOCKS.md)

## Setup

```bash
pip install jsonschema
```

## Build and test

```bash
python3 scripts/validate_blocks.py
```

Tests hit **live** public networks/APIs (the org rule is no mocks). A failure can be an upstream outage: re-run before changing code.

## Structure

| Path | What |
|---|---|
| `docs/BUILD-WITH-BLOCKS.md` | assembly guide + recipes |
| `docs/BLOCKS-SCHEMA.md` | schema documentation |
| `docs/blocks.schema.json` | JSON Schema |
| `docs/STATUS.md` | repo audit |
| `scripts/validate_blocks.py` | validator |
| `.github/workflows/validate-blocks.yml` | CI |
| `ISSUE_TEMPLATE/, *.md` | community health defaults |

## Conventions

- Community files here apply to every repo that does not define its own.

## Extension points

- New schema field: add it to blocks.schema.json + BLOCKS-SCHEMA.md as optional first.

## Do

- Validate locally before pushing a blocks.json.

## Don't

- Make optional schema fields required without updating every repo.
- Commit secrets, keys or `.env` files. Run `gitleaks` before pushing; CI and the org policy reject leaks.

## Using it from another project

- **docs/blocks.schema.json** (file): `https://raw.githubusercontent.com/Blockchains/.github/main/docs/blocks.schema.json`
- **docs/BUILD-WITH-BLOCKS.md** (file): `how to assemble projects from Blockchains repos, with 3 verified recipes`
- **scripts/validate_blocks.py** (cli): `python3 scripts/validate_blocks.py [--local DIR ...]   # validates every repo's blocks.json`
- **validate blocks** (github-action): `push, daily, workflow_dispatch`

See the README section [Use as a building block](README.md#use-as-a-building-block) for a copy-paste example.

## Related blocks

- [Blockchains/blockchains.github.io](https://github.com/Blockchains/blockchains.github.io): hub aggregates every blocks.json into /blocks.json
- [Blockchains/blockchainlab-sdk](https://github.com/Blockchains/blockchainlab-sdk): example block
- [Blockchains/blockchainlab-mcp](https://github.com/Blockchains/blockchainlab-mcp): example block
