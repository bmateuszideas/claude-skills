---
name: skill-porter
description: "Converts ONE complete skill package — a single skill\u2019s full folder (SKILL.md plus all of its dependencies: scripts/, references/, assets/, commands/, agents/, plugin manifest) — from Claude Code or OpenAI Codex into a fully working Mistral format: Vibe Work (chat.mistral.ai Context > Skills), Vibe Code CLI (~/.vibe/skills/), or the Mistral Skills API (POST /v2/skills). Use when the user pastes or uploads ONE skill folder from Anthropic/Claude/Codex and wants that exact skill working in Mistral, when a raw Claude skill loaded into Mistral misbehaves (unknown tools, dead scripts, ignored commands), or when the user asks to port/migrate/translate a single agent skill between platforms. Reads the whole source folder, understands what the skill is for, maps every mechanism to its verified Mistral equivalent, and emits a Mistral-native package — never a blind file copy, never a batch converter."
license: MIT
metadata:
  version: "1.0.0"
  category: engineering
---

# Skill Porter — Claude/Codex → Mistral Vibe

You are converting **one skill package at a time** — a single skill\u2019s
full folder (SKILL.md plus every dependency it ships) that gives an AI
agent domain expertise — from its native platform into a Mistral target.
If the user provides multiple skills, port them one at a time, each as its
own full-folder conversion. This is
intelligence work: understand **what the skill is for**, then re-express it
so a Mistral model executes it correctly.

## Runtime capability references (READ THESE — do not guess platforms)

You have no live access to platform documentation. Everything you must know
about the three Mistral targets and the two source platforms is attached to
this skill. Load the right file when the task touches that area:

| When you need… | Read |
|---|---|
| What Vibe Work / Code CLI / Skills API can actually do (verified capabilities, tool names, execution environments, file/Canvas/Code-Interpreter mechanics, workflows, built-in skills) | [references/mistral-capabilities.md](references/mistral-capabilities.md) |
| The exact SKILL.md format rules and validation constraints per target (name regex, description limit, frontmatter fields, discovery, invocation) | [references/format-contract.md](references/format-contract.md) |
| How to translate Claude/Codex mechanisms (tools, hooks, subagents, commands, slash-command syntax, env vars, script kinds) to their Mistral expression — the full decision tables with worked patterns | [references/mapping-tables.md](references/mapping-tables.md) |
| The anatomy of the input package you were handed (what each folder/file type means on Claude Code vs OpenAI Codex, incl. the Codex `agents/openai.yaml` bridge) | [references/source-anatomy.md](references/source-anatomy.md) |

Load them before you assess or rewrite anything. If a fact is not in these
files and is not verifiable from the package itself, ask the user instead of
assuming.

## Workflow (follow in order)

0. **Capability mapping** — for every mechanism the source package uses
   (tools, hooks, subagents, commands, MCP, env vars, scripts), find its
   Mistral expression using `mapping-tables.md` — same *intent* by whatever
   route the target supports. Score the surviving usefulness on two axes:
   **content** (domain knowledge — usually ~100%) and **operating
   environment** (where the skill's logic actually runs). Report both
   percentages and the what-mapped-to-what list **before** rewriting, so the
   user knows what the port will include. Never auto-reject because the
   package mentions hooks or multi-agent flows — Mistral has hooks
   (CLI), subagents, and code execution on all targets; map first. Never
   force-port around a genuinely unexpressible core without saying so.
1. **Ingest** — read every file the user provides. If SKILL.md references a
   file that was not supplied, list the gaps and ask.
2. **Understand** — summarize in 2–3 sentences what the skill does and when
   it triggers; if you cannot, ask before converting.
3. **Choose target** — infer from context (chat / chat.mistral.ai /
   "online" → Work; terminal / CLI / `~/.vibe` → Code CLI; API / Studio /
   console → Skills API). Ask only when genuinely ambiguous. Ask about the
   user's plan tier when scripts are involved on Work (Code Interpreter is
   paid-plan, rate-limited — write the body to degrade gracefully).
4. **Rewrite** — frontmatter per `format-contract.md`, mechanisms per
   `mapping-tables.md`, commands/agents per the classification there.
   Preserve the skill's voice, structure, and domain content — convert the
   *execution layer*, never the *expertise*.
5. **Self-review** — re-read your output as the Mistral model that just had
   it activated: is every instruction executable on this target? Any
   dangling tool names, dead file references, stale command tables, or
   leftover `${VAR}`s? Fix, then re-check the format constraints.
6. **Deliver** — the converted package plus a **port report**: what changed
   (frontmatter, tool calls, commands→skills, agents, scripts, env/state
   rewrites), what could not be ported and why, surviving usefulness on both
   axes, exact import steps for the target, and provenance preserved in
   frontmatter `metadata:` (e.g. `ported_from: claude-code/<name>`).

## Per-target deliverables (details in format-contract.md)

- **Vibe Work**: folder with rewritten SKILL.md + supporting files to paste
  into `Context > Skills > New Skill` (Title / Description / body /
  attachments). Manage the attachment file-count limit by merging related
  files and repointing **all** cross-file references (body→references,
  references→references, references→assets).
- **Vibe Code CLI**: flat folder(s) — `~/.vibe/skills/<name>/SKILL.md`
  with `name` matching the directory, `scripts/`, `references/`, `assets/`
  preserved; one extra `user-invocable: true` mini-skill per source slash
  command; `.vibe/agents/<name>.toml` per source agent.
- **Skills API**: JSON for `POST /v2/skills` — `name`,
  `definition.description` (trigger), `definition.body` (instruction text),
  `definition.assets` (files as `textContent`/`rawContent` + `isExecutable`),
  `sharingScope`, `notes` with provenance.

## Anti-patterns

- Blind-copying the folder and hoping — the skill loads but "misbehaves"
  because tool names and commands don't exist on the target.
- Auto-rejecting on Claude/Codex buzzwords — map the intent first.
- Force-porting around a dead centerpiece without telling the user.
- Assuming a Mistral target lacks a capability without checking the
  references — all three targets run code; two have hooks; all have
  multi-step agent flows.
- Rewriting the description into something shorter and vaguer — you destroy
  the skill's activation trigger.
- Dropping `references/` to "save space" — progressive disclosure loads
  them on demand; they cost nothing until used.
- One giant SKILL.md — a skill is a *package*: lean core in SKILL.md,
  tables and evidence in `references/`, loaded when needed.
