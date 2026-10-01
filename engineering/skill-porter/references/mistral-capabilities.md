# Mistral Capabilities — verified platform facts

Verified against the Mistral Vibe source code (`mistralai/mistral-vibe`:
`vibe/core/skills/*`, `vibe/core/tools/*`) and the official docs source
(`mistralai/platform-docs-public`). These are the real capabilities of each
target — never assume less, never invent more.

## Vibe Work (chat.mistral.ai, Work tab)

Online chat environment. Skills live in `Context > Skills` (sections:
Built-in / Personal / Workspace; toggle per skill; workspace admins can
force-enable; Personal = private, Workspace = shared).

Execution environment — all of this exists:

- **Files**: upload via `+` or drag-and-drop (PDF, DOCX, PPTX, CSV, XLSX,
  JSON, XML, YAML, MD, code files, images, email). Uploaded files become
  task context and are available to the Code Interpreter for the current
  conversation.
- **Canvas**: built-in editor where Work produces and iterates on text,
  data, code, and presentations. Multiple Canvases per chat (tabs),
  version control with restore, manual editing, AI-assisted inline edits.
  Opens automatically when useful; trigger manually with `/canvas` or
  "open in Canvas". Typical: reports, data tables, scripts, slide decks.
- **Code Interpreter**: native sandbox running **Python and TypeScript**
  (pandas, numpy, matplotlib preinstalled; chart libs for TS). Runs code
  described in plain language; returns tables, figures, or downloadable
  files. **No internet access inside the sandbox; cannot reach the user's
  system.** Uploaded files available per conversation. Paid plans only,
  rate-limited by plan.
- **Web search**: available; use it before fetching when data is online
  (the interpreter cannot fetch URLs — download and upload instead).
- **Workflows**: internal automations built by developers in Mistral
  Studio, published as chat-compatible assistants; surface in Work's `+`
  tool menu and are called like tools during reasoning. (If a source skill
  wraps an internal pipeline, the Work-side equivalent may be a published
  Workflow — note this in the port report as a developer task.)
- **skill-creator**: built-in Mistral skill that creates, updates, deletes
  Skills from inside Work. A converted skill's instructions can tell the
  user to invoke it, and Work itself can scaffold skill folders.
- **Mini apps, spreadsheets, scheduled tasks, connectors (incl. MCP
  connectors), voice mode, image generation** also exist as Work features.

Skill mechanics: progressive disclosure — (1) discovery loads only
name+description (~100 tokens each); (2) activation loads the full
SKILL.md body when the task matches the description; (3) attached files
load on demand. Invocation: automatic on description match, explicit
`/{skill-name}`, or natural mention. **The description is the activation
trigger — write it as "Use when…".** Supporting files are subject to a
file-count limit.

Built-in Work skills (style reference for trigger-writing):
`challenge-my-thinking`, `data-analysis`, `deep-research`,
`doc-coauthoring`, `document-review`, `internal-comms`, `meeting-prep`,
`research-synthesis`, `skill-creator`, `stakeholder-translator`,
`structured-extraction`, `vibe-work-onboarding`.

## Vibe Code CLI

Terminal coding agent. Skills discovered from: `config.toml`
`skill_paths = [...]` (custom), `./.vibe/skills/` or `./.agents/skills/`
(project, trusted workdir), `~/.vibe/skills/` (user). Discovery is **flat**:
only direct child directories of a skill path, each with a `SKILL.md`.

Tool registry (real tool names, snake_case):
`bash`, `edit`, `exit_plan_mode`, `git_bash`, `grep`, `read_file`,
`search_replace`, `skill`, `task`, `todo`, `web_fetch`, `web_search`,
`ask_user_question`, `write_file` — plus MCP and connector tools when
configured. Anything else named in a Claude skill does not exist here.

Hooks (`.vibe/hooks.toml`, project and `~/.vibe/`):
- `pre_tool` — before the permission prompt; can deny or **fully rewrite
  tool arguments** (`hook_specific_output.tool_input`)
- `post_tool` — after the tool ran; can replace/append output text
  (`additional_context`), audit
- `post_agent` — after each assistant turn; deny + reason → retry (max 3)
Contract: JSON invocation on stdin (`session_id`, `cwd`,
`hook_event_name`, tool fields), exit 0 + JSON on stdout to act.
Subagents inherit hook config.

Agents (`.vibe/agents/<name>.toml`): `agent_type = "agent"` (user-facing)
or `"subagent"` (delegation-only via the `task` tool, text-only results,
no user questions). Fields: `display_name`, `description`, `safety`,
`active_model`, `system_prompt_id` (file in `~/.vibe/prompts/`),
`enabled_tools`, `disabled_tools`, per-tool `[tools.<name>] permission`
(`always` | `ask` | `never`).

Also: MCP (`.vibe/mcp.json`), AGENTS.md project/user instructions (up to
two loaded), slash-command invocation of skills (`/{name}` when
`user-invocable: true`; trailing text becomes extra instructions), built-in
subagent `explore`.

## Mistral Skills API (beta) — console.mistral.ai / Studio

Studio `Build > Skills` is the GUI for the same object; `Publish to Vibe`
makes a Studio skill available in Vibe Work. Skills are versioned
(`POST /v2/skills/{id}/versions`; older versions rollback-able).

Endpoints: `GET /v2/skills`, `POST /v2/skills`,
`POST /v2/skills/{id}/versions`.

`POST /v2/skills` request:

```json
{
  "name": "kebab-case-name",
  "definition": {
    "description": "Use when … (activation trigger)",
    "body": "Full instruction text (SKILL.md body, no frontmatter)",
    "assets": {
      "references/policy.md": {"textContent": "…", "isExecutable": false},
      "scripts/extract.py": {"rawContent": "<base64>", "isExecutable": true}
    }
  },
  "notes": "Ported from <platform>/<skill>, original: <name>",
  "sharingScope": "private",
  "aliases": ["production"]
}
```

- `assets`: filename → `{textContent | rawContent, isExecutable}`;
  `isExecutable: true` marks runnable assets
- `sharingScope`: `"private"` | `"workspace"`
- `aliases`: version pins (e.g. `production`)
- A SKILL.md parse failure is silently dropped by the CLI — always
  validate output before delivering (use `scripts/validate_skill.py`)
