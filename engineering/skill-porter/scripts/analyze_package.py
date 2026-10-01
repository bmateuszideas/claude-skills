#!/usr/bin/env python3
"""analyze_package.py — Scan a Claude/Codex skill package and emit a mechanism inventory.

Walks the source package, classifies every file, detects platform (Claude
Code vs OpenAI Codex), inventories mechanisms (tools named, hooks, agents,
commands, scripts, env vars, plugin manifests), and prints a report the
converting model uses for capability mapping. Deterministic, stdlib-only.

Usage:
    python3 scripts/analyze_package.py <package-dir> [--json]
Exit codes: 0 success, 1 warnings (e.g. missing referenced files), 2 errors.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CLAUDE_TOOLS = [
    "Read", "Write", "Edit", "MultiEdit", "Bash", "Grep", "Glob",
    "WebSearch", "WebFetch", "Task", "TodoWrite", "AskUserQuestion",
]
CLAUDE_HOOK_EVENTS = [
    "PreToolUse", "PostToolUse", "SessionStart", "Stop",
    "UserPromptSubmit", "Notification", "PreCompact",
]
TOOL_USE_RES = [re.compile(p) for p in (
    r"`{t}`",
    r"\bthe {t} tool\b",
    r"\buse the {t}\b",
    r"\b{t} tool\b",
    r"\b{t}\(".replace("\\\\", "\\\\\\\\"),
)]
ENV_VAR_RE = re.compile(r"\$\{[A-Z_][A-Z0-9_]*\}|\$\(date[^)]*\)|~/\.[A-Za-z_]+")
SHELL_BLOCK_RE = re.compile(r"```(?:bash|sh|shell)\n(.*?)```", re.DOTALL)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict = {}
    for line in m.group(1).splitlines():
        if line.startswith("  ") or ":" not in line:
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip().strip("\"'")
    return out


def classify_script(path: Path, text: str) -> str:
    head = text[:4000]
    if re.search(r"os\.walk|glob\.glob|Path\(.*home|expanduser|~\/", head):
        return "filesystem-bound"
    if re.search(r"--action|session|state|\.json.*(write|dump|save)|append.*log", head, re.I):
        if re.search(r"record_sent|record_received|counter|tally|cache", text, re.I):
            return "stateful"
    body_lines = len(text.splitlines())
    # crude formula-mask heuristic: simple arithmetic on tabular input
    if re.search(r"\b(Reach|Impact|Confidence|Effort)\b", head) or (
        body_lines < 400 and re.search(r"argv|argparse", head)
        and not re.search(r"transcript|interview|sentiment", head, re.I)
    ):
        return "formula-maskable"
    if re.search(r"transcript|interview|sentiment|theme|quote", text, re.I):
        return "text-analysis"
    return "general"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("package_dir")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    root = Path(args.package_dir)
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        print("error: no SKILL.md found — is this a skill package?",
              file=sys.stderr)
        return 2

    warnings: list[str] = []
    all_text: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix in {".md", ".yaml", ".yml", ".json", ".py", ".sh"}:
            try:
                all_text[str(p.relative_to(root))] = p.read_text(
                    encoding="utf-8", errors="replace")
            except OSError as e:
                warnings.append(f"unreadable: {p}: {e}")

    combined = "\n".join(all_text.values())

    platform = "claude-code"
    if (root / "agents" / "openai.yaml").is_file():
        platform = "codex"

    def tool_referenced(tool: str) -> bool:
        patterns = (rf"`{tool}`", rf"\bthe {tool} tool\b",
                    rf"\buse the {tool}\b", rf"\b{tool} tool\b")
        return any(re.search(p, combined) for p in patterns)

    tools_found = sorted(t for t in CLAUDE_TOOLS if tool_referenced(t))
    hooks_found = sorted({h for h in CLAUDE_HOOK_EVENTS
                          if re.search(rf"\b{h}\b", combined)})
    env_vars = sorted(set(ENV_VAR_RE.findall(combined)))
    shell_blocks = sum(len(SHELL_BLOCK_RE.findall(v)) for v in all_text.values())

    commands = sorted(str(p.relative_to(root))
                      for p in (root / "commands").glob("*.md") if p.is_file()
                      ) if (root / "commands").is_dir() else []
    agents = sorted(str(p.relative_to(root))
                    for p in (root / "agents").glob("*.md") if p.is_file()
                    ) if (root / "agents").is_dir() else []

    scripts: dict[str, str] = {}
    if (root / "scripts").is_dir():
        for p in sorted((root / "scripts").iterdir()):
            if p.is_file() and p.suffix == ".py":
                scripts[p.name] = classify_script(p, all_text.get(
                    str(p.relative_to(root)), ""))

    # referenced-but-missing files
    referenced = set(re.findall(r"(?:references|assets|scripts)/[\w./-]+", combined))
    for ref in sorted(referenced):
        if not (root / ref.split("#")[0].rstrip("./")).exists():
            if not (root / ref).exists():
                warnings.append(f"referenced but not supplied: {ref}")

    plugin = (root / ".claude-plugin").is_dir()
    fm = parse_frontmatter(all_text.get("SKILL.md", ""))
    name = fm.get("name", root.name)

    report = {
        "package": str(root),
        "platform": platform,
        "name": name,
        "description_chars": len(fm.get("description", "")),
        "frontmatter_fields": sorted(fm.keys()),
        "name_regex_ok": bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name)),
        "claude_tools_referenced": tools_found,
        "claude_hook_events": hooks_found,
        "env_vars_and_shell_paths": env_vars,
        "shell_code_blocks": shell_blocks,
        "commands": commands,
        "agents": agents,
        "codex_openai_yaml": platform == "codex",
        "claude_plugin_manifest": plugin,
        "scripts_classified": scripts,
        "files": sorted(all_text.keys()),
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for k, v in report.items():
            print(f"{k}: {v}")
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
