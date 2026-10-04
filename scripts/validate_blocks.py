#!/usr/bin/env python3
"""Validate the blocks.json manifest of every public, non-archived, non-fork Blockchains repo against docs/blocks.schema.json.

Usage:
  python3 scripts/validate_blocks.py                 # all live repos (GitHub API; uses GH_TOKEN/GITHUB_TOKEN if set)
  python3 scripts/validate_blocks.py --local DIR...  # local checkouts (DIR/blocks.json or DIR/blocks/hub.json)
Exit 1 if any manifest is invalid, if `repo`/`name` do not match the repository, or if a repo listed in REQUIRED has none.
"""
import json, os, sys, urllib.request, urllib.error, pathlib
import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "docs" / "blocks.schema.json").read_text())
OWNER = "Blockchains"
# The hub's root /blocks.json is the aggregated org catalogue; its own manifest lives here instead.
MANIFEST_PATH = {"blockchains.github.io": "blocks/hub.json"}
# Repos that must ship a manifest (third-party hackathon code and empty placeholders are exempt).
REQUIRED = {".github", "Blockchains", "awesome-blockchainlab", "awesome-grokhack", "blockchain-dev-roadmap", "blockchain-interview-questions",
            "blockchainlab-api", "blockchainlab-compose", "blockchainlab-feeds", "blockchainlab-index", "blockchainlab-labs", "blockchainlab-lens",
            "blockchainlab-mcp", "blockchainlab-sdk", "blockchainlab-starters", "blockchainlab-tools", "blockchains.github.io",
            "forge-dao-governance-token", "forge-example-gasless-membership", "forge-example-usd-savings-vault", "forge-usd-priced-membership-nft",
            "fork-sync", "grok-release-radar", "grok-tools-chat", "grokhack-forge", "grokhack-index", "grokhack-submissions",
            "hackathon-entry-template", "hackathons", "sites-monitor", "whitepapers"}
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")


def get(url, raw=False):
    h = {"User-Agent": "blockchains-validate-blocks"}
    if TOKEN and "api.github.com" in url:
        h["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        b = r.read()
    return b.decode() if raw else json.loads(b)


def live_repos():
    out, page = [], 1
    while True:
        batch = get(f"https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&page={page}")
        out += [r for r in batch if not r["fork"] and not r["archived"] and not r["private"]]
        if len(batch) < 100:
            return out
        page += 1


def check(name, manifest, v):
    errs = [f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message[:200]}" for e in v.iter_errors(manifest)]
    if manifest.get("repo") != f"{OWNER}/{name}":
        errs.append(f"repo field is {manifest.get('repo')!r}, expected {OWNER}/{name}")
    if manifest.get("name") != name:
        errs.append(f"name field is {manifest.get('name')!r}, expected {name}")
    for c in manifest.get("compatible_with", []):
        if c.get("repo") == f"{OWNER}/{name}":
            errs.append("compatible_with lists the repo itself")
    return errs


def main():
    v = jsonschema.Draft202012Validator(SCHEMA, format_checker=jsonschema.FormatChecker())
    results, missing = {}, []
    if "--local" in sys.argv:
        for d in sys.argv[sys.argv.index("--local") + 1:]:
            p = pathlib.Path(d).resolve(); name = p.name
            f = p / MANIFEST_PATH.get(name, "blocks.json")
            if not f.exists():
                if name in REQUIRED: missing.append(name)
                continue
            results[name] = check(name, json.loads(f.read_text()), v)
    else:
        for r in live_repos():
            name, br = r["name"], r["default_branch"]
            path = MANIFEST_PATH.get(name, "blocks.json")
            try:
                m = json.loads(get(f"https://raw.githubusercontent.com/{OWNER}/{name}/{br}/{path}", raw=True))
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    if name in REQUIRED:
                        missing.append(name)
                    else:
                        print(f"skip  {name}: no manifest (not required)")
                    continue
                raise
            except json.JSONDecodeError as e:
                results[name] = [f"invalid JSON: {e}"]; continue
            results[name] = check(name, m, v)
    bad = {k: e for k, e in results.items() if e}
    for k in sorted(results):
        print(("FAIL " if results[k] else "ok    ") + k)
        for e in results[k]:
            print("      - " + e)
    for k in missing:
        print(f"MISSING {k}: required manifest not found")
    print(f"\n{len(results) - len(bad)}/{len(results)} manifests valid; {len(missing)} required missing")
    sys.exit(1 if bad or missing else 0)


if __name__ == "__main__":
    main()
