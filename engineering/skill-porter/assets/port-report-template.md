# Port Report Template

Fill this after every conversion and deliver it with the package.

---

## Port Report — `<source-name>` → `<target>`

**Source platform:** claude-code | codex
**Source package:** `<name>` (<n> files: SKILL.md, scripts/x…, references/x…, commands/x…, agents/x…)
**Target:** vibe-work | vibe-code | skills-api
**Surviving usefulness:** content **<N>%** · operating environment **<N>%**

### What mapped to what

| Source mechanism | Intent | Target expression |
|---|---|---|
| e.g. `PreToolUse` hook `security-guard.json` | block dangerous bash before run | CLI: `hooks.toml` `pre_tool` (deny + reason); Work: body rule "never run rm -rf…" |
| e.g. `scripts/<calculator>.py` | deterministic ranking | Work: Code Interpreter run on uploaded CSV (fallback: formula in body) |

### What could not be ported (and why)

| Element | Why | What happens instead |
|---|---|---|
| e.g. `init_vault.py` walking the user's disk | Work sandbox cannot reach the user's system | CLI-only capability; on Work the skill works as methodology |

### Changes made

- Frontmatter: <fields added/stripped/rewritten>
- Tool calls rewritten: <count> (Read→read_file: n, Bash→interpreter: n, …)
- Commands: <each source command → mini-skill / workflow section>
- Agents: <each source agent → TOML with fields / inline persona>
- Scripts: <kept / interpreter / formula-inline / tallied / flagged CLI-only>
- Env vars & paths: <each `${VAR}` → replacement>
- Cross-file references repointed after merging: <list>

### Import steps (target-specific)

- vibe-work: Context > Skills > New Skill → Title: <human title> · Description: <one-liner> → paste SKILL.md body → attach: <file list>
- vibe-code: `cp -r <name> ~/.vibe/skills/` → `/{name}` (user-invocable) · per-command mini-skills + `.vibe/agents/*.toml` paths
- skills-api: `POST /v2/skills` with `<name>.skills-api.json` (review `definition.body` first)

### Validation

`scripts/validate_skill.py <dir> --target <t>` → VALID / issues fixed (list)
