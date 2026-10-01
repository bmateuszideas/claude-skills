# Source Anatomy — what a Claude Code or OpenAI Codex package looks like

Identify the source platform before converting; the two package differently.

## Claude Code package

```
<skill>/
├── SKILL.md                 # frontmatter: name, description (+ optional
│                            #   metadata: version, author, tags, source_spec)
│                            # body: instructions, may reference commands,
│                            #   agents, scripts, references by relative path
├── .claude-plugin/
│   ├── plugin.json          # plugin manifest: name, description, version,
│   │                        #   author {name,url}, homepage, repository,
│   │                        #   license, skills: ["./skills/<x>"]
│   └── authoring-notes.json # provenance (build pattern, source spec)
├── commands/*.md            # slash commands: own frontmatter
│                            #   (name, description) + body; invoked /name;
│                            #   may be namespaced (/cs:pulse)
├── agents/*.md              # personas: frontmatter name, description,
│                            #   skills, domain, model (e.g. opus),
│                            #   tools: [Read, Write, Edit, Bash, Grep, Glob,
│                            #   WebFetch, WebSearch], context: fork
├── scripts/                 # usually stdlib-only Python CLIs (--help, --json)
├── references/              # on-demand knowledge
└── assets/                  # templates, sample data, expected outputs
```

Claude Code tool names you will find in bodies: `Read`, `Write`, `Edit`,
`MultiEdit`, `Bash`, `Grep`, `Glob`, `WebSearch`, `WebFetch`, `Task`,
`TodoWrite`, `AskUserQuestion`. Hook events: `PreToolUse`, `PostToolUse`,
`SessionStart`, `Stop`, `UserPromptSubmit`, `Notification`, `PreCompact`.

## OpenAI Codex package

Same Agent Skills core (SKILL.md + scripts/references/assets) plus:

```
<skill>/
├── SKILL.md
└── agents/
    └── openai.yaml          # Codex metadata:
                             #   policy:
                             #     allow_implicit_invocation: bool
                             #     products: [codex-cli]
```

Notes:
- Codex has no per-command markdown convention like Claude's `commands/` —
  behavior lives in the skill body.
- No `.claude-plugin/` equivalent.
- **Vibe Code CLI reads `agents/openai.yaml` natively** (`policy` with
  `allow_implicit_invocation` and `products`; unknown policy keys are
  treated as invalid so a typo cannot silently widen access):
  preserve the file when targeting the CLI; drop it for Work/API.
- Bodies may still casually reference Claude-style tool names — always run
  the tool-name sweep regardless of platform.


## Real examples (verbatim from actual Claude packages)

**`commands/*.md` frontmatter** — note `argument-hint` and `$ARGUMENTS` (no `name` field; the filename is the command name):

```yaml
---
description: Top-level product-team router. Classifies a product inquiry across 16 lanes (prioritization, OKRs, UX, ...) with a deterministic script and forks context to the right sub-skill via the product-skills orchestrator, returning a ≤200-word digest with one grill challenge.
argument-hint: "<product inquiry: prioritize features, plan an experiment, discovery health, etc.>"
---
```
Body invokes with `$ARGUMENTS` and may run `python3 <package>/scripts/<router>.py --text "$ARGUMENTS" --output json` (path shape, not a real file).

**`agents/*.md` frontmatter** — note `tools:` (Claude names), `model:` pin, no `context: fork` here means shared session (when present it means a fresh isolated session):

```yaml
---
name: cs-product-orchestrator
description: Outcome-first product lead. Routes product inquiries (...) to the right sub-skill via the product-skills orchestrator, and drives the continuous-discovery loop with machine gates (cadence tracker + OST linter). Forks context to keep heavy intake out of the parent thread.
tools: Read, Write, Edit, Glob, Grep, Bash, Skill
model: sonnet
---
```
The body below the frontmatter is the persona system prompt.

**`.claude-plugin/plugin.json`** (verbatim):

```json
{
  "name": "agile-product-owner",
  "description": "Agile product ownership ...",
  "version": "2.9.0",
  "author": {"name": "Alireza Rezvani", "url": "https://alirezarezvani.com"},
  "homepage": "https://github.com/alirezarezvani/claude-skills/tree/main/product-team/agile-product-owner",
  "repository": "https://github.com/alirezarezvani/claude-skills",
  "license": "MIT",
  "skills": ["./skills"]
}
```

**A package with hooks** (`engineering/human-gate` in this repo): the SKILL.md body references hook config JSON (e.g. a `Stop` event hook that halts the turn for human approval). Detect hook-event names in body text and in any `.json`/`.toml` hook config files shipped in the folder.

## Reading order when ingesting

1. SKILL.md (frontmatter + body) — the contract.
2. Every supporting file the body references — check each exists.
3. commands/ and agents/ (Claude) or agents/openai.yaml (Codex).
4. Scripts: read enough of each to classify it per the mapping tables
   (formula-maskable / text-analysis / stateful / filesystem-bound /
   sample-generator).
5. `.claude-plugin/` for provenance only (→ preserve in `metadata:`).
6. List anything the body references that was not supplied; ask the user.
