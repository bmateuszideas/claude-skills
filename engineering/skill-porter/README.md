# skill-porter — Design & Technical Documentation

How this skill was built, what each file does, the conversion pipeline it
teaches, and how the two source platforms (Anthropic Claude Code vs OpenAI
Codex) differ when mapping to Mistral.

## 1. Origin — where every rule comes from

Nothing in this skill was invented. Every constraint was extracted from two
authoritative sources, then condensed into instructions a Mistral model can
follow at conversion time:

| Source | What was mined from it |
|---|---|
| `mistralai/mistral-vibe` (source code, cloned) | `vibe/core/skills/parser.py` — exact frontmatter parsing (`FM_BOUNDARY = ^-{3,}$`, YAML); `vibe/core/skills/models.py` — pydantic `SkillMetadata` (name regex `^[a-z0-9]+(-[a-z0-9]+)*$` ≤64 chars, description ≤1024, `allowed-tools`, `user-invocable`, `disable-model-invocation`); `vibe/core/skills/manager.py` — flat discovery (only direct child dirs of a skill path), `/name` invocation only when `user-invocable: true`, reserved builtin names, native `agents/openai.yaml` (Codex) bridge; `vibe/core/tools/base.py` + `tools/builtins/` — real tool registry via `get_name()` = snake_case class name |
| `mistralai/platform-docs-public` (docs source of docs.mistral.ai, cloned) | `vibe/work/skills` + quickstart `create-first-skill` — Work skill mechanics (New Skill form: Title/Description/SKILL.md, attached files, progressive disclosure, description-as-trigger, file-count limit, Personal vs Workspace); `studio/create-skill` — Studio `Build > Skills`, `Publish to Vibe`, versioning; `api/endpoint/beta/skills` — Skills API schema: `POST /v2/skills` with `definition.description` / `definition.body` / `definition.assets` (`textContent` \| `rawContent` + `isExecutable`), `sharingScope`, `aliases`, `POST /v2/skills/{id}/versions` |
| agentskills.io/specification | The shared Agent Skills standard: name/description constraints, optional dirs (`scripts/`, `references/`, `assets/`), progressive disclosure, ≤500-line body guidance |

Verification performed before delivery: the emitted `SKILL.md` was parsed and
validated **with the real Vibe parser + pydantic `SkillMetadata`** from the
cloned mistral-vibe repo (result: parse OK, name valid, description 786/1024,
body 171 lines), plus the repo's own linters (`check_frontmatter.py`,
`check_skill_names.py`) — 0 errors.

## 2. Package layout — what is in each folder

```
engineering/skill-porter/
├── SKILL.md                                  # The skill itself — instructions the
│                                             # converting model loads on activation
└── references/
    └── mistral-platform-spec.md              # Hard facts (loaded on demand)
```

### `SKILL.md` (the resident core, ~170 lines)
Loaded into context only when a conversion task activates the skill. Contains
the decision logic:

- **Three-target table** — Vibe Work / Vibe Code CLI / Skills API, with what
  the deliverable looks like for each.
- **Non-negotiable format rules** — the name regex, description-as-trigger,
  which frontmatter fields survive per target, ≤500-line body discipline.
- **Tool-call translation table** — the #1 failure cause of raw ports: Claude
  tool names (Read/Write/Edit/Bash/Grep/Glob/WebSearch/WebFetch/Task/
  TodoWrite/AskUserQuestion) mapped to Vibe Code tools, Vibe Work equivalents,
  and an honest fallback ("do not invent a Mistral tool that does not exist —
  leave a `[porter note]`").
- **Source-package reading order** — identify platform → read everything →
  classify each supporting item (references copy, assets copy, scripts get a
  per-runtime decision tree, commands become mini-skills or Workflow sections,
  agents become TOML or inline persona).
- **Output contracts** — the exact deliverable layout per target, including
  the `POST /v2/skills` JSON skeleton.
- **Workflow (6 ordered steps)** — Ingest → Understand → Choose target →
  Rewrite → Self-review ("re-read your output as if you were the Mistral model
  that just had it activated") → Deliver + port report.
- **Anti-patterns** — blind copy, vague description rewrites, silent script
  drops, invented tool names.

### `references/mistral-platform-spec.md` (on-demand reference, ~150 lines)
Not loaded until the model needs a hard fact. Contains the full evidence:
frontmatter validation contract, complete Vibe tool registry, discovery
mechanics, the Codex `agents/openai.yaml` bridge schema, Vibe Work mechanics +
built-in skill list (style reference for trigger-writing), the Skills API
field table, the Claude/Codex package anatomy, and an extended
tool-name→intent table for cases the SKILL.md table doesn't cover.

This split follows the progressive-disclosure pattern the skill itself
teaches: small resident core, details on demand.

## 3. The conversion pipeline the skill encodes

```
 INPUT                     UNDERSTAND                REWRITE                 DELIVER
┌─────────────────┐   ┌──────────────────┐   ┌───────────────────┐   ┌──────────────┐
│ Claude or Codex │ → │ identify platform │ → │ frontmatter fix    │ → │ target folder │
│ skill package   │   │ read every file   │   │ tool-call rewrite  │   │ + port report │
│ SKILL.md +      │   │ state the purpose │   │ commands → skills  │   │ (Work / CLI / │
│ scripts/referen- │   │ classify items    │   │ agents → TOML/per- │   │  API JSON)    │
│ ces/assets/cmds/ │   │                   │   │ sona, scripts →    │   └──────────────┘
│ agents/          │   │                   │   │ keep|inline|flag   │   + self-review
└─────────────────┘   └──────────────────┘   └───────────────────┘
```

Per-item decision matrix taught by the skill:

| Item | Vibe Code CLI | Vibe Work | Skills API |
|---|---|---|---|
| `SKILL.md` body | keep, rewrite tool names | keep, strip CLI fields, rewrite to no-filesystem phrasing | → `definition.body` |
| `description` | keep ≤1024 | rewrite as "Use when…" trigger | → `definition.description` |
| `references/*.md` | copy 1:1 | attach as files | `assets` `textContent` |
| `assets/*` | copy 1:1 | attach as files | `assets` |
| `scripts/*` | keep + runtime note (`bash: python3 …`) | short/pure → inline as steps; complex → attach; filesystem-bound → report "CLI-only" | `rawContent` + `isExecutable: true` |
| `commands/*.md` | one mini-skill each, `user-invocable: true` | fold into body as "Workflows" section | fold into `body` |
| `agents/*.md` | `.vibe/agents/<name>.toml` | inline persona into body | fold into `body` |
| `.claude-plugin/` | drop | drop | drop |
| `agents/openai.yaml` | **keep** (Vibe reads it natively) | drop | drop |

## 4. Claude vs OpenAI Codex — why the mapping differs

The two source platforms package skills differently, and the skill encodes
both anatomies:

| Aspect | Anthropic Claude Code | OpenAI Codex |
|---|---|---|
| Core file | `SKILL.md` (YAML frontmatter: `name`, `description`, optional `metadata`) | `SKILL.md` — same Agent Skills core |
| Slash commands | `commands/*.md` — **separate files**, each with its own frontmatter (`name`, `description`) and body; invoked as `/command` in Claude Code | No per-command markdown convention to carry over; behavior tends to live in the skill body |
| Personas / subagents | `agents/*.md` — markdown with frontmatter (`name`, `description`, `tools: [Read, Write, …]`, `model:`) | `agents/openai.yaml` — **YAML metadata file** with `policy:` (`allow_implicit_invocation`, `products`) |
| Plugin manifest | `.claude-plugin/plugin.json` (author object, version, repo) | none equivalent |
| Platform bridge | none — Claude fields must be translated by the porter | **native**: Vibe Code reads `agents/openai.yaml` itself (`load_openai_skill_metadata` in `skills/parser.py`), so a Codex skill ported to the CLI can keep it as-is |
| Tool names in body | Claude Code set: `Read`, `Write`, `Edit`, `MultiEdit`, `Bash`, `Grep`, `Glob`, `WebSearch`, `WebFetch`, `Task`, `TodoWrite`, `AskUserQuestion` | Codex uses shell/filesystem phrasing closer to generic agents, but any Claude-style references get the same table |

Practical consequence encoded in the skill: porting **Claude** packages is a
heavier rewrite (commands → mini-skills, agents → TOML, tool table applied
aggressively); porting **Codex** packages to the CLI target is lighter (keep
`agents/openai.yaml`, mostly frontmatter hygiene + tool-name checks), while
Work/API targets still strip it because the cloud skill object has no notion
of Codex policies.

## 5. Frontmatter per target (what survives)

```
Claude/Codex in              vibe-code out            vibe-work out        API out
─────────────────            ──────────────           ─────────────        ─────────────
name                  →      name (regex-checked)    name                 name
description           →      description (≤1024)      description-as-      definition.description
                             allowed-tools (mapped)    trigger             definition.body ← body
                             user-invocable            (no CLI fields)
                             license/compatibility/
                             metadata (optional)
```
