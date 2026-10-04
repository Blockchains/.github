# Build with Blocks

How an AI agent (or a human) assembles a working project from the repositories under [github.com/Blockchains](https://github.com/Blockchains). Every live repo is documented as a **block**: what it exports, how to install it, its inputs and outputs, and which other blocks it fits with.

- Org doc map for LLMs: **https://blockchains.github.io/llms.txt** (full text: https://blockchains.github.io/llms-full.txt)
- Catalogue of every block (machine-readable): **https://blockchains.github.io/blocks.json** · human view: https://blockchains.github.io/blocks/
- Manifest format: [BLOCKS-SCHEMA.md](BLOCKS-SCHEMA.md) ([JSON Schema](blocks.schema.json))
- In each repo: `README.md` → section **Use as a building block**, `AGENTS.md` (setup, commands, structure, rules), `llms.txt`, `blocks.json`

## 1. The blocks at a glance

| Layer | Block | Use it for | Get it |
|---|---|---|---|
| Data | [blockchainlab-api](https://github.com/Blockchains/blockchainlab-api) | 20 nightly JSON datasets (chains, RPC health, TVL, stablecoins, yields, L2s, hacks, OFAC, EIPs…) | `https://blockchains.github.io/blockchainlab-api/v1/<dataset>.json` |
| Data | [blockchainlab-sdk](https://github.com/Blockchains/blockchainlab-sdk) | Typed TS/Python client for the API | `npm i github:Blockchains/blockchainlab-sdk` |
| Data | [blockchainlab-feeds](https://github.com/Blockchains/blockchainlab-feeds), [whitepapers](https://github.com/Blockchains/whitepapers) | Hackathon/event/X-intel feeds; historic whitepaper index | raw JSON URLs |
| Agents | [blockchainlab-mcp](https://github.com/Blockchains/blockchainlab-mcp) | 43 read-only MCP tools for any agent (datasets + live on-chain decoding) | `npx -y github:Blockchains/blockchainlab-mcp` |
| Agents | [grokhack-forge](https://github.com/Blockchains/grokhack-forge) | Compose a Grok app (chat or digest) with CI and Pages | `python3 forge/compose.py --idea … --name …` |
| Agents | [grokhack-index](https://github.com/Blockchains/grokhack-index) | Grok/xAI integration parts from 99 forks | `data/parts.json` |
| Contracts | [forge-usd-priced-membership-nft](https://github.com/Blockchains/forge-usd-priced-membership-nft) | ERC-721 pass, USD price via Chainlink, royalties, roles | `forge install Blockchains/forge-usd-priced-membership-nft` |
| Contracts | [forge-dao-governance-token](https://github.com/Blockchains/forge-dao-governance-token) | ERC20Votes + permit token, Governor + Timelock | `forge install …` |
| Contracts | [forge-example-usd-savings-vault](https://github.com/Blockchains/forge-example-usd-savings-vault), [forge-example-gasless-membership](https://github.com/Blockchains/forge-example-gasless-membership) | ERC-4626 USD vault; ERC-4337 paymaster club (with viem front ends) | `forge install …` |
| Contracts | [blockchainlab-labs](https://github.com/Blockchains/blockchainlab-labs) | 45 small tested Solidity patterns (AMM, flash loan, proxy, ERC-7201…), Noir, Cairo | `forge install Blockchains/blockchainlab-labs` |
| Contracts | [blockchainlab-starters](https://github.com/Blockchains/blockchainlab-starters) | 8 CI-tested starters (OZ, Chainlink, Uniswap v4 hook, 4337, Hedera, wagmi, circom, Noir) | template repo |
| Composers | [blockchainlab-compose](https://github.com/Blockchains/blockchainlab-compose) + [blockchainlab-index](https://github.com/Blockchains/blockchainlab-index) | Idea → tested Foundry repo from indexed fork components | `python3 -m blcompose.compose "…" --name …` |
| UI / explain | [blockchainlab-tools](https://github.com/Blockchains/blockchainlab-tools), [blockchainlab-lens](https://github.com/Blockchains/blockchainlab-lens) | 26 browser tools with deep links; explorer explainer + `BLLens` detector | `https://blockchains.github.io/blockchainlab-tools/<tool>/?…` |
| Hub | [blockchains.github.io](https://github.com/Blockchains/blockchains.github.io) | 75 services, `services.json`, health data, this catalogue | https://blockchains.github.io |
| Templates | [hackathon-entry-template](https://github.com/Blockchains/hackathon-entry-template), [grokhack-submissions](https://github.com/Blockchains/grokhack-submissions) | Entry repos with CI and secret scanning | GitHub template |
| Learning | [blockchain-dev-roadmap](https://github.com/Blockchains/blockchain-dev-roadmap), [blockchain-interview-questions](https://github.com/Blockchains/blockchain-interview-questions) | Curated paths linking labs and tools | README |
| Fork corpus | [awesome-blockchainlab](https://github.com/Blockchains/awesome-blockchainlab), [awesome-grokhack](https://github.com/Blockchains/awesome-grokhack), [fork-sync](https://github.com/Blockchains/fork-sync) | Curated, synced forks of upstream projects (see section 4) | `forge.json`, `grok-forge.json`, `forks.json` |

## 2. How to assemble a project (procedure for an AI agent)

1. **Discover.** Fetch `https://blockchains.github.io/blocks.json`. Filter `blocks[]` by `kind` (`library`, `contracts`, `mcp-server`, `http-api`, …) and read each candidate's `summary`, `inputs`, `outputs` and `compatible_with`.
2. **Check fit.** Prefer pairs that list each other in `compatible_with`. Check `license` (GPL blocks such as `forge-example-gasless-membership` make the combined work GPL) and `stability` (`reference` = copy and adapt, `stable` = depend on it).
3. **Read the block's `AGENTS.md`** (raw URL in its `llms.txt`) for setup, test commands and do/don't rules.
4. **Install from the `entrypoints`** exactly as written; pin a tag or commit (`github:Blockchains/<repo>#<sha>`, `forge install Blockchains/<repo>@<tag>`).
5. **Prove it.** Run the block's `tests.command`, then your own test of the combination. Most tests use live networks: retry once before assuming a code bug.
6. **Never** commit keys; run `gitleaks` before pushing. Show "needs key" notices instead of faking AI output.

## 3. Recipes (each one was run end to end on 2026-10-04)

### Recipe 1: token-gated dApp (forge-usd-priced-membership-nft + blockchainlab-sdk + blockchainlab-api)

A members-only contract gated on the composed USD-priced membership NFT, plus the off-chain gate a front end uses: OFAC screening and a healthy RPC from the SDK.

**Contracts** (Foundry, solc 0.8.30):

```bash
forge init gated && cd gated && rm -f src/Counter.sol test/Counter.t.sol script/Counter.s.sol
forge install Blockchains/forge-usd-priced-membership-nft Blockchains/openzeppelin-contracts@v5.7.0
cat > remappings.txt <<'R'
@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/
@chainlink/contracts/src/=lib/forge-usd-priced-membership-nft/lib/chainlink-evm/contracts/src/
forge-std/=lib/forge-std/src/
membership/=lib/forge-usd-priced-membership-nft/src/
R
# foundry.toml [profile.default]: solc = "0.8.30", evm_version = "cancun"
```

`lib/` inside each forge-* repo holds only the OpenZeppelin files that project uses, so map `@openzeppelin/contracts/` to the full fork at the same release (v5.7.0, commit `cab1993`). That way several forge-* blocks can share one OpenZeppelin.

`src/MembersOnly.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";

/// Token gate: any function marked onlyMembers needs at least one pass from the membership NFT.
contract MembersOnly {
    IERC721 public immutable pass;
    mapping(address => string) public notes;
    error NotMember(address who);
    constructor(IERC721 pass_) { pass = pass_; }
    modifier onlyMembers() { if (pass.balanceOf(msg.sender) == 0) revert NotMember(msg.sender); _; }
    function post(string calldata note) external onlyMembers { notes[msg.sender] = note; }
}
```

`test/MembersOnly.t.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "forge-std/Test.sol";
import {UsdPricedMembership} from "membership/UsdPricedMembership.sol";
import {FixedPriceAggregator} from "lib/forge-usd-priced-membership-nft/test/utils/FixedPriceAggregator.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {MembersOnly} from "../src/MembersOnly.sol";

contract MembersOnlyTest is Test {
    UsdPricedMembership nft; MembersOnly gate; address alice = address(0xA11CE);
    function setUp() public {
        FixedPriceAggregator feed = new FixedPriceAggregator(2500e8);           // $2,500 / ETH
        nft = new UsdPricedMembership(address(this), 100, "ipfs://base/", address(feed), 25e18, 1 hours, address(this), 500); // $25 mint
        gate = new MembersOnly(IERC721(address(nft)));
        vm.deal(alice, 1 ether);
    }
    function test_gate() public {
        vm.prank(alice); vm.expectRevert(abi.encodeWithSelector(MembersOnly.NotMember.selector, alice)); gate.post("hi");
        uint256 price = nft.mintPriceWei();                                      // $25 at $2,500/ETH = 0.01 ETH
        vm.prank(alice); nft.mint{value: price}();
        vm.prank(alice); gate.post("gm");
        assertEq(gate.notes(alice), "gm");
    }
}
```

`forge test` → `[PASS] test_gate()`. Deploy with the repo's `script/Deploy.s.sol` pattern (live Chainlink ETH/USD feed on Sepolia/mainnet), then deploy `MembersOnly(pass)`. The same setup also compiles `forge-dao-governance-token` if you install it next to it, so you can add a governor.

**Off-chain gate** (Node ≥ 18 or browser; `npm i github:Blockchains/blockchainlab-sdk`):

```js
import { BlockchainLab } from "blockchainlab-sdk";
const bl = new BlockchainLab();

// Is `wallet` allowed in? Screen against OFAC, then check it holds a pass on the membership NFT.
export async function canEnter(wallet, nft, chain = "ethereum") {
  if (await bl.isSanctioned(wallet)) return { ok: false, reason: "sanctioned address" };
  const [rpc] = await bl.healthyRpcs(chain);                       // fastest healthy public RPC from the nightly probe
  const data = "0x70a08231" + wallet.slice(2).toLowerCase().padStart(64, "0");   // balanceOf(address)
  const r = await fetch(rpc.url, { method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "eth_call", params: [{ to: nft, data }, "latest"] }) }).then(r => r.json());
  const balance = BigInt(r.result);
  return { ok: balance > 0n, balance, rpc: rpc.url };
}
// Live check against any ERC-721, e.g. canEnter("0x000000000000000000000000000000000000dEaD", "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D")
// returned { ok: true, balance: 3n, rpc: "https://eth.drpc.org" } on 2026-10-04.
```

Extend: show the mint price in USD (`mintPriceWei()`), link each tx to `https://blockchains.github.io/blockchainlab-tools/tx/?chain=<chain>&hash=<hash>`, or start the UI from `blockchainlab-starters/starters/wagmi-rainbowkit-dapp`.

### Recipe 2: Grok agent with blockchain tools (grokhack-forge + blockchainlab-mcp + blockchainlab-sdk)

**a. Compose the app** (Python 3.10+, Node 20):

```bash
git clone https://github.com/Blockchains/grokhack-forge && cd grokhack-forge
python3 forge/compose.py --idea "A chat assistant that answers DeFi questions with tools" --name defi-grok-chat --out /tmp/defi-grok-chat
cd /tmp/defi-grok-chat && npm ci && npm i github:Blockchains/blockchainlab-sdk
```

**b. Give Grok blockchain tools.** The `chat` archetype streams through `@ai-sdk/xai` and calls the tools in `src/tools.ts` → `localTools`. Add:

```ts
import { BlockchainLab } from 'blockchainlab-sdk'
const bl = new BlockchainLab()

// inside `export const localTools = { … }`
  defi_protocols: tool({
    description: 'Top DeFi protocols by TVL (DefiLlama snapshot via the Blockchain Lab Open Data API). Filter by category and chain.',
    inputSchema: z.object({ category: z.string().optional().describe('e.g. Lending, Dexs'), chain: z.string().optional().describe('e.g. Arbitrum'), limit: z.number().int().min(1).max(20).default(5) }),
    execute: async ({ category, chain, limit }) => ({ results: (await bl.rows('protocols')).filter(p => (!category || p.category === category) && (!chain || (p.chains ?? []).includes(chain))).slice(0, limit) }),
  }),
  stablecoin: tool({
    description: 'Stablecoin price vs peg and circulating supply by symbol.',
    inputSchema: z.object({ symbol: z.string().describe('e.g. USDC') }),
    execute: async ({ symbol }) => ({ results: [await bl.stablecoin(symbol)].filter(Boolean) }),
  }),
```

`npm run build` (tsc + vite) passes, and a node test calling both tools against the live API passes (`npm test`). The visitor's xAI key goes only to api.x.ai. Push with `--create --wait` (or the compose workflow) to get a repo with CI and Pages.

The SDK is used in app code because it is typed. `blockchainlab-mcp`'s JS SDK works too, but it ships no `.d.ts` yet, so `tsc` needs a `declare module 'blockchainlab-mcp'` shim.

**c. Give the developer agent the same powers via MCP.** When you or an AI coding agent (Grok, Cursor, Claude Code) works on the app, add the MCP server so it can query chains, decode transactions and check standards while coding:

```json
{ "mcpServers": { "blockchainlab": { "command": "npx", "args": ["-y", "github:Blockchains/blockchainlab-mcp"] } } }
```

`tools/list` returns 43 tools (e.g. `top_defi_protocols`, `decode_transaction`, `lookup_standard`, `sanctions_check`). For a server-side Grok agent, spawn the same server over stdio from your backend and pass its tools to the model. It never signs or sends transactions.

### Recipe 3: risk dashboard (blockchainlab-api + blockchainlab-lens + blockchainlab-tools)

A single static page: stablecoins off peg and large recent hacks from the API, plus a box that turns any tx hash, address or ENS name into an explanation link, using the same detector the Lens extension uses.

```html
<!doctype html>
<meta charset="utf-8">
<title>Risk dashboard (Blockchain Lab blocks)</title>
<script src="https://blockchains.github.io/blockchainlab-lens/extension/detect.js"></script>
<h1>Stablecoin pegs and recent hacks</h1>
<p><input id="q" placeholder="paste a tx hash, address or ENS name" size="70"> <a id="explain" target="_blank">explain ↗</a></p>
<h2>Stablecoins off peg (&gt; 0.5%)</h2><table id="peg"></table>
<h2>Hacks over $10m since 2026-01-01</h2><table id="hacks"></table>
<script type="module">
const API = "https://blockchains.github.io/blockchainlab-api/v1";
const get = (d) => fetch(`${API}/${d}.json`).then(r => r.json());
const [stables, hacks] = await Promise.all([get("stablecoins"), get("security-incidents")]);
document.querySelector("#peg").innerHTML = stables.data
  .filter(s => s.price != null && s.peg_type === "peggedUSD" && Math.abs(s.price - 1) > 0.005 && s.circulating > 1e7)
  .map(s => `<tr><td>${s.symbol}</td><td>${s.price.toFixed(4)}</td><td>$${(s.circulating / 1e6).toFixed(0)}m</td></tr>`).join("");
document.querySelector("#hacks").innerHTML = hacks.data
  .filter(h => (h.date ?? "") >= "2026-01-01" && (h.amount_usd ?? 0) >= 1e7)
  .map(h => `<tr><td>${h.date}</td><td>${h.name}</td><td>${h.technique ?? ""}</td><td>$${(h.amount_usd / 1e6).toFixed(1)}m</td></tr>`).join("");
const q = document.querySelector("#q"), a = document.querySelector("#explain");
q.oninput = () => { a.href = BLLens.fromText(q.value) || ""; };   // same deep links the Lens extension opens
</script>
```

Serve it with any static server (`python3 -m http.server`). Headless Chromium on 2026-10-04: 20 peg rows, 24 hack rows, no JS errors; `vitalik.eth` → `https://blockchains.github.io/blockchainlab-tools/address/?q=vitalik.eth&chain=ethereum&utm_source=blockchainlab-lens`. Data is CORS-enabled and needs no key. For production, switch the `fetch` calls to the typed SDK, add more datasets (`l2-metrics`, `yields`, `rpc-health`), and install [Lens](https://github.com/Blockchains/blockchainlab-lens) so explorer pages get the same explanations.

## 4. Reusing the fork corpus

388 live forks of upstream open-source projects sit under Blockchains (archived forks are listed in `ARCHIVED-*.md` reports and can be unarchived). They are **unmodified mirrors**, kept current by [fork-sync](https://github.com/Blockchains/fork-sync) (curated blockchain set) and the grokhack-index nightly (Grok set). They have no `blocks.json` of their own. Use the indexes instead:

| Need | Where | How |
|---|---|---|
| Find a contract/module by capability or symbol | [blockchainlab-index](https://github.com/Blockchains/blockchainlab-index) | `index.sqlite` FTS5, `components/<slug>.json`, or `indexer/compose.py plan "<idea>"` |
| How to reuse a fork of a given category | `catalog.json` → `repos[].reuse` and [`taxonomy/reuse.json`](https://github.com/Blockchains/blockchainlab-index/blob/main/taxonomy/reuse.json) | pinned install line per fork + per-category notes |
| Curated list with licences and starters | [awesome-blockchainlab `forge.json`](https://github.com/Blockchains/awesome-blockchainlab/blob/main/forge.json) | category, licence notes, docs, starters, index links |
| Grok/xAI integration code | [grokhack-index `data/parts.json`](https://blockchains.github.io/grokhack-index/data/parts.json) | SDK exports, packages, snippets with commit-pinned URLs |
| Generate a project automatically | [blockchainlab-compose](https://github.com/Blockchains/blockchainlab-compose) (Solidity), [grokhack-forge](https://github.com/Blockchains/grokhack-forge) (Grok apps) | idea → repo with CI |

Rules for fork code: pin the indexed `commit`; keep SPDX headers and add a NOTICE; never copy source-available files (e.g. BUSL-1.1); GPL/LGPL components make the combined work copyleft; prefer the upstream package registry when the fork is only a mirror.

## 5. Keeping this true

- Each repo's `blocks.json` is validated daily by [validate-blocks](../.github/workflows/validate-blocks.yml); the hub catalogue is rebuilt weekly by `scripts/blocks.py` in blockchains.github.io.
- When you add or change an export, update that repo's README section, `AGENTS.md`, `llms.txt` and `blocks.json` in the same commit.
