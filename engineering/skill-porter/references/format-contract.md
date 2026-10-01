# Format Contract — per-target SKILL.md rules and validation

The exact, checkable constraints for each Mistral target. Every rule here is
machine-verifiable; `scripts/validate_skill.py` enforces them.

## Shared Agent Skills core (all targets)

- `SKILL.md` starts with YAML frontmatter delimited by `---` on the first
  line, closed by `---`.
- `name`: 1–64 chars; only `a-z`, `0-9`, hyphens; no leading/trailing hyphen;
  no `--`; regex `^[a-z0-9]+(-[a-z0-9]+)*$`; must equal the parent directory
  name. Colon-namespaced source commands (`cs:pulse`) must be sanitized
  (`cs-pulse`).
- `description`: 1–1024 chars, non-empty; written as an activation trigger
  ("Use when…") because discovery loads only name+description (~100 tokens)
  and decides activation from that text alone.
- Optional fields: `license` (short), `compatibility` (1–500 chars),
  `metadata` (string→string map), `allowed-tools` (space-separated or YAML
  list; experimental).
- Body: keep under 500 lines; point to `references/` files with relative
  paths from the skill root, one level deep.
- Progressive disclosure: metadata (~100 tokens) → SKILL.md body on
  activation (< 5000 tokens recommended) → referenced files on demand.

## Vibe Code CLI specifics

Extra frontmatter fields the CLI reads (from `vibe/core/skills/models.py`):

| Field | Type | Default | Meaning |
|---|---|---|---|
| `user-invocable` | bool | `true` | `false` hides the skill from the `/` menu and blocks direct `/{name}` invocation (model can still load it) |
| `disable-model-invocation` | bool | `false` | `true` = only the user can invoke it |
| `allowed-tools` | str or list | — | restricts the tools the skill may call; names must be real Vibe tools |

Valid tool names: `bash`, `edit`, `exit_plan_mode`, `git_bash`, `grep`,
`read_file`, `search_replace`, `skill`, `task`, `todo`, `web_fetch`,
`web_search`, `ask_user_question`, `write_file`, plus configured MCP/
connector tools.

Reserved names (builtins, cannot be overridden): `vibe`, `skill-creator`.

Layout: flat — one directory per skill directly under a skill path
(`~/.vibe/skills/<name>/SKILL.md`). Nested `<domain>/<skill>/` layouts are
NOT discovered. A SKILL.md that fails to parse is silently dropped.

Slash commands: `/{skill-name}` works only with `user-invocable: true`;
text after the name is passed to the skill as extra instructions.

Codex bridge: the CLI natively reads `agents/openai.yaml` inside a skill
folder. Schema: `policy:` → optional `allow_implicit_invocation: bool` and
`products: [str]`. Preserve this file when porting a Codex skill to the CLI;
map `allow_implicit_invocation: false` to
`disable-model-invocation: true` semantics and say so in the report.

## Vibe Work specifics

- No CLI frontmatter fields: strip `user-invocable`, `allowed-tools`,
  `disable-model-invocation`, `agents/openai.yaml`. Work activates by
  description match; every enabled skill is `/{name}`-invocable.
- Import via `Context > Skills > New Skill`: Title (human-readable),
  Description (trigger), SKILL.md body, attached files/folders. Supporting
  files are subject to a file-count limit — when the package has more than
  ~10 files, merge related ones (e.g. collapse 8 references into 2–3) and
  repoint ALL cross-file references (body→references,
  references→references, references→assets).
- Attachments: markdown, CSV, templates all work; they load on demand.
- Deliverables the skill body can rely on: Canvas documents, chat tables,
  Code Interpreter output, downloadable files.

## Mistral Skills API specifics

- Frontmatter does not travel: the API object is JSON. Map:
  - `name` → `"name"`
  - `description` → `"definition.description"`
  - body → `"definition.body"` (full instruction text, no frontmatter)
  - `references/*`, `assets/*` → `"definition.assets"` entries with
    `textContent` (plain text) or `rawContent` (base64 for binary) and
    `isExecutable` (`true` for scripts)
  - provenance → `"notes"`
- `"sharingScope"`: `"private"` | `"workspace"`.
- Versioned: changes create a new version via
  `POST /v2/skills/{id}/versions`; keep `aliases` (e.g. `production`)
  stable across versions.
- Studio `Build > Skills` is the GUI for the same object; `Publish to Vibe`
  surfaces it in Vibe Work.
