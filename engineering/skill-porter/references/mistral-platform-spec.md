# Mistral Platform Hard Reference

Facts below are extracted from the Mistral Vibe source code
(`mistralai/mistral-vibe`, `vibe/core/skills/*` and `vibe/core/tools/*`) and the
Mistral documentation repo (`mistralai/platform-docs-public`). Treat them as
authoritative when converting.

## SKILL.md frontmatter — validation contract (Vibe Code CLI)

Parsed with `parse_skill_markdown`: frontmatter must start at line 1 with `---`
and be valid YAML. Validated with pydantic `SkillMetadata`:

| Field | Type | Constraint |
|---|---|---|
| `name` | str | 1–64 chars, regex `^[a-z0-9]+(-[a-z0-9]+)*$`, must match parent dir |
| `description` | str | 1–1024 chars |
| `license` | str, optional | any |
| `compatibility` | str, optional | ≤500 chars |
| `metadata` | map[str,str], optional | all values coerced to strings |
| `allowed-tools` | str or list | space-delimited or YAML list |
| `user-invocable` | bool, default `true` | `false` hides it from `/name` |
| `disable-model-invocation` | bool, default `false` | `true` = user-only skill |

Unknown frontmatter fields are ignored, not rejected. A SKILL.md that fails to
parse is silently dropped by the CLI (a toast shows the parse failure) — always
self-validate before delivering.

## Vibe Code tool registry (from `BaseTool.get_name()`, snake_case of class)

`bash`, `edit`, `exit_plan_mode`, `git_bash`, `grep`, `read_file`,
`search_replace`, `skill`, `task`, `todo`, `web_fetch`, `web_search`,
`ask_user_question`, `write_file`, plus MCP and connector tools when
configured. Anything else named in a Claude skill does not exist.

## Skill discovery (Vibe Code CLI)

- `config.toml` → `skill_paths = ["…"]` (custom, global scope)
- `./.vibe/skills/` or `./.agents/skills/` (project, trusted workdir only)
- `~/.vibe/skills/` (user-global)
- Discovery is **flat**: only direct child directories of a skill path are
  scanned; each must contain `SKILL.md`. Nested `<domain>/<skill>/` layouts
  are NOT discovered.
- Reserved names (builtins) cannot be overridden: `vibe`, `skill-creator`.
- `/{skill-name}` invocation requires `user-invocable: true`; text after the
  name is passed as extra instructions.

## Codex compatibility bridge

Vibe Code natively reads `agents/openai.yaml` inside a skill folder (Codex
skill metadata). Schema: `policy:` with optional `allow_implicit_invocation:
bool` and `products: [str]`. Preserve this file when porting a Codex skill to
the CLI target; drop it for Work/API targets.

## Vibe Work (chat.mistral.ai) mechanics

- Skills created under `Context > Skills` → New Skill: fields Title,
  Description, SKILL.md; optional attached files/folders.
- Progressive disclosure: (1) discovery loads only name+description (~100
  tokens each), (2) activation loads the full SKILL.md body when the task
  matches the description, (3) execution reads attached files on demand.
- Invocation: automatic on description match, or explicit `/{skill-name}`, or
  natural mention ("use the contract-review Skill").
- Supporting files are subject to a file-count limit; keep references focused,
  merge when porting large packages.
- Sharing: Personal vs Workspace; workspace admins can force-enable.
- Built-in Work skills (style reference for trigger-writing):
  `challenge-my-thinking`, `data-analysis`, `deep-research`,
  `doc-coauthoring`, `document-review`, `internal-comms`, `meeting-prep`,
  `research-synthesis`, `skill-creator`, `stakeholder-translator`,
  `structured-extraction`, `vibe-work-onboarding`.

## Mistral Skills API (beta) — cloud format

Endpoints: `GET /v2/skills`, `POST /v2/skills`, `POST /v2/skills/{id}/versions`.

`POST /v2/skills` request body:

| Field | Type | Notes |
|---|---|---|
| `name` | str | kebab-case, as frontmatter |
| `definition.description` | str | activation trigger |
| `definition.body` | str | full instruction text (SKILL.md body, no frontmatter) |
| `definition.assets` | map | filename → `{rawContent, isExecutable}` or `{textContent, isExecutable}` |
| `notes` | str | version notes |
| `sharingScope` | str | `private` \| `workspace` |
| `aliases` | [str] | e.g. `["production"]` |

Asset entry: `rawContent` (string, base64 for binary) or `textContent`
(plain text); `isExecutable: true` marks runnable assets (scripts).
Skills are versioned: saving changes creates a new version; older versions
stay available for rollback. Studio (`Build > Skills`) is the GUI for the
same object; `Publish to Vibe` makes a Studio skill available in Vibe Work.

## Claude Code skill package anatomy (input side)

```
<skill>/
├── SKILL.md               # frontmatter: name, description (+ optional metadata)
├── .claude-plugin/plugin.json   # Claude plugin manifest — DROP for Mistral
├── commands/*.md           # slash commands: frontmatter name/description + body
├── agents/*.md            # personas: frontmatter name/description/tools/model
├── scripts/*              # usually stdlib-only Python CLIs
├── references/*.md        # on-demand knowledge
└── assets/*               # templates, samples, data
```

Codex variant: same tree plus optional `agents/openai.yaml`.

## Claude tool-name → intent table (use when the table in SKILL.md is not enough)

- `Read(path)` → intent: load file content. CLI: `read_file`. Work: attached
  file or ask user to paste.
- `Write(path, content)` → intent: create file. CLI: `write_file`. Work:
  output in response/Canvas.
- `Edit(path, old, new)` → intent: surgical replace. CLI: `search_replace`.
  Work: regenerate the corrected full content.
- `Bash(cmd)` → intent: run a command. CLI: `bash`. Work: Code Interpreter or
  restructure as explicit steps.
- `Glob(pattern)` → intent: list files. CLI: `grep`/`bash ls`. Work: ask user
  for the file list.
- `WebFetch(url)` → intent: get page content. CLI: `web_fetch`. Work: ask user
  to paste, or use web search result snippets.
