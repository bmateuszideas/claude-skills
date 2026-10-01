#!/usr/bin/env python3
"""scaffold_skill.py — Generate the output skeleton for a converted skill on a chosen Mistral target.

Creates the target directory structure with a SKILL.md stub (frontmatter
pre-filled from the source), copies supporting files per target rules
(CLI: scripts/references/assets preserved; Work: merged references capped
by file-count; API: emits the POST /v2/skills JSON skeleton), and prints
the import checklist. The converting model fills the stub bodies.

Usage:
    python3 scripts/scaffold_skill.py <src-package> <out-dir> --name <kebab-name> --target vibe-code|vibe-work|api [--json]
Exit codes: 0 success, 1 warnings, 2 errors.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MERGE_CAP = 10  # Work attachment file-count rule of thumb


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip("\"'")
    return fm


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src_package")
    ap.add_argument("out_dir")
    ap.add_argument("--name", required=True)
    ap.add_argument("--target", required=True,
                    choices=["vibe-code", "vibe-work", "api"])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    src = Path(args.src_package)
    out = Path(args.out_dir)
    warnings: list[str] = []

    if not src.is_dir() or not (src / "SKILL.md").is_file():
        print("error: source package must be a directory with SKILL.md",
              file=sys.stderr)
        return 2
    if not NAME_RE.fullmatch(args.name) or not (1 <= len(args.name) <= 64):
        print(f"error: name '{args.name}' violates the Agent Skills name rules",
              file=sys.stderr)
        return 2

    src_fm = parse_frontmatter((src / "SKILL.md").read_text(
        encoding="utf-8", errors="replace"))
    desc = src_fm.get("description", "")
    if len(desc) > 1024:
        desc = desc[:1021] + "..."
        warnings.append("description truncated to 1024 chars")

    actions: list[str] = []
    if args.target == "api":
        skill = {
            "name": args.name,
            "definition": {
                "description": desc,
                "body": "<!-- fill: converted instruction text, no frontmatter -->",
                "assets": {},
            },
            "notes": f"Ported from {src.name}",
            "sharingScope": "private",
        }
        for sub in ("references", "assets", "scripts"):
            d = src / sub
            if d.is_dir():
                for p in d.rglob("*"):
                    if p.is_file():
                        rel = f"{sub}/{p.relative_to(d).as_posix()}"
                        try:
                            skill["definition"]["assets"][rel] = {
                                "textContent": p.read_text(encoding="utf-8"),
                                "isExecutable": p.suffix == ".py",
                            }
                        except UnicodeDecodeError:
                            skill["definition"]["assets"][rel] = {
                                "rawContent": base64.b64encode(
                                    p.read_bytes()).decode(),
                                "isExecutable": p.suffix == ".py",
                            }
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{args.name}.skills-api.json").write_text(
            json.dumps(skill, indent=2, ensure_ascii=False), encoding="utf-8")
        actions.append(f"wrote {args.name}.skills-api.json (fill definition.body, review assets)")

    else:
        skill_dir = out / args.name
        skill_dir.mkdir(parents=True, exist_ok=True)
        fm_lines = ["---", f"name: {args.name}",
                    f"description: \"{desc}\""]
        if args.target == "vibe-code":
            fm_lines.append("user-invocable: true")
        fm_lines += [
            "license: MIT",
            "metadata:",
            f"  ported_from: \"{src.name}\"",
            "---",
        ]
        (skill_dir / "SKILL.md").write_text(
            "\n".join(fm_lines) + "\n\n# <skill title>\n\n<!-- fill: converted body -->\n",
            encoding="utf-8")
        actions.append("wrote SKILL.md stub")

        for sub in ("references", "assets"):
            d = src / sub
            if d.is_dir():
                shutil.copytree(d, skill_dir / sub, dirs_exist_ok=True)
                actions.append(f"copied {sub}/")

        if args.target == "vibe-work":
            attachment_count = 0
            for sub in ("references", "assets"):
                sub_dir = skill_dir / sub
                if sub_dir.is_dir():
                    attachment_count += sum(
                        1 for p in sub_dir.rglob("*") if p.is_file())
            if attachment_count > MERGE_CAP:
                warnings.append(
                    f"{attachment_count} attached files exceed the ~{MERGE_CAP} guideline — merge related references and repoint ALL cross-file references")
            if (src / "scripts").is_dir():
                shutil.copytree(src / "scripts", skill_dir / "scripts",
                                dirs_exist_ok=True)
                warnings.append("Work target: scripts/ copied as attachments — rewrite body examples per the mapping tables (interpreter-first, instruction fallback)")
        else:  # vibe-code
            if (src / "scripts").is_dir():
                shutil.copytree(src / "scripts", skill_dir / "scripts",
                                dirs_exist_ok=True)
                actions.append("copied scripts/ (add runtime note: bash: python3 scripts/…)")
            for f in ("agents/openai.yaml",):
                if (src / f).is_file():
                    (skill_dir / "agents").mkdir(exist_ok=True)
                    shutil.copy2(src / f, skill_dir / f)
                    actions.append("preserved agents/openai.yaml (Vibe Code reads it natively)")
        actions.append(f"next: fill the body, then run scripts/validate_skill.py {skill_dir} --target {args.target}")

    report = {"name": args.name, "target": args.target, "out": str(out),
              "actions": actions, "warnings": warnings}
    print(json.dumps(report, indent=2) if args.json else "\n".join(
        [f"{'WARN: ' if a in warnings else ''}{a}" for a in actions + warnings]))
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
