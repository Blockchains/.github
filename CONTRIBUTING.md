# Contributing to Blockchain Lab open source

Thanks for helping! These rules apply to every repository under [github.com/Blockchains](https://github.com/Blockchains) unless a repo has its own CONTRIBUTING file.

## Ground rules

1. **Real and verifiable.** Tools, datasets and docs must use real public sources (RPCs, specs, public APIs). Cite the source. Never ship placeholder data as if it were live.
2. **Tested.** Every change ships with a test or a reproducible check. CI must be green.
3. **No secrets.** Never commit keys, tokens, `.env` files or private data. Run `gitleaks dir .` before pushing.
4. **Small PRs.** One logical change per pull request, with a clear description.
5. **Educational code is not audited.** Labs and examples are for learning — do not deploy them with real funds.

## Workflow

1. Search existing issues, or open one using a template.
2. Fork, create a branch, make your change, add tests.
3. Open a PR using the template. A maintainer reviews within a few days.

## Where things live

| Area | Repo |
|---|---|
| Hub (search, AI briefs, monitors) | [blockchains.github.io](https://github.com/Blockchains/blockchains.github.io) |
| Browser tools | [blockchainlab-tools](https://github.com/Blockchains/blockchainlab-tools) |
| Data API | [blockchainlab-api](https://github.com/Blockchains/blockchainlab-api) |
| SDK (TS/Python) | [blockchainlab-sdk](https://github.com/Blockchains/blockchainlab-sdk) |
| MCP server | [blockchainlab-mcp](https://github.com/Blockchains/blockchainlab-mcp) |
| Labs | [blockchainlab-labs](https://github.com/Blockchains/blockchainlab-labs) |

By contributing you agree your work is licensed under the repository's licence and that you follow the [Code of Conduct](CODE_OF_CONDUCT.md).
