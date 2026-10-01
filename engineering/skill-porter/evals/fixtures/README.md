# Eval fixtures — synthetic source packages

The four eval cases in `evals.json` reference synthetic source packages you
reconstruct before running the eval. Each is small and takes ~2 minutes to
assemble; the filenames and frontmatter below are the contract — the body
content can be any realistic placeholder, but the **mechanism mix must match**
(hook count, subagent count, tool names) because the evals assert on how the
model handles those mechanisms.

## Fixture 1 — `changelog-writer` (Claude Code, clean port)

```
changelog-writer/
├── SKILL.md          # frontmatter: name: changelog-writer; description with
│                     #   trigger phrases; body instructs to "use Read to load
│                     #   references/style-guide.md" and "run
│                     #   scripts/changelog_gen.py via Bash"
├── scripts/
│   └── changelog_gen.py   # reads a unified diff on stdin, prints markdown
├── references/
│   └── style-guide.md     # ~600 lines of writing rules
└── commands/
    └── changelog-full.md  # frontmatter name: changelog-full, description,
                          #   body: full-release workflow invoking the skill
```

## Fixture 2 — `security-gate` (Claude Code, hooks + subagents — the anti-auto-reject case)

```
security-gate/
├── SKILL.md               # body: "installs PreToolUse hook
│                          #   (hooks/security-guard.json) blocking rm -rf on
│                          #   project dirs and curl|sh; SessionStart injects
│                          #   the checklist below; /security-audit fans out
│                          #   to two Task subagents (attacker persona,
│                          #   defender persona) and synthesizes findings"
├── hooks/
│   └── security-guard.json
├── scripts/
│   └── audit.py           # walks local directories (os.walk) — CLI-only
├── references/
│   └── threat-models.md
└── commands/
    └── security-audit.md
```

## Fixture 3 — `plugin-shell` (Claude Code, unportable core)

```
plugin-shell/
├── SKILL.md                   # ~10 lines: "install the plugin to get
│                              #   marketplace skills; real logic lives in
│                              #   the plugin runtime"
└── .claude-plugin/
    └── plugin.json            # registers 15 commands, 4 hooks, 2 MCP
                               #   servers that must run inside Claude Code
```

## Fixture 4 — `repo-summarizer` (OpenAI Codex, bridge case)

```
repo-summarizer/
├── SKILL.md              # frontmatter: name: repo-summarizer, clean
│                         #   description; body may casually reference
│                         #   Read/Grep — assert the model still checks
├── agents/
│   └── openai.yaml       # policy:
│                         #     allow_implicit_invocation: false
│                         #     products: [codex-cli]
├── references/
│   └── structure.md
└── scripts/
    └── summarize.py
```

## Scoring

For each case, mark every `expected_behavior` assertion as PASS / PARTIAL /
FAIL with a one-line evidence quote from the model's output. A case passes
when no assertion is FAIL. The suite passes when all four cases pass **on the
live target model** — static parsing of the output SKILL.md is only the first
assertion, never the whole test.
