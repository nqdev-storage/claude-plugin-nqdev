# CHANGELOG — nqdev-init-agents

Format: `## [version] — date`. Versions follow Semantic Versioning (MAJOR.MINOR.PATCH).

---

## [1.8.1] — 2026-11-21

### Changed
- `templates/Business-Document.md`: states it is project-level only and points to `docs/brd/` for module requirements; "Success Criteria" lists project outcomes and points to BRD sections 1 and 7 for MVP scope instead of a feature list; "Related Documents" drops the `SPECS.md` link (not created in target repos) and links `docs/brd/`.
- `templates/agents.md`: documentation agents read `docs/Business-Document.md` only when it has been filled in.
- SKILL.md step 5 and README: Business-Document does not replace per-module BRDs (`nqdev-brd-prd-writer`).
- Existing `docs/Business-Document.md` files in target repos are not overwritten; update them by hand if needed.

## [1.8.0] — 2026-11-20

### Added
- Step 6 and section "Thư mục draft": always create `draft/.gitkeep` and `draft/docs/.gitkeep` (no overwrite), append the `draft/*` ignore block (`!draft/.gitkeep`, `!draft/docs/.gitkeep`) to the target `.gitignore` if missing, and note `draft/` in the root `CLAUDE.md`.

### Changed
- Completion criteria and final summary now include `draft/`.

## [1.7.1] — 2026-11-19

### Changed
- Comment label examples (SKILL.md and `templates/code-rules.md` v2.2.2) use the `[<label>]` placeholder instead of a fixed `[nqdev]` label.

## [1.7.0] — 2026-11-19

### Changed
- Development Workflow Policy rule 0 (SKILL.md and `templates/code-rules.md` v2.2.1) suggests `/nqdev:nqdev-task-flow` (skill `nqdev-flow` was renamed). Existing `code-rules.md` files are not overwritten; edit rule 0 by hand.
- Description points to `nqdev-task-flow` instead of `nqdev-flow`.

## [1.6.4] — 2026-11-17

### Fixed
- Step 4 resolves the template path from the skill's base directory instead of `${CLAUDE_PLUGIN_ROOT}`, which may not be substituted.

## [1.6.3] — 2026-11-17

### Added
- Development Workflow Policy rule 0 (`templates/code-rules.md` v2.2.0): for new features, bug fixes and releases, suggest `/nqdev:nqdev-flow` first when the `nqdev` plugin is installed. Existing `code-rules.md` files are not overwritten.

### Changed
- Description: not for a plain codebase-summary CLAUDE.md (built-in `/init`) or while building a feature.
- Steps 4-5 point to `templates/code-rules.md` and `templates/Business-Document.md`, so generated files match the bundled templates.
- `compatibility`: Claude.ai prints the files to chat instead of writing them.

## [1.6.2] — 2026-11-16

### Changed
- `docs/PRD.md`, `docs/SPECS.md`, `manifest.json`: removed the non-existent `nqdev-codebase-analyst` from related skills; renamed `nqdev-client-requirement-insight` to `nqdev-requirement-estimator`. Documentation only.

## [1.6.1] — 2026-11-11

### Added
- Comment Rule rule 5: comments are short by default (one line, about 100 characters); no multi-paragraph comments, no change-history narration (`templates/code-rules.md` v2.1.1).

## [1.6.0] — 2026-11-09

### Added
- Task Execution Policy in generated `code-rules.md` (`templates/code-rules.md` v2.1.0): one task at a time within the approved plan, small scoped commits, declare files before coding, no new dependencies or out-of-scope edits without approval, stop and ask on ambiguity.

### Changed
- The hard constraint in SKILL.md covers four verbatim policies (DB, Git, Workflow, Task Execution).
- README and manifest list the full `code-rules.md` contents.

## [1.5.0] — 2026-11-04

### Changed
- SKILL.md refactored from about 1155 to about 47 lines (progressive disclosure); history moved to this file, optional setups to `references/`.
- `code-rules.md` is a mandatory step (it was nested under "Optional").
- `templates/code-rules.md` v2.0.0 adds Comment Rule (4 rules plus per-dev label) and the Database, Git and Workflow policies.
- `settings.share.json` is documented as per-machine and not committed; unverified `claude.ai/*` permission patterns removed.
- Frontmatter aligned with the project metadata template.

## [1.4.13] — 2026-09-28

### Changed
- Comment Rule cut from about 250 lines to 4 rules: dropped the philosophy essay, decision matrix, per-language examples and checklist; same intent (WHY not WHAT, only non-obvious logic, clean up on update).

## [1.4.12] — 2026-09-27

### Added
- Database Execution Policy in `code-rules.md`: Claude/agents never execute SQL against any database (dev, staging, production) by any means (CLI, ORM, MCP). Applies to DDL, DML and migrations; read-only `SELECT` is exempt. SQL is tagged `-- NOT run by Claude — cần DBA review` for a DBA to run.
- "Database Safety" callout in the root CLAUDE.md.

## [1.4.11] — 2026-09-27

### Added
- `--opencode` flag: creates `.opencode/opencode.jsonc` (schema reference, MCP section filled from `.mcp.json` if present), `.opencode/.gitignore` and a `.env` template.
- Fixes the project `.gitignore`: removes `!.env` lines and ignores `.env`.

## [1.4.10] — 2026-09-25

### Changed
- Renamed `.claude/settings.local.json` to `.claude/settings.share.json`; `.gitignore` pattern changed from `*.local.json` to `*.share.json`.

## [1.4.9] — 2026-09-24

### Added
- Optional `.claude/settings.local.json` generation with a `permissions.allow` array (renamed in 1.4.10).

## [1.4.8] — 2026-09-21

### Changed
- Merged `testing-rules.md` and `comment-cleanup-rule.md` into a single `code-rules.md`: testing rules with the approved phone numbers (`0909090909`, `0765418062`) plus comment guidelines.

## [1.4.7] — 2026-08-28

### Added
- `--rtk` and `--no-rtk` flags; `.rtk/` setup is auto-detected from the project type by default.

### Removed
- `.rtk-gitkeep` references.

## [1.4.6] — 2026-08-25

### Changed
- `.rtk/.gitignore` template gains RTK AI references and a note on what does and does not belong in `.rtk/`.

## [1.4.5] — 2026-08-20

### Added
- `.rtk/` directory for runtime and temporary files (git-ignored), `.rtk/.gitignore` template and `.rtk-usage.md`.

## [1.4.4] — 2026-08-20

### Added
- `.claude/rules/` directory with `testing-rules.md` (replaced by `code-rules.md` in 1.4.8).

### Changed
- `agents.md` reduced to a pure routing guide that points to `.claude/rules/`.

## [1.4.3] — 2026-08-13

### Added
- `agents.md` template: routing guide for AI agents, with the core phone-number testing rule.

## [1.4.2] — 2026-08-13

### Added
- `docs/Business-Document.md` template (vision, goals, stakeholders, KPIs, risks).

## [1.4.1] — 2026-08-13

### Added
- `.claude/.gitignore` created with `.claude/` (`.env`, `*.local.json`, secrets and temp patterns).

## [1.4.0] — 2026-08-10

### Added
- Optional hierarchical CLAUDE.md (`src/`, `tests/`, `db/`, `docs/`) with scope resolution; off by default.
- Flags `--hierarchical-claude`, `--sub-claude`, `--claude-depth=N`, `--claude-dirs=a,b`.
- `docs/SPECS.md`, `docs/PRD.md`, `docs/INDEX.md`.

## [1.3.0] — 2026-07-28

### Added
- Root CLAUDE.md, tech stack detection (Node.js, Next.js, Python, Java/Spring, PHP/Laravel, .NET, Go/Ruby), `.claudeignore`, optional `.claude/` configuration, 6 templates, basic CLI.

## [1.2.0] — 2026-07-15

### Changed
- Improved `.claudeignore` patterns and artifact detection; fixed false positives.

## [1.1.0] — 2026-07-01

### Changed
- Larger template library, better error messages and project analysis, more frameworks; fixed stack-detection edge cases.

## [1.0.0] — 2026-06-15

### Added
- Initial release: root CLAUDE.md generation, basic tech stack detection, template system, CLI.
