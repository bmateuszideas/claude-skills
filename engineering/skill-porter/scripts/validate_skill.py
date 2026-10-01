#!/usr/bin/env python3
"""validate_skill.py — Validate a converted skill package against the Agent Skills spec and Mistral constraints.

Checks: SKILL.md presence; frontmatter parse; name regex
^[a-z0-9]+(-[a-z0-9]+)*$ (1-64 chars, matches parent dir); description
1-1024 chars; optional field constraints (compatibility <=500); body line
count vs the 500-line guidance; every relative file reference resolves
inside the package; CLI-target checks (allowed-tools against the real Vibe
tool registry, no reserved builtin names); Work-target checks (no
CLI-only frontmatter fields, no leftover ${VAR}/bash blocks).

Usage:
    python3 scripts/validate_skill.py <skill-dir> --target vibe-code|vibe-work|api [--json]
Exit codes: 0 valid, 1 warnings, 2 invalid.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VIBE_TOOLS = {
    "bash", "edit", "exit_plan_mode", "git_bash", "grep", "read_file",
    "search_replace", "skill", "task", "todo", "web_fetch", "web_search",
    "ask_user_question", "write_file",
}
RESERVED_NAMES = {"vibe", "skill-creator"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
REF_RE = re.compile(r"(?:references|assets|scripts)/[\w./-]*[\w-]+(?:\.[\w-]+)?(?<![.])")
VAR_RE = re.compile(r"\$\{[A-Z_][A-Z0-9_]*\}|\$\(date[^)]*\)")
SHELL_BLOCK_RE = re.compile(r"```(?:bash|sh|shell)\n")
CLI_ONLY_FIELDS = {"user-invocable", "disable-model-invocation", "allowed-tools"}


def parse_frontmatter(text: str) -> tuple[dict, list[str]]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, ["SKILL.md must start with --- frontmatter on line 1"]
    fm: dict[str, str] = {}
    errors: list[str] = []
    for line in m.group(1).splitlines():
        if line.startswith((" ", "\t")) or not ":" in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip("\"'")
    return fm, errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("skill_dir")
    ap.add_argument("--target", required=True,
                    choices=["vibe-code", "vibe-work", "api"])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.skill_dir)
    errors: list[str] = []
    warnings: list[str] = []

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        print(json.dumps({"valid": False, "errors": ["no SKILL.md"]})
              if args.json else "INVALID: no SKILL.md", file=sys.stderr)
        return 2

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, errs = parse_frontmatter(text)
    errors += errs

    name = fm.get("name", "")
    if not name:
        errors.append("frontmatter: missing name")
    else:
        if not (1 <= len(name) <= 64):
            errors.append(f"name: length {len(name)} outside 1-64")
        if not NAME_RE.fullmatch(name):
            errors.append(f"name '{name}': violates ^[a-z0-9]+(-[a-z0-9]+)*$")
        if root.name and name != root.name:
            errors.append(f"name '{name}' != parent directory '{root.name}'")
        if name in RESERVED_NAMES:
            errors.append(f"name '{name}' is a reserved builtin")

    desc = fm.get("description", "")
    if not (1 <= len(desc) <= 1024):
        errors.append(f"description: {len(desc)} chars (must be 1-1024)")

    compat = fm.get("compatibility")
    if compat and len(compat) > 500:
        errors.append("compatibility: >500 chars")

    body = FRONTMATTER_RE.sub("", text, count=1)
    lines = len(body.strip().splitlines())
    if lines > 500:
        warnings.append(f"body is {lines} lines (recommended <500) — split into references/")

    # file references resolve (body + every reference/asset file).
    # In supporting files, ignore fenced code blocks (illustrative examples)
    # and require a file extension — folder-name prose is not a reference.
    FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
    scan_files = [("SKILL.md", body)]
    for sub in ("references", "assets"):
        sub_dir = root / sub
        if sub_dir.is_dir():
            for p in sorted(sub_dir.rglob("*.md")):
                scan_files.append((str(p.relative_to(root)), p.read_text(encoding="utf-8", errors="replace")))
    for src_name, src_body in scan_files:
        if src_name != "SKILL.md":
            src_body = FENCE_RE.sub("", src_body)
        for ref in sorted(set(REF_RE.findall(src_body))):
            if src_name != "SKILL.md" and "." not in ref.rsplit("/", 1)[-1]:
                continue
            target = (root / ref.split("#")[0].rstrip("/")).resolve()
            if not target.exists():
                errors.append(f"referenced file missing: {ref} (referenced from {src_name})")

    if args.target == "vibe-work":
        bad = CLI_ONLY_FIELDS & set(fm.keys())
        if bad:
            errors.append(f"Work target: strip CLI-only frontmatter fields: {sorted(bad)}")
        if VAR_RE.search(body):
            errors.append("Work target: leftover ${VAR}/$(date) shell references in body")
        if SHELL_BLOCK_RE.search(body):
            warnings.append("Work target: bash code blocks in body — rewrite as instructions or interpreter snippets")
        if (root / "agents" / "openai.yaml").is_file():
            warnings.append("Work target: agents/openai.yaml present — Work does not read it; drop or fold into body")

    if args.target == "vibe-code":
        tools = fm.get("allowed-tools", "")
        for t in tools.split():
            base = re.split(r"[(:]", t)[0]
            if base not in VIBE_TOOLS:
                warnings.append(f"allowed-tools: '{t}' not a known Vibe tool")

    report = {"valid": not errors, "errors": errors, "warnings": warnings,
              "name": name, "description_chars": len(desc), "body_lines": lines,
              "frontmatter_fields": sorted(fm.keys())}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for e in errors:
            print(f"ERROR: {e}")
        for w in warnings:
            print(f"WARN: {w}")
        print("VALID" if not errors else "INVALID")
    return 2 if errors else (1 if warnings else 0)


if __name__ == "__main__":
    sys.exit(main())
