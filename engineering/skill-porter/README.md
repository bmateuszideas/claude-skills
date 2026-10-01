# skill-porter — Claude/Codex → Mistral skill conversion package

Full Agent Skills package (v1.0) that converts complete skill packages from
Claude Code / OpenAI Codex into working Mistral targets: Vibe Work,
Vibe Code CLI, and the Mistral Skills API.

## Layout (per agentskills.io)

```
skill-porter/
├── SKILL.md                     # Lean core (~90 lines): workflow, decisions, routing
├── references/                  # On-demand knowledge (progressive disclosure)
│   ├── mistral-capabilities.md  # Verified facts: Work (Files/Canvas/Code Interpreter/
│   │                            #   Workflows/skill-creator), CLI (tools/hooks/agents),
│   │                            #   Skills API schema — extracted from mistral-vibe
│   │                            #   source + platform-docs-public
│   ├── format-contract.md       # Machine-checkable format rules per target
│   ├── mapping-tables.md        # Mechanism → intent → Mistral expression; script
│   │                            #   decision tree; scoring axes
│   └── source-anatomy.md        # Claude vs Codex package anatomy; ingest order
├── scripts/                     # Executable tools the agent runs
│   ├── analyze_package.py       # Scan a source package → mechanism inventory
│   │                            #   (platform, tools, hooks, env vars, script classes,
│   │                            #   missing references) — --json, exit 0/1/2
│   ├── scaffold_skill.py        # Generate the output skeleton per target (CLI folder
│   │                            #   with preserved scripts/openai.yaml; Work with
│   │                            #   merge warnings; API JSON with assets +
│   │                            #   isExecutable) — --json
│   └── validate_skill.py       # Validate the converted package against the Agent
│                                #   Skills spec + per-target rules (name regex,
│                                #   description limit, CLI-only fields on Work,
│                                #   leftover ${VAR}s, allowed-tools registry) —
│                                #   --json, exit 0/1/2
└── assets/
    ├── output-templates.md      # Paste-ready output skeletons per target
    └── port-report-template.md  # The report delivered with every conversion
```

## How the agent uses it

1. `scripts/analyze_package.py <pkg>` → mechanism inventory (the model reads
   it as the evidence base for capability mapping).
2. Load the relevant `references/` files for the target and mechanisms found.
3. `scripts/scaffold_skill.py` → output skeleton; the model fills the body
   per `mapping-tables.md` using `assets/output-templates.md` patterns.
4. `scripts/validate_skill.py <out> --target <t>` → hard gate before delivery.
5. Fill `assets/port-report-template.md` → deliver package + report.

## Verification

- All three scripts tested against real packages (`research/pulse`,
  `product-team/skills/product-manager-toolkit`): analyze correctly detects
  platform, Claude tool references, env vars (`${RESEARCH_DIR}`,
  `$(date)`), classifies scripts (formula-maskable / text-analysis /
  filesystem-bound / stateful), flags missing references.
- SKILL.md validated with the real Mistral Vibe parser + pydantic
  `SkillMetadata` from the mistralai/mistral-vibe source.
- Facts in references/ extracted from `mistralai/mistral-vibe` (source) and
  `mistralai/platform-docs-public` (docs source of docs.mistral.ai).
