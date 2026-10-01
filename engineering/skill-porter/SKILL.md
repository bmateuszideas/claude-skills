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

## Rule zero: do not force-port — assess feasibility first

Mistral is not a replica of Anthropic's platform. Some Claude skills depend on
infrastructure that does not exist on Mistral, and a forced port produces a
package that *looks* converted but silently fails. Before rewriting anything,
run a **feasibility assessment** and report it honestly.

### Hard blockers (skill cannot be ported to the chosen target)

- **Claude Code hooks** (`PreToolUse`, `PostToolUse`, `hooks/*.json`) — Vibe
  Work and the Skills API have no hook mechanism; only Vibe Code has limited
  hook config. A skill whose core value is a hook is unportable to Work/API.
- **Multi-agent orchestration beyond one hop** — Claude `Task` subagents that
  spawn further subagents with tool permissions per agent. Mistral subagents
  exist (`.vibe/agents/*.toml`, `task` tool) but are text-only, single-hop,
  and simpler. If the skill's essence is deep agent trees with per-agent tool
  allow-lists and inter-agent messaging, that architecture does not survive.
- **Claude plugin/platform APIs** — `.claude-plugin/` manifests, marketplace
  mechanics, `plugin.json` commands/hooks registries. No equivalent exists.
- **MCP servers bundled with the skill** — Vibe Code supports MCP config
  (`.vibe/mcp.json`), Vibe Work uses Connectors instead; a skill that *ships*
  an MCP server must have that server deployed somewhere reachable, which is
  out of scope for a skill port. Report it as infrastructure, not skill logic.
- **Filesystem-heavy workflows for the Work target** — scripts that iterate
  over local directories, watch files, or shell out to local tools. Work has
  no filesystem; inlining cannot rescue a workflow whose every step needs a
  local disk.
- **Model-specific behavior** — skills tuned to Claude model quirks (e.g.
  `model: opus` persona calibration, Claude-specific token/limit assumptions).
  Behavior may transfer imperfectly; say so.

### Partial portability (port what survives, report the rest)

A skill is usually a mix: domain knowledge (portable), workflow shape
  (usually portable), execution plumbing (sometimes not). In that case:

1. Port the portable majority.
2. For each unportable element, state: **what it did on the source platform,
   why it cannot run on the target, what the converted skill does instead**
   (degraded mode, manual step, or omission).
3. Never silently substitute a made-up "equivalent". A `[porter note]`
   explaining the gap is worth more than a fake bridge.

### Refusal protocol

If, after assessment, the skill's core value is unportable, **say so plainly**:
"This skill cannot be meaningfully ported to <target> because <reason>. The
parts that survive are <list>; here is what that reduced skill looks like —
want it?" Do not deliver a full-looking package whose centerpiece is dead.
The user explicitly prefers an honest "no" over a conversion that pretends.

## The three Mistral targets (pick from user intent, ask only if unclear)

| Target | Where it runs | What you deliver |
|---|---|---|
| **Vibe Work** (chat.mistral.ai, Work tab) | Online chat. Skills live in `Context > Skills`. No filesystem tools. | A folder: rewritten `SKILL.md` + supporting files, ready to paste into the New Skill form (Title / Description / SKILL.md body / attached files). Progressive disclosure: description decides auto-activation; body loads on activation; attached files load on demand. |
| **Vibe Code CLI** | Terminal coding agent. Skills live at `~/.vibe/skills/<name>/` (user) or `./.vibe/skills/` (project). Full filesystem access via tools. | A folder with converted `SKILL.md` (flat layout — one directory per skill directly under `skills/`, no nesting), preserving `scripts/`, `references/`, `assets/`. |
| **Mistral Skills API** (console.mistral.ai, Studio) | Cloud, versioned, shareable. | A JSON body for `POST /v2/skills` (see schema below), or — simpler — a skill created in Studio `Build > Skills` then `Publish to Vibe`. |

## Non-negotiable format rules (hard Mistral validation)

1. **`name`**: 1–64 chars, only `a-z`, `0-9`, hyphens. No uppercase, no leading/trailing hyphen, no double hyphens. Must match the parent folder name. If the source name violates this (e.g. `MySkill`, `pdf--tools`), rewrite it and tell the user.
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

0. **Feasibility gate** — before any conversion, run the rule-zero
   assessment: scan the package for hard blockers (hooks, deep multi-agent
   orchestration, plugin APIs, bundled MCP servers, filesystem-bound flows,
   model-specific tuning) against the chosen target. Report one of:
   **portable** / **partially portable** (list what survives and what does
   not, with reasons) / **not portable** (explain the blocker and what a
   reduced version would look like). Only proceed to rewriting when the
   user knows what will and will not survive. Do not start converting
   something whose core is unportable without saying so first.
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
   inlined/kept/dropped), what could not be ported and why, and the exact
   import steps for the chosen target.

## Anti-patterns

- Blind-copying the folder and hoping — the skill loads but "misbehaves"
  precisely because tool names and commands don't exist on Mistral.
- Force-porting: converting around a hard blocker and shipping a package
  whose central mechanism (hook, agent tree, MCP dependency) is dead on the
  target. An honest "not portable" or a reduced port is the correct output.
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
