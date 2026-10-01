# Output Templates — paste-ready skeletons per target

Fill-in skeletons the converting model emits. Keep frontmatter rules from
`references/format-contract.md` (name regex, description ≤1024, etc.).

## 1. Vibe Work — SKILL.md body (no CLI-only frontmatter)

```markdown
---
name: <kebab-name>
description: "Use when <trigger phrases>. <What it produces>."
license: MIT
metadata:
  ported_from: "<platform>/<original-name>"
---

# <Skill Title>

<One-paragraph overview: what this does and when to use it.>

## Workflow

<Numbered steps the model follows on activation. Where the source used
tools/files, phrase for Work: "read the attached <file>", "produce the
result as a table in the chat", "open the deliverable in Canvas".>

## Runtime paths (capabilities used)

- Files (attachments): <list which attached files this skill expects>
- Canvas: <deliverables produced as documents>
- Code Interpreter: <computations run as Python; note paid-plan fallback:
  the same computation expressed as body instructions>
- Running state: <tallies the model maintains across steps, e.g. the
  sent/received/cited table>

## Workflows (former slash commands)

### <workflow-name> — <former /command>
**Trigger:** the user asks for <intent>.
<Steps>

## References (attached files — load on demand)

- `<file>` — <what it contains, when to read it>
```

## 2. Vibe Code CLI — SKILL.md (frontmatter + flat layout)

```markdown
---
name: <kebab-name>            # must equal the folder name
description: "Use when <triggers>. <What it does>."
user-invocable: true          # makes /<name> available
allowed-tools: bash read_file write_file   # only real Vibe tools
license: MIT
metadata:
  ported_from: "<platform>/<original-name>"
---

# <Skill Title>

## Runtime note

Scripts live in this skill's directory. Run them from the skill root:
`bash: python3 scripts/<tool>.py --help`.

## Workflow
<Steps, using Vibe tool names: read_file, grep, bash, web_search, web_fetch, task…>

## Sub-agents (this skill ships)
| Agent file | Purpose |
|---|---|
| `.vibe/agents/<name>.toml` | <role; agent_type subagent; enabled_tools …> |

## Slash commands (this skill ships)
| Skill | Purpose |
|---|---|
| `<name>-<command>/SKILL.md` | <former /command; user-invocable: true> |
```

Per-command mini-skill frontmatter:

```markdown
---
name: <kebab-name>-<command>
description: "Use when the user runs /<command> or asks for <intent>."
user-invocable: true
---
```

Sub-agent TOML (`.vibe/agents/<name>.toml`):

```toml
agent_type = "subagent"
display_name = "<Name>"
description = "<role and when to spawn>"
safety = "safe"
enabled_tools = ["read_file", "grep", "bash"]
```

## 3. Skills API — POST /v2/skills JSON

```json
{
  "name": "<kebab-name>",
  "definition": {
    "description": "Use when <trigger>.",
    "body": "<full instruction text — SKILL.md body, no frontmatter>",
    "assets": {
      "references/<file>.md": {"textContent": "<content>", "isExecutable": false},
      "scripts/<file>.py": {"rawContent": "<base64>", "isExecutable": true}
    }
  },
  "notes": "Ported from <platform>/<original-name> · <what changed>",
  "sharingScope": "private",
  "aliases": ["production"]
}
```

## 4. Per-command mini-skill (Vibe Code) — body pattern

```markdown
# <Command Title>

Formerly `/<command>` on <source platform>. Invoked as `/<kebab-name>-<command>`.

## Usage
/<kebab-name>-<command> <args> — <what it does>

## Steps
<The command body, converted: tool names remapped, paths relative to the
skill root, flags explained in prose.>
```
