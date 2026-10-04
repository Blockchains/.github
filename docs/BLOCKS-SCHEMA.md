# blocks.json: the Blockchains building-block manifest

Every live, non-fork repository under [github.com/Blockchains](https://github.com/Blockchains) ships a `blocks.json` at its root that tells AI agents and humans **what the repo exports and how to plug it into something else**. One schema is used everywhere:

- JSON Schema (draft 2020-12): [`docs/blocks.schema.json`](blocks.schema.json), raw URL `https://raw.githubusercontent.com/Blockchains/.github/main/docs/blocks.schema.json`
- Validator: [`scripts/validate_blocks.py`](../scripts/validate_blocks.py), run by [`validate-blocks`](../.github/workflows/validate-blocks.yml) on every push here and daily across all repos
- Aggregated catalogue of every manifest: **https://blockchains.github.io/blocks.json** (human view: https://blockchains.github.io/blocks/)
- How to combine blocks: [BUILD-WITH-BLOCKS.md](BUILD-WITH-BLOCKS.md)

Each repo also has `AGENTS.md` (instructions for AI coding agents) and `llms.txt` ([llmstxt.org](https://llmstxt.org/) format). `blocks.json` is the machine-readable part of the same information.

**Exception:** in `Blockchains/blockchains.github.io` the root `/blocks.json` is the org catalogue and `/llms.txt` is the org doc map, so that repo's own manifest is `blocks/hub.json`.

## Fields

| Field | Required | Type | Meaning |
|---|---|---|---|
| `$schema` | no | URI | Schema URL (always the raw URL above) |
| `schema_version` | yes | `"1.0"` | Manifest format version |
| `name` | yes | string | Repository name; must match the repo |
| `repo` | yes | `Blockchains/<name>` | Full repository id; must match the repo |
| `summary` | yes | string (10–400) | What the block is, in one or two sentences |
| `kind` | yes | array of enum | `library`, `contracts`, `http-api`, `dataset`, `mcp-server`, `cli`, `github-action`, `web-app`, `browser-extension`, `template`, `index`, `curated-list`, `docs`, `automation` |
| `stability` | yes | enum | `stable` (interfaces kept compatible), `beta` (may change, used in production), `experimental`, `reference` (generated/example code: copy and adapt) |
| `version` | no | string | Current version or API version |
| `license` | yes | SPDX expression | `NOASSERTION` when the repo has no licence file |
| `homepage` | no | URI | Live site or docs |
| `entrypoints` | yes | array | How to consume the block (see below) |
| `inputs` / `outputs` | yes | array of ports | `{name, type, description?}` |
| `deps` | yes | array of strings | Toolchains/runtimes, e.g. `node>=18`, `foundry (solc 0.8.30)` |
| `compatible_with` | yes | array | `{repo: "Blockchains/<other>", how}`: tested or documented combinations |
| `tests` | yes | object | `{command, ci?, network?}`: how to prove it works; `network: true` means live networks (no mocks) |
| `env` | no | array | `{name, required, purpose?}`: environment variables / secrets (names only, never values) |
| `docs` | yes | object | `{readme, agents, llms, extra?}`: paths of the docs in the repo |
| `tags` | no | array of strings | Free-form search tags |

### Entrypoints

| `type` | `ref` is | Typical `install` / `usage` |
|---|---|---|
| `npm` | source path of the package entry | `npm i github:Blockchains/<repo>` |
| `pypi` | source path of the package | `pip install "git+https://github.com/Blockchains/<repo>#subdirectory=python"` |
| `git` | template or clone URL | "Use this template" |
| `http` | URL (may contain `{placeholders}`) | `curl …` |
| `mcp-stdio` | server entry file | `npx -y github:Blockchains/<repo>` |
| `docker` | Dockerfile | `docker run -i --rm ghcr.io/blockchains/<repo>` |
| `cli` | script path | full command line |
| `solidity` | contract source path | `forge install Blockchains/<repo>` |
| `file` | path in the repo | how to use the file |
| `github-action` | workflow path | inputs / triggers |
| `web` | URL | deep-link pattern |
| `browser-script` | script path | `<script src=…>` |

`exports` (optional) lists the public names: functions, classes, contracts or MCP tools.

## Example (abridged, from blockchainlab-sdk)

```json
{
  "$schema": "https://raw.githubusercontent.com/Blockchains/.github/main/docs/blocks.schema.json",
  "schema_version": "1.0",
  "name": "blockchainlab-sdk",
  "repo": "Blockchains/blockchainlab-sdk",
  "summary": "Typed TypeScript and Python clients for the Blockchain Lab Open Data API …",
  "kind": ["library"],
  "stability": "stable",
  "version": "1.1.0",
  "license": "MIT",
  "entrypoints": [
    { "type": "npm", "name": "blockchainlab-sdk", "ref": "ts/src/index.ts", "install": "npm i github:Blockchains/blockchainlab-sdk", "exports": ["BlockchainLab", "DATASETS"] }
  ],
  "inputs": [{ "name": "dataset name", "type": "DatasetName" }],
  "outputs": [{ "name": "typed rows", "type": "<Dataset>Row[]" }],
  "deps": ["node>=18 (or browsers/Deno/Bun)", "python>=3.9 (stdlib only)"],
  "compatible_with": [{ "repo": "Blockchains/blockchainlab-api", "how": "the data source" }],
  "tests": { "command": "npm test", "ci": ".github/workflows/ci.yml", "network": true },
  "docs": { "readme": "README.md", "agents": "AGENTS.md", "llms": "llms.txt" }
}
```

## Rules

1. Everything in a manifest must be true of the code at the default branch. Commands must run; exports must exist.
2. Never put secret values in a manifest; `env` lists names only.
3. New optional fields can be added within `1.x`; making a field required or changing its meaning is `2.0` with a new schema file.
4. Validate before pushing: `pip install jsonschema && python3 scripts/validate_blocks.py --local ../<repo>`.
