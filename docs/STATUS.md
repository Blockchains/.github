# Blockchains: end-to-end test and documentation audit

Run on Sunday 4 October 2026, 18:13–18:45 BST, signed in to `gh` as **Blockchains**. Covers all **65 non-fork repos** (`gh repo list Blockchains --source`; 46 public, 19 private).
Every result below comes from a real run. Nothing was mocked or deleted. gitleaks scanned the staged changes before each of the 26 pushes and found no leaks.

## Totals

| Check | Result |
|---|---|
| CI | **123 workflows** across 65 repos. **116 green**, 0 red, 6 manual-dispatch workflows that have never run (sdk `release`, compose `Compose a project`, grokhack-forge `compose app`, 2× `Deploy (Sepolia)`, 1 dynamic Pages entry). 1 was mid-run at the final check (`blockchainlab-index` Nightly index, being edited by another worker; its previous run was green). Every workflow triggered by the 26 pushes from this audit completed green (CI, Pages, CodeQL, link-check, docker, live-tests). |
| Pages / homepages | 36 unique live URLs returned 200. lychee checked **~4,690 links** on their main pages (internal and external; 429s and bot-wall 403s ignored). **2 broken links, both fixed** (dead `grokhack.com/forge`). 1 off-org homepage returns 403 (`webapp` → swap.bancor.network, Bancor's site). |
| Data JSON | Hub: 14/14 `data/*.json` load · Open Data API: 20/20 datasets load · sites-monitor: 7/7 · feeds: 4/4 raw feeds |
| Local tests (core repos) | **17/17 pass.** hub, tools, api, mcp, sdk (TS + Py), labs (forge/hardhat/noir/cairo), lens, compose, grokhack-forge, the 4 forge example repos, sites-monitor, feeds, whitepapers, hackathons (no code) |
| Docs | 26 repos had README gaps filled from the actual code and pushed. Metadata set on 9 repos (topics, homepages, descriptions). All in-scope Blockchain Lab repos now pass, except for licence-file gaps that need a decision (below). |

## Highlights of the real end-to-end runs
- **blockchainlab-mcp**: `npm test` starts the stdio MCP server and calls **all 43 tools** against live sources (Safe, EIP-712, bridges, approvals, Solana, PSBT, Uniswap price impact, MEV, RPC health…). Result: `MCP OK 43 tools`.
- **blockchainlab-compose**: compose run from the idea *"An NFT membership collection with ERC-2981 royalties, role-based minting, a pause switch, and a paid mint priced in USD using a Chainlink ETH/USD price feed"*. It matched 5 capabilities (nft archetype), passed the compat checks, generated the code, and `forge test` gave 10 pass + 1 fork test skipped. With a public mainnet RPC: **11/11**. A **live Grok review ran (grok-4.7, ~9k tokens) and wrote REVIEW.md**. No repo was created.
- **grokhack-forge**: composed a chat app (Vite build, `npm test` 0 failures, **live api.x.ai e2e: grok-4.7 replied "pong"**) and a digest app (pytest 3 passed, **live e2e grok-4.7 "pong"**).
- **blockchainlab-tools** live browser e2e 27/27 · **hub** e2e 27/27 · **lens** real unpacked MV3 extension + bookmarklet 9/9 · **labs** forge 131/131.
- `XAI_API_KEY` came from the environment and was never printed.

## Fixes made
1. **Dead link `https://grokhack.com/forge` (404)**: the page doesn't exist on grokhack.com (the live sitemap has no `/forge`). It was linked from the grokhack-forge homepage and README, the grokhack-index search page and README, the grok-release-radar page (`app/render.py`), the grok-tools-chat footer (`src/main.ts`), PARTS.md, awesome-grokhack, and **the grokhack-forge generator templates** (so future apps would have inherited it). All now point to `github.com/Blockchains/grokhack-forge`. The grokhack-forge homepage is now `https://grokhack.com/`. The live pages were redeployed and re-checked with lychee: 0 errors.
2. **README completeness** (written from the code: env vars, defaults, flags, secrets): Configuration tables (hub jobs, starters, compose, grokhack-forge, grokhack-index, both forge contract repos with Deploy.s.sol defaults, sdk client options, labs, sites-monitor, feeds), Run/Usage (sites-monitor, feeds, whitepapers), Licence sections (only stating what the LICENSE files say), Contributing links to `Blockchains/.github`, and "Built by Blockchain Lab" footers. In blockchainlab-tools, the duplicated "Tests" section after the footer was merged into the main one. The whitepapers README is generated, so the change was made in `scripts/build_index.py` and the README regenerated (data unchanged).
3. **Metadata**: topics set for grokhack-index, awesome-grokhack, blockchainlab-compose and grokhack-forge. Homepage set for blockchainlab-compose, fork-sync, forge-usd-priced-membership-nft and forge-dao-governance-token (`blockchainlab.com/forge`). Descriptions set for badger-timelock and badger-geyser (taken from their own READMEs).

## Needs Ismail / not fixable here
- **grokhack.com/forge page**: if a /forge page is wanted on grokhack.com, it has to be built in Grok Build (not touched here). The links now point at the GitHub repo until then.
- **Licence decisions** (no LICENSE file, so I didn't invent one): `fork-sync`, `sites-monitor`, `blockchainlab-feeds`, `whitepapers`, `hackathons`, `Blockchains`, `.github`, `HoodPilot`, `x.github.io`. Their READMEs now say plainly that no licence file exists. **awesome-grokhack is inconsistent**: the README says CC0-1.0 but the LICENSE file is MIT. Pick one.
- **blockchainlab-feeds X source down**: the X API returns `client-not-enrolled`. It needs an X developer App attached to a Project. Feeds still publish hackathons/events, with X counts set to null.
- **FORGE_TOKEN not set?** The `Compose a project` (compose) and `compose app` (grokhack-forge) workflows have never run. Each one fails fast without a `FORGE_TOKEN` secret (fine-grained PAT). The 2 `Deploy (Sepolia)` workflows need `DEPLOYER_PRIVATE_KEY` and `SEPOLIA_RPC_URL`. The sdk `release` workflow has never been triggered.
- **Placeholders**: `HoodPilot`, `x.github.io`, `Lab` have README-only content, so there's nothing accurate to document. Fill them or archive them.
- **tmp-e2e** (private, empty, created 3 Oct): reported only, not deleted.
- **Third-party imports** (`badger-*` ×5, `synthetix-exchange-stats`, `mStable-tech-challenges`, `webapp` (Bancor), `HoodPilots`, `relic`, `clawchestra-hackathon`, `glom-analysis-project`): other authors' code. They weren't rebranded "Built by Blockchain Lab", since that would be false. Consider archiving the 2020 imports.
- **Private backup mirrors of the 17 domain sites** and `blockchainlab.com` (Grok Build source): CI is green and the live domains return 200 with clean links. They weren't edited (Grok Build scope).
- **blockchainlab-index**: only checked, not edited (another worker is editing it). Its README still lacks a Contributing link and a Built-by footer.
- **Flaky**: one forge-example-gasless-membership Sepolia fork test failed once on a public RPC and passed on the 2 reruns. · `ethglobal.com/events/mumbai` (hackathons README) returns 500 to automated clients behind Cloudflare, so it couldn't be verified.

## Per-repo results

| Repo | CI (latest run per workflow, default branch) | Pages / homepage | Tests | Docs | Fixed |
|---|---|---|---|---|---|
| [blockchains.github.io](https://github.com/Blockchains/blockchains.github.io) | ✅ 9/9 | ✅ 200, links ok, 14 data JSON 200 | ✅ gen_site no diff; validate 19 files; e2e 27/27 | ✅ (added config, licence, contributing) | docs |
| [blockchainlab-tools](https://github.com/Blockchains/blockchainlab-tools) | ✅ 4/4 | ✅ 200, links ok | ✅ npm test 16 groups; live e2e 27/27 | ✅ (config, contributing; removed duplicate Tests section) | docs |
| [blockchainlab-api](https://github.com/Blockchains/blockchainlab-api) | ✅ 5/5 | ✅ 200, links ok, 20/20 datasets load | ✅ validate 20 datasets, OpenAPI regen no diff | ✅ (config, contributing) | docs |
| [blockchainlab-mcp](https://github.com/Blockchains/blockchainlab-mcp) | ✅ 4/4 | ✅ homepage 200 | ✅ MCP stdio server, all 43 tools called live | ✅ (contributing) | docs |
| [blockchainlab-sdk](https://github.com/Blockchains/blockchainlab-sdk) | ✅ 4/5 (+1 manual, never run) | ✅ homepage 200 | ✅ TS live ALL OK; pytest 4 passed | ✅ (config table, licence, contributing, Built by) | docs |
| [blockchainlab-labs](https://github.com/Blockchains/blockchainlab-labs) | ✅ 3/3 | ✅ homepage 200 | ✅ forge 131/131, hardhat 2, noir, cairo | ✅ (config, licence, contributing) | docs |
| [blockchainlab-lens](https://github.com/Blockchains/blockchainlab-lens) | ✅ 4/4 | ✅ 200, links ok | ✅ extension + bookmarklet 9/9 | ✅ (config, licence, contributing) | docs |
| [blockchainlab-compose](https://github.com/Blockchains/blockchainlab-compose) | ✅ 1/2 (+1 manual, never run) | — (no Pages; homepage now blockchainlab.com/forge) | ✅ unittest 3; real NFT compose → forge 11/11 + live Grok review | ✅ (config, contributing, Built by, homepage, topics) | docs+meta |
| [grokhack-forge](https://github.com/Blockchains/grokhack-forge) | ✅ 3/4 (+1 manual, never run) | ⚠️ homepage was grokhack.com/forge (404) → now grokhack.com | ✅ unittest 3; chat app build/test + live Grok e2e; digest app pytest 3 + live Grok e2e | ✅ (config, contributing, topics) | dead link+docs+meta |
| [forge-example-gasless-membership](https://github.com/Blockchains/forge-example-gasless-membership) | ✅ 4/4 | ✅ 200, links ok | ✅ forge 6/6 (1 flaky fork run); web 3 + build | ✅ (contributing, Built by) | docs |
| [forge-example-usd-savings-vault](https://github.com/Blockchains/forge-example-usd-savings-vault) | ✅ 4/4 | ✅ 200, links ok | ✅ forge 10/10; web 4 + build | ✅ (contributing, Built by) | docs |
| [forge-usd-priced-membership-nft](https://github.com/Blockchains/forge-usd-priced-membership-nft) | ✅ 2/3 (+1 manual, never run) | — (contracts only; homepage set) | ✅ forge 11/11 incl. fork | ✅ (deploy config, contributing, Built by) | docs+meta |
| [forge-dao-governance-token](https://github.com/Blockchains/forge-dao-governance-token) | ✅ 2/3 (+1 manual, never run) | — (contracts only; homepage set) | ✅ forge 8/8 | ✅ (deploy config, contributing, Built by) | docs+meta |
| [sites-monitor](https://github.com/Blockchains/sites-monitor) | ✅ 5/6 (+1 manual, never run) | ✅ 200, links ok, 7 data JSON valid | ✅ uptime 36/36; security.py runs (no test suite) | ⚠️ no LICENSE file (run, config, contributing, Built by added) | docs |
| [blockchainlab-feeds](https://github.com/Blockchains/blockchainlab-feeds) | ✅ 1/1 | ✅ 4 live feed JSON valid | ✅ build_feeds.py runs (no test suite); X source down | ⚠️ no LICENSE file (usage, config, contributing added) | docs |
| [hackathons](https://github.com/Blockchains/hackathons) | none | ✅ /events/ 200 | n/a (issue tracker); 1 README link unverifiable (ethglobal 500 behind Cloudflare) | ⚠️ no LICENSE file (live link, contributing, Built by added) | docs |
| [whitepapers](https://github.com/Blockchains/whitepapers) | ✅ 3/3 | ✅ blockchainlab.com/pdf 200 (888 links ok) | ✅ build_index.py 79 papers, 0 non-200 | ⚠️ no LICENSE file (rebuild, contributing, Built by added via generator) | docs |
| [grokhack-index](https://github.com/Blockchains/grokhack-index) | ✅ 3/3 | ⚠️→✅ dead grokhack.com/forge link fixed | — | ✅ (config, contributing, topics) | dead link+docs+meta |
| [grok-release-radar](https://github.com/Blockchains/grok-release-radar) | ✅ 5/5 | ⚠️→✅ dead link fixed (188/188 ok) | ✅ pytest 3 (re-run after edit) | ✅ (contributing) | dead link+docs |
| [grok-tools-chat](https://github.com/Blockchains/grok-tools-chat) | ✅ 4/4 | ✅ 200, links ok | ✅ build + npm test 4/4 (re-run after edit) | ✅ (contributing) | dead link+docs |
| [awesome-grokhack](https://github.com/Blockchains/awesome-grokhack) | ✅ 1/1 | ✅ grokhack.com 200 | — | ⚠️ README says CC0-1.0, LICENSE file is MIT | dead link+docs+meta |
| [awesome-blockchainlab](https://github.com/Blockchains/awesome-blockchainlab) | ✅ 1/1 | ✅ 200 | — | ✅ (list; examples/config n/a) | — |
| [blockchainlab-starters](https://github.com/Blockchains/blockchainlab-starters) | ✅ 4/4 | ✅ 200, links ok | — (CI green) | ✅ (config, contributing, Built by) | docs |
| [fork-sync](https://github.com/Blockchains/fork-sync) | ✅ 1/1 | — (no Pages; homepage set) | — | ⚠️ no LICENSE file (licence note, contributing added) | docs+meta |
| [blockchain-dev-roadmap](https://github.com/Blockchains/blockchain-dev-roadmap) | ✅ 2/2 | ✅ 200 | — (link-check CI green) | ✅ (licence section) | docs |
| [blockchain-interview-questions](https://github.com/Blockchains/blockchain-interview-questions) | ✅ 2/2 | ✅ 200 | — (link-check CI green) | ✅ (licence, contributing link) | docs |
| [Blockchains](https://github.com/Blockchains/Blockchains) | none | ✅ (profile) | — | ✅ profile (contributing, Built by) | docs |
| [.github](https://github.com/Blockchains/.github) | none | — | — | ✅ (STATUS.md added) | docs |
| [blockchainlab-index](https://github.com/Blockchains/blockchainlab-index) | ✅ 0/1 (1 running) | ✅ homepage 200 | read-only (other worker editing) | ⚠️ no contributing/Built by (not edited on purpose) | — |
| [hackathon-entry-template](https://github.com/Blockchains/hackathon-entry-template) | ✅ 3/3 | ✅ 200 | — | template: README is the entry skeleton, left as is | — |
| [grokhack-submissions](https://github.com/Blockchains/grokhack-submissions) | ✅ 3/3 | ✅ 200 | — | template, left as is | — |
| [halalswitch.com](https://github.com/Blockchains/halalswitch.com) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [aisales.news](https://github.com/Blockchains/aisales.news) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [grokhack.com](https://github.com/Blockchains/grokhack.com) | ✅ 2/2 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [grokskill.com](https://github.com/Blockchains/grokskill.com) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [induscript.com](https://github.com/Blockchains/induscript.com) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [11plus.college](https://github.com/Blockchains/11plus.college) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [gpu.skin](https://github.com/Blockchains/gpu.skin) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [hackers.college](https://github.com/Blockchains/hackers.college) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [land.solar](https://github.com/Blockchains/land.solar) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [agenticoins.com](https://github.com/Blockchains/agenticoins.com) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [rcapad.com](https://github.com/Blockchains/rcapad.com) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [halal.coupons](https://github.com/Blockchains/halal.coupons) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [regulationcryptoasset.com](https://github.com/Blockchains/regulationcryptoasset.com) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [onetouchswitch.com](https://github.com/Blockchains/onetouchswitch.com) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [partywallsurvey.uk](https://github.com/Blockchains/partywallsurvey.uk) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [equityperpetual.com](https://github.com/Blockchains/equityperpetual.com) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [altvaults.com](https://github.com/Blockchains/altvaults.com) | ✅ 1/1 | ✅ live domain 200, links ok | n/a (backup mirror) | private backup mirror of a Grok Build site; not edited | — |
| [blockchainlab.com](https://github.com/Blockchains/blockchainlab.com) | none | ✅ 200 (312 links ok) | not run (Grok Build source) | not edited (Grok Build) | — |
| [tmp-e2e](https://github.com/Blockchains/tmp-e2e) | ✅ 1/1 | — | — | empty test repo; report only, not deleted | — |
| [HoodPilot](https://github.com/Blockchains/HoodPilot) | none | — | — | ⚠️ placeholder: README only; nothing to document | — |
| [x.github.io](https://github.com/Blockchains/x.github.io) | none | — | — | ⚠️ placeholder: README only; nothing to document | — |
| [Lab](https://github.com/Blockchains/Lab) | none | — | — | ⚠️ 2015 placeholder: 2-line README; nothing to document | — |
| [HoodPilots](https://github.com/Blockchains/HoodPilots) | ✅ 1/1 | — | — | third-party hackathon code; not rebranded | — |
| [relic](https://github.com/Blockchains/relic) | ✅ 1/1 | ✅ 200 | — | third-party hackathon code; not rebranded | — |
| [clawchestra-hackathon](https://github.com/Blockchains/clawchestra-hackathon) | ✅ 1/1 | — | — | third-party hackathon code; not rebranded | — |
| [glom-analysis-project](https://github.com/Blockchains/glom-analysis-project) | ✅ 1/1 | — | — | third-party hackathon code; not rebranded | — |
| [badger-timelock](https://github.com/Blockchains/badger-timelock) | ✅ 1/1 | — | — | 2020 third-party import; not rebranded (description set) | meta |
| [badger-geyser](https://github.com/Blockchains/badger-geyser) | ✅ 1/1 | — | — | 2020 third-party import; not rebranded (description set) | meta |
| [badger-docs](https://github.com/Blockchains/badger-docs) | none | — | — | 2020 third-party import; not rebranded | — |
| [badger-deploy](https://github.com/Blockchains/badger-deploy) | ✅ 1/1 | — | — | 2020 third-party import; not rebranded | — |
| [badger-dao](https://github.com/Blockchains/badger-dao) | ✅ 1/1 | — | — | 2020 third-party import; not rebranded | — |
| [synthetix-exchange-stats](https://github.com/Blockchains/synthetix-exchange-stats) | ✅ 1/1 | — | — | 2020 third-party import; not rebranded | — |
| [mStable-tech-challenges](https://github.com/Blockchains/mStable-tech-challenges) | none | — | — | 2020 third-party import; not rebranded | — |
| [webapp](https://github.com/Blockchains/webapp) | ✅ 1/1 | ⚠️ swap.bancor.network 403 (upstream, not ours) | — | 2020 third-party import; not rebranded | — |

Raw data on the box: `/workspace/e2e-ci.json`, `e2e-pages.json`, `e2e-lychee/`, `e2e-docs.json`, `e2e-progress.json`.
