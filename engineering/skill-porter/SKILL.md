---
name: skill-porter
description: "Converts complete skill packages (SKILL.md + scripts/ + references/ + assets/ + commands/ + agents/) from Claude Code or OpenAI Codex into fully working Mistral formats: Vibe Code CLI (~/.vibe/skills/), Vibe Work (chat.mistral.ai Context > Skills), and the Mistral Skills API (POST /v2/skills). Use when the user pastes or uploads a skill folder from Anthropic/Claude/Codex and wants it working in Mistral, when a raw Claude skill loaded into Mistral misbehaves (unknown tools like Read/Write/Edit/WebSearch, dead scripts, ignored commands), or when the user asks to port/migrate/translate an agent skill between platforms. The model doing the conversion reasons over the skill's purpose, rewrites tool calls, remaps commands, and emits a Mistral-native package — not a blind file copy."
license: MIT
metadata:
  version: "1.0.0"
  author: "claude-skills"
  category: engineering
---

# Skill Porter — Claude/Codex → Mistral Vibe

You are converting a **skill package** — a folder of instructions plus supporting
files that gives an AI agent domain expertise — from its native platform
(Claude Code or OpenAI Codex) into one of the three Mistral targets. This is
intelligence work, not a file copy: you must understand **what the skill is
trying to accomplish**, then re-express it so a Mistral model executes it
correctly.

## Rule zero: map capabilities intelligently — never force-port, never auto-reject

Mistral is not a replica of Anthropic's platform — but it is not a barren
subset either. Mistral Vibe has its own hooks, subagents, MCP support and
permission system; they are younger and smaller than Anthropic's pioneers,
so a Claude skill's mechanisms will rarely map one-to-one. Your job is
**capability mapping**, not gatekeeping: for every mechanism the source skill
uses, ask "what is this *for*, and how can the Mistral target express the
same intent?" Often the same result is reachable by a different route
(a − b may equal a + c). Only after mapping do you judge what survives.

### Capability map (Claude mechanism → Mistral expression)

| Claude mechanism | Mistral expression — use it when it covers the intent |
|---|---|
| `PreToolUse` / `PostToolUse` hooks | Vibe Code `hooks.toml`: `pre_tool` (deny or **rewrite tool arguments**), `post_tool` (replace/append output, audit). Subagents inherit hooks. Work/API targets: no hooks — fold the hook's *policy* into the SKILL.md body as explicit rules the model enforces itself. |
| Lifecycle hooks (SessionStart, Stop, UserPromptSubmit, PreCompact, Notification) | Vibe has `post_agent` (fires after each assistant turn; can deny with a reason → retry). Others have no event twin: re-express as body instructions (e.g. a "at session start, first do X" checklist) or a scheduled/manual step. |
| `Task` subagent trees (multi-hop, per-agent tool allow-lists, inter-agent messaging) | Vibe subagents exist: `.vibe/agents/<name>.toml` (`agent_type = "agent"|"subagent"`, `enabled_tools`, `disabled_tools`, permissions, `system_prompt_id`) spawned via the `task` tool — text-only results, single hop. Map shallow trees directly; for deep trees, flatten into sequential `task` calls orchestrated by the main agent, or inline the persona as a body section. |
| Bundled MCP servers | Vibe Code: `.vibe/mcp.json` config; Work: Connectors. The *server* is infrastructure, not skill logic — port the skill to consume the tools, and tell the user the server must be deployed/configured separately. |
| `.claude-plugin/` manifest, marketplace | No equivalent. Drop; the skill itself is the unit on Mistral. |
| Per-tool permission policies | Vibe agents' `[tools.<name>] permission` tables and skill-level `allowed-tools` frontmatter. |
| Shell/env variables embedded in body text and paths (`${RESEARCH_DIR}`, `$(date +%Y-%m-%d)`, `~/.pulse_sessions/`) | These assume a shell + persistent filesystem. CLI target: keep, they work under `bash`. Work/API target: replace every one — output paths become "produce the briefing in the chat/Canvas", state directories become conversation state (see stateful scripts below). Never leave a `${VAR}` reference in a Work body. |
| **Formula-maskable scripts** (a long script whose core is one deterministic formula or rule — e.g. a 300-line RICE calculator that is really `(Reach × Impact × Confidence) / Effort` plus CSV plumbing) | CLI: keep the script. Work/API: do NOT attach the script — replace every usage example in the body with the formula/rule written out as an instruction ("for each feature compute R = R×I×C/E, rank in a table") plus a worked example using the skill's own sample data asset. Report the substitution. |
| **Text-analysis scripts** (heuristically parse transcripts/notes into insights — e.g. an interview analyzer) | CLI: keep. Work/API: replace with an explicit analysis instruction in the body (input format → what to extract → output structure). The model reading the transcript natively is usually *better* than the heuristic script — say that in the report; this is a capability upgrade, not a degradation. |
| **Script-flag examples in the body** (bash blocks showing `python scripts/x.py input.csv --capacity 15 --output json > out.json`, `sample` subcommands that generate working files) | CLI: keep, they run under `bash`. Work/API: rewrite each block — flags become instruction parameters ("with a capacity of 15…"), output redirects become "produce the table/JSON in your answer", and `sample`-generator subcommands are replaced by pointing at the skill's example data assets. |
| **Stateful scripts** (a script whose *value* is persisting state across workflow steps: counters, session logs, dedup caches, e.g. `citation_tracker.py` writing `~/.pulse_sessions/<id>.json`) | CLI: keep as-is. Work/API: the filesystem persistence is unportable — port the *tally* into the body as an explicit "running state" pattern the model maintains in the conversation (e.g. a three-count table: queries sent / sources received / sources cited, updated at each phase). Name the pattern in the report; do not attach the script and pretend it runs. |
| `model:` field (persona tuned to a specific Claude model) | Drop the pin; note behavioral calibration may shift and watch for it in self-review. |
| `context: fork` on an agent (subagent runs in a forked session) | Vibe subagents run as fresh independent sessions by design — the isolation intent is already the default; drop the field and verify the agent's prompt is self-contained (no reliance on parent-session state). |
| Platform branding in the body ("Claude Code", "this plugin", "works with Codex") | Rewrite to the target's name ("Vibe", "this skill") or neutral "your agent". Also sweep asset/template filenames like CLAUDE.md.template: keep the file if it seeds an AGENTS.md-style instruction doc, but rename or re-point it (Vibe reads AGENTS.md, not CLAUDE.md) and update every reference to it. |
| Cross-reference tables in the body listing source-platform commands (`/wiki-ingest <path>` etc.) | After converting commands to mini-skills/workflows, rewrite the table to the NEW invocation map on the target — a stale table pointing at Claude commands is a silent failure. |

### How to reason (the part no table can do for you)

1. **Intent first.** For each mechanism, name the user-visible job it does
   ("block dangerous shell commands", "inject project context at start",
   "fan out research across 3 personas").
2. **Search the target for an expression of that intent** — direct twin,
   different route, or body-instruction the model itself enforces.
3. **Compose.** One Claude mechanism may need two Mistral pieces (hook →
   `pre_tool` + a body rule); several Claude mechanisms may collapse into one.
4. **Score honestly — twice.** First **per element** (mechanism by mechanism). Then **for the whole skill**: ask "where does this skill's core value actually live — in knowledge, or in a local environment?" A skill like a personal-wiki maintainer can be 100% portable knowledge for the CLI target and yet nearly useless on Work, because its whole point is operating on a folder of files on a local disk. The Work port still has value (methodology, structures, prompts) but the model must name that class of gap explicitly in the report: "on Work this skill works as a methodology, not as a file tool." Estimate the surviving usefulness fraction for BOTH dimensions — content and operating environment — before delivering. 90%? Port, and say what the missing 10% was. Core mechanism genuinely unexpressible on the chosen target? Say so — but only after you have tried the map, not because the file mentioned a hook and you flinched. A forced port that ships a dead centerpiece is a failure; so is a lazy refusal of an 80%-portable skill. Deliver the honest maximum.

## The three Mistral targets (pick from user intent, ask only if unclear)

| Target | Where it runs | What you deliver |
|---|---|---|
| **Vibe Work** (chat.mistral.ai, Work tab) | Online chat. Skills live in `Context > Skills`. No filesystem tools. | A folder: rewritten `SKILL.md` + supporting files, ready to paste into the New Skill form (Title / Description / SKILL.md body / attached files). Progressive disclosure: description decides auto-activation; body loads on activation; attached files load on demand. |
| **Vibe Code CLI** | Terminal coding agent. Skills live at `~/.vibe/skills/<name>/` (user) or `./.vibe/skills/` (project). Full filesystem access via tools. | A folder with converted `SKILL.md` (flat layout — one directory per skill directly under `skills/`, no nesting), preserving `scripts/`, `references/`, `assets/`. |
| **Mistral Skills API** (console.mistral.ai, Studio) | Cloud, versioned, shareable. | A JSON body for `POST /v2/skills` (see schema below), or — simpler — a skill created in Studio `Build > Skills` then `Publish to Vibe`. |

## Non-negotiable format rules (hard Mistral validation)

1. **`name`**: 1–64 chars, only `a-z`, `0-9`, hyphens. No uppercase, no leading/trailing hyphen, no double hyphens. Must match the parent folder name. If the source name violates this (e.g. `MySkill`, `pdf--tools`, or a namespaced command like `cs:pulse` — colons are illegal), rewrite it (e.g. `cs-pulse`) and tell the user.
2. **`description`**: 1–1024 chars, non-empty. This is the **activation trigger**. Rewrite it as "Use when …" with the skill's concrete trigger phrases — a Mistral model decides from this text alone whether to load the skill. Vague descriptions ("Helps with PDFs") are failures.
3. **Frontmatter fields** for the Vibe Code target: `name`, `description`, optionally `license`, `compatibility`, `metadata`, `allowed-tools`, `user-invocable`, `disable-model-invocation`. Drop all Claude-specific fields (e.g. nested `metadata.author` blocks are fine, but no Claude plugin fields).
4. **For Vibe Work / Skills API**: no `allowed-tools`, no `user-invocable` — Work activates skills by description matching and `/name`; there are no CLI tool names to allow-list. Strip them.
5. **Body**: keep under ~500 lines; move long material into supporting files (`references/…`) and point to them with relative paths from the skill root.

## Tool call translation (the #1 reason raw ports fail)

Claude skills name Claude Code tools in their instructions. Mistral models will
not recognize them and either stall or hallucinate a failure. Find every tool
reference in `SKILL.md`, `references/*`, `commands/*` and rewrite it:

| Claude Code | Vibe Code CLI equivalent | Vibe Work equivalent |
|---|---|---|
| `Read` | `read_file` | "read the attached file" / paste content into the task |
| `Write` | `write_file` | produce the content in the response / Canvas |
| `Edit`, `MultiEdit` | `search_replace`, `edit` | regenerate the full corrected content |
| `Bash`, `Shell` | `bash` | Code Interpreter (if available) or rewrite as explicit step-by-step instructions |
| `Grep` / `Glob` | `grep` | instruct the model to search within the pasted/attached material |
| `WebSearch` | `web_search` | web search feature / `deep-research` pattern |
| `WebFetch` | `web_fetch` | fetch URL content if available; else ask user to paste |
| `Task` (subagent) | `task` (Vibe subagents, `.vibe/agents/*.toml`) | inline the subagent's instructions as a section |
| `TodoWrite` | `todo` | describe the plan in the response |
| `AskUserQuestion` | `ask_user_question` | ask directly in chat (natural) |
| `SLASH commands` (`/foo`) | only if a skill named `foo` exists with `user-invocable: true` | `/skill-name` of the converted skill |

Unrecognized tool names: do **not** invent an equivalent. Replace with the
closest honest instruction and add a `[porter note]` line at that spot
explaining the original intent, so the user can review.

## Understanding the source package (do this before rewriting)

1. **Identify the platform.** Claude Code packages: `SKILL.md` + optional
   `commands/*.md` (slash commands with their own frontmatter), `agents/*.md`
   (persona files with `name`, `description`, `tools:` frontmatter),
   `.claude-plugin/plugin.json`. Codex packages: `SKILL.md` + optional
   `agents/openai.yaml` (Codex metadata — Vibe Code actually reads this natively;
   preserve it when targeting the CLI).
2. **Read the whole skill** — SKILL.md and every supporting file. State to
   yourself: what task is this skill for, what workflow does it encode, what
   artifacts does it produce?
3. **Classify each supporting item**:
   - `references/*.md` — knowledge → copy near-verbatim (after tool rewrite).
   - `assets/*` — templates/samples → copy unchanged.
   - `scripts/*.py|sh` — **decide per script**: deterministic transformation?
     For Vibe Code CLI: keep it, add a runtime note in SKILL.md ("run with
     `bash`: `python3 scripts/foo.py` from the skill directory"). For Vibe
     Work: if short and pure, inline its logic as numbered instructions or a
     worked example; if complex, keep the script as an attached file with
     `isExecutable: true` in the Skills API and an instruction to run it via
     Code Interpreter; if it needs the local filesystem, mark it as
     "CLI-only capability" and say so in the report.
   - `commands/*.md` — each becomes, for Vibe Code, its own mini-skill
     (`<skill>-<command>/SKILL.md` with `user-invocable: true`); for Vibe
     Work, fold into the body as a "Workflows" section keyed by intent.
   - `agents/*.md` — Claude personas. For Vibe Code CLI, convert to
     `.vibe/agents/<name>.toml` (`agent_type = "agent"`, `display_name`,
     `description`, `enabled_tools`). For Work, inline the persona's voice
     into the SKILL.md body ("Adopt this persona: …").
4. **Sanity-check triggers.** After conversion, the description must still fire
   on the same user intents as the original. If the original description listed
   trigger phrases, keep the strongest ones within the 1024-char budget.

## Output contract per target

- **For the Work target, also manage the file-count limit**: Work caps the number of attached files. When the package has many (a rule of thumb: more than ~10), merge related files — e.g. collapse 8 `references/*.md` into 2-3 focused ones, fold small page templates into one `templates.md`. After merging, sweep **every file that references another file** (body → references, references → references, references → assets) and repoint those paths to the merged names — cross-file pointers that still name the old paths are as broken as dropped files. Never silently drop a referenced file.

### Vibe Work (online chat) — deliverable
```
<skill-name>/
├── SKILL.md          ← cleaned body + frontmatter as a single file the user pastes
├── references/…      ← attached one by one in the "New Skill" files section
└── assets/…          ← templates, samples
```
Plus a short import note in your answer: "Title: <human title> · Description:
<one-liner> · attach every file under references/ and assets/". Vibe Work has a
file-count limit — if the package has many files, merge related references into
fewer, focused files and use progressive disclosure.

### Vibe Code CLI — deliverable
```
~/.vibe/skills/<name>/SKILL.md        (flat, name matches folder)
~/.vibe/skills/<name>/scripts/…       (kept, with runtime note)
~/.vibe/skills/<name>/references/…
~/.vibe/skills/<name>/assets/…
~/.vibe/skills/<name>-<command>/SKILL.md   (one per Claude command)
```
Add `user-invocable: true` when the skill should be callable as `/<name>`.
Validate: `name` regex `^[a-z0-9]+(-[a-z0-9]+)*$`, description ≤1024 chars.

### Mistral Skills API — deliverable
JSON for `POST /v2/skills`:
```json
{
  "name": "kebab-case-name",
  "definition": {
    "description": "Use when … (trigger)",
    "body": "Full SKILL.md body text (no frontmatter)",
    "assets": {
      "references/policy.md": {"textContent": "…", "isExecutable": false},
      "scripts/extract.py": {"rawContent": "<base64>", "isExecutable": true}
    }
  },
  "notes": "Ported from <source platform>, original skill: <name>",
  "sharingScope": "private"
}
```
`sharingScope`: `"private"` or `"workspace"`. Version bumps via
`POST /v2/skills/{id}/versions`. Keep `assets` file-count low.

## Workflow (follow in order)

0. **Capability mapping** — before converting, run the rule-zero mapping:
   for every mechanism the package uses (hooks, agents, MCP, permissions),
   find its Mistral expression per the capability map, or a different route
   to the same intent. Then report the estimated surviving usefulness and
   what you mapped to what — before you start rewriting, so the user knows
   what the port will and will not include. Never auto-reject on buzzwords;
   never force-port around a genuinely unexpressible core.
1. **Ingest** — read every file the user provides (pasted text, uploaded
   folder, or a repo path). If pieces are missing (e.g. SKILL.md references
   `references/foo.md` that was not supplied), list them and ask.
2. **Understand** — summarize in 2–3 sentences what the skill does and when
   it triggers; if you cannot, ask the user before converting.
3. **Choose target** — infer from context; if the user mentions chat /
   chat.mistral.ai / "online", it's Vibe Work; terminal / CLI / `~/.vibe`,
   it's Vibe Code; API / Studio / console, it's Skills API. Ask only when
   genuinely ambiguous.
4. **Rewrite** — frontmatter per the rules, tool calls per the table,
   commands/agents per the classification, scripts per the decision tree.
   Preserve the skill's voice, structure, and domain content — convert the
   *execution layer*, never the *expertise*.
5. **Self-review** — re-read your output as if you were the Mistral model that
   just had it activated: would every instruction be executable here? Any
   dangling tool names? Any file referenced but not included? Fix, then
   re-check the name/description constraints.
6. **Deliver** — the converted package plus a **port report**: what was
   changed (frontmatter, tool calls, commands→skills, agents→TOML, scripts
   inlined/kept/dropped, env-var/state rewrites), what could not be ported
   and why, the estimated surviving usefulness (content and environment),
   and the exact import steps for the chosen target. When the source
   carried provenance notes (e.g. `.claude-plugin/authoring-notes.json`),
   preserve the traceability in the frontmatter `metadata:` block (e.g.
   `ported_from: claude-code/pulse`, `source_spec: …`) so the skill keeps
   its history instead of losing it with the dropped plugin folder.

## Anti-patterns

- Blind-copying the folder and hoping — the skill loads but "misbehaves"
  precisely because tool names and commands don't exist on Mistral.
- Auto-rejecting because the package mentions hooks or multi-agent flows —
  Mistral has hooks (`.vibe/hooks.toml`), subagents, and MCP; map first.
- Force-porting around a genuinely dead centerpiece without telling the
  user — the mirror failure of auto-rejection.
- Rewriting the description into something shorter and vaguer — you destroy
  the skill's activation.
- Dropping `references/` to "save space" — progressive disclosure loads them
  on demand; they cost nothing until used.
- Silently dropping a script because no runtime exists — report it instead.
- Inventing Mistral tool names that don't exist (the valid Vibe Code tool set
  is: bash, read_file, write_file, search_replace, edit, grep, web_search,
  web_fetch, task, todo, ask_user_question, skill).

## Cross-references

- Agent Skills spec: <https://agentskills.io/specification> (name/description
  constraints, progressive disclosure)
- Vibe Code skills: <https://docs.mistral.ai/vibe/code/cli/skills>
- Vibe Work skills: <https://docs.mistral.ai/vibe/work/skills>
- Skills API: <https://docs.mistral.ai/api/endpoint/beta/skills>
