# Mapping Tables — Claude/Codex mechanism → Mistral expression

For every mechanism the source package uses: name its **intent** (the
user-visible job), find the target's expression of that intent, then decide
per target. Same result by a different route is a success; a fake bridge is
a failure.

## Tool-call translation (find every reference in SKILL.md, references/, commands/)

| Claude Code | Vibe Code CLI | Vibe Work | Skills API (body text) |
|---|---|---|---|
| `Read` | `read_file` | "read the attached file" / Files as context | "the user provides the file" |
| `Write` | `write_file` | produce in Canvas / downloadable via Code Interpreter | "produce the document" |
| `Edit`, `MultiEdit` | `search_replace`, `edit` | regenerate the corrected full content in Canvas | same |
| `Bash`, `Shell` | `bash` | Code Interpreter (port the command as a Python/TS snippet; conversation files accessible; no internet in sandbox) | "computed step" phrasing |
| `Grep` / `Glob` | `grep` / `bash` ls | search within pasted/attached material | instruct search over provided content |
| `WebSearch` | `web_search` | Work web search / `deep-research` pattern | "search the web" instruction |
| `WebFetch` | `web_fetch` | web search results, or user pastes content (interpreter cannot fetch URLs) | same |
| `Task` (subagent) | `task` + `.vibe/agents/*.toml` | inline the subagent's instructions as a body section (persona + steps) | same |
| `TodoWrite` | `todo` | describe the plan in the response | same |
| `AskUserQuestion` | `ask_user_question` | ask directly in chat | same |
| Unrecognized tool | DO NOT invent a name | honest fallback + `[porter note]` at that spot | same |

## Mechanism map (hooks, agents, commands, plugins, MCP, models)

| Source mechanism | Mistral expression |
|---|---|
| `PreToolUse` / `PostToolUse` hooks | CLI: `hooks.toml` `pre_tool` (deny or full argument rewrite) / `post_tool` (replace or append output, audit). Work/API: no hook events — fold the hook's policy into the body as explicit rules the model enforces itself; say so. |
| Lifecycle hooks (SessionStart, Stop, UserPromptSubmit, PreCompact, Notification) | CLI: `post_agent` covers the after-turn case. Others: re-express as body instructions ("at session start, first do X") or a manual step; note there is no event twin. |
| Subagent trees (multi-hop, per-agent tool lists, inter-agent messaging) | CLI: `.vibe/agents/<name>.toml` (`agent_type = "subagent"`, `enabled_tools`, `disabled_tools`, `[tools.x] permission`, `system_prompt_id` → `~/.vibe/prompts/`), spawned via `task`, text-only single-hop. Shallow trees map directly; deep trees flatten to sequential `task` calls or inline personas. Work/API: inline as body sections. |
| `context: fork` on an agent | Vibe subagents already run as fresh isolated sessions — drop the field; verify the agent prompt is self-contained (no parent-session state). |
| Bundled MCP servers | CLI: `.vibe/mcp.json`. Work: MCP connectors. The server is infrastructure — port the skill's *consumption* of its tools; tell the user the server must be deployed/configured separately. |
| `.claude-plugin/` (plugin.json, marketplace, authoring-notes) | No equivalent. Drop the manifest; preserve provenance in frontmatter `metadata:` (`ported_from`, `source_spec`). |
| Per-tool permission policies | CLI: agent TOML `[tools.<name>] permission` (`always`/`ask`/`never`) and skill `allowed-tools`. |
| `model:` (persona pinned to a Claude model) | Drop the pin; note calibration may shift; watch in self-review. |
| Slash commands `commands/*.md` | CLI: one mini-skill per command (`<skill>-<command>/SKILL.md`, `user-invocable: true`). Work: fold into the body as "Workflows" sections keyed by intent. API: fold into `body`. |
| Platform branding in body ("Claude Code", "this plugin") + asset names (`CLAUDE.md.template`) | Rewrite to target/neutral ("Vibe", "this skill", "your agent"). Vibe reads AGENTS.md, not CLAUDE.md: rename/re-point such templates and update every reference. |
| Cross-reference tables listing source-platform commands | After conversion, rewrite the table to the NEW invocation map on the target — a stale table pointing at Claude commands is a silent failure. |
| Shell/env vars in paths (`${RESEARCH_DIR}`, `$(date +%Y-%m-%d)`, `~/...`) | CLI: keep (bash). Work/API: replace every one — deliverables to Canvas/chat/downloadable files, state to conversation; never leave a `${VAR}` in a Work body. |
| Namespaced names (`cs:pulse`) | Sanitize: colons are illegal in the name regex → `cs-pulse`. |

## Script decision tree (per script file)

1. **Formula-maskable** (long script, core is one deterministic formula —
   e.g. a RICE calculator): CLI keep; Work prefer Code Interpreter (attach
   and run against uploaded input), fallback = formula written as an
   instruction + worked example from the skill's sample data; API inline.
2. **Text-analysis** (heuristic transcript/notes parsing): CLI keep; Work
   model-native analysis instruction is usually *better* — give input
   format → what to extract → output structure; optionally attach the
   script for reproducible interpreter runs; API instruction inline.
3. **Stateful** (value = persisting state across steps — counters, session
   logs, dedup caches): CLI keep; Work/API port the tally as a body
   "running state" pattern the model maintains (e.g. a sent/received/cited
   table updated per phase) or persist via Canvas versioning. Do not
   pretend the script runs against the user's disk.
4. **Filesystem/system-bound** (walks the user's disk, spawns processes,
   needs their machine): CLI keep + runtime note; Work/API mark as
   "CLI-only capability" in the report and degrade that path honestly.
5. **Sample-generator subcommands** (`x.py sample`): CLI keep; Work point
   at the skill's existing example-data asset instead.

Script-flag examples in the body (`--capacity 15 --output json > out.json`):
CLI keep; Work/API rewrite — flags → instruction parameters, redirects →
"produce the table/JSON in your answer", interpreter produces downloadable
exports when the user needs files.

## Scoring (report before rewriting)

Two axes, honest percentages:
- **Content**: how much of the domain knowledge/workflow survives (usually high).
- **Operating environment**: where the logic runs — CLI ≈ 1:1; Work maps
  filesystem/shell to Canvas/Interpreter/conversation state; API is
  instruction-only.

Deliver the honest maximum: port what survives, name what does not and why,
never a fake bridge, never an auto-rejection, never a forced port around a
dead centerpiece.
