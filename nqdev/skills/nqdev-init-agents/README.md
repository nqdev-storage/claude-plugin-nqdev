# nqdev-init-agents

Analyzes a project and creates the guidance files AI agents need (CLAUDE.md, ignore rules, `code-rules.md`). Existing files are never overwritten. Version and behavior are defined in [SKILL.md](SKILL.md).

## Quick Start

```bash
/nqdev:nqdev-init-agents                                  # root CLAUDE.md and the base files
/nqdev:nqdev-init-agents --sub-claude                     # plus CLAUDE.md per layer (src, tests, db, docs)
/nqdev:nqdev-init-agents --sub-claude --claude-depth=3    # deeper hierarchy for large projects
/nqdev:nqdev-init-agents --sub-claude --claude-dirs=packages/api,packages/web   # monorepo
/nqdev:nqdev-init-agents --rtk                            # plus .rtk/
/nqdev:nqdev-init-agents --opencode                       # plus .opencode/ and .env template
```

## What It Creates

| Output | When |
|---|---|
| `CLAUDE.md` (root) with Database, Git and Workflow Safety callouts | Always |
| `.claudeignore` | Always |
| `.claude/rules/code-rules.md` and `.claude/.gitignore` | Always |
| `draft/` and `draft/docs/` (each with `.gitkeep`) plus the matching `.gitignore` block | Always |
| `docs/Business-Document.md` | When the project has a `docs/` folder |
| `CLAUDE.md` per layer | `--sub-claude` |
| `.rtk/`, `.rtk-usage.md` | `--rtk` (auto-detected by default) |
| `.opencode/opencode.jsonc`, `.env` template | `--opencode` |

`code-rules.md` is copied from `templates/code-rules.md` and holds: Testing rules (approved test phone numbers only), Comment Rule (5 rules plus a per-developer label), Database Execution Policy (Claude never runs SQL; statements are tagged `-- NOT run by Claude — cần DBA review` for a DBA), Git Commit Policy, Development Workflow Policy and Task Execution Policy.

## Flags

| Flag | Purpose | Default |
|---|---|---|
| `--sub-claude`, `--hierarchical-claude` | Create CLAUDE.md per layer | Off |
| `--no-hierarchical-claude` | Turn hierarchy off | n/a |
| `--claude-depth=N` | Hierarchy depth, 1-15 | 2 |
| `--claude-dirs=a,b` | Target directories | Auto-detect |
| `--rtk`, `--no-rtk` | Turn `.rtk/` on or off | Auto-detect |
| `--opencode` | Create OpenCode config | Off |

## Files in This Skill

- [SKILL.md](SKILL.md): the instructions the agent follows
- [CHANGELOG.md](CHANGELOG.md): version history
- [docs/INDEX.md](docs/INDEX.md): which document to read for what ([SPECS](docs/SPECS.md), [PRD](docs/PRD.md))
- `templates/`: `code-rules.md`, `Business-Document.md`, `agents.md`, `README.md`
