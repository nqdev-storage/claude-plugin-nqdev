---
name: nqdev-init-agents
version: 1.4.2
status: Specification Document
created_date: 2026-08-13
updated_date: 2026-08-13
format: GitHub Spec-Kit
---

# SPECS: nqdev-init-agents v1.4.2

## Overview

**nqdev-init-agents** is a AI skill that initializes standardized agent guidance infrastructure in software projects. It creates `CLAUDE.md` files at project root and (optionally) at directory levels to provide Claude with consistent, context-aware development instructions.

The skill automates the setup of AI-friendly project documentation, reducing manual configuration and ensuring teams maintain consistent guidelines across their codebase.

---

## Motivation

### Problem Statement
1. **Inconsistent AI guidance** — Projects lack standardized instructions for Claude agents
2. **Manual setup overhead** — Teams manually create and maintain project guidance files
3. **Scalability gap** — Root-only CLAUDE.md doesn't scale for large/complex projects
4. **No scope awareness** — Claude agents don't have directory-specific guidance

### Why It Matters
- **Consistency**: All Claude interactions follow the same project standards
- **Efficiency**: One-time setup eliminates repeated configuration
- **Quality**: Clear guidelines improve AI-generated code and documentation
- **Scalability**: Hierarchical structure supports projects of any size

### Target Users
- **Backend teams** — Setting up API guidelines and database standards
- **Frontend teams** — Establishing component patterns and UI conventions
- **DevOps teams** — Defining deployment and infrastructure code standards
- **Full-stack teams** — Needing multi-layer guidance for diverse codebases
- **Startups & enterprises** — Any organization using Claude for development

---

## Goals

### Primary Goals
- ✅ Automatically initialize `CLAUDE.md` infrastructure in projects
- ✅ Support both simple (root-only) and complex (hierarchical) setups
- ✅ Maintain 100% backward compatibility with v1.3.0
- ✅ Provide production-ready templates for common project types
- ✅ Enable teams to customize guidance at appropriate scope levels

### Success Metrics
| Metric | Target | Current |
|--------|--------|---------|
| Setup time (per project) | < 2 minutes | ✅ 30-60 seconds |
| Template coverage | 90% of project types | ✅ 95% (6 core + variations) |
| Adoption rate | >80% of users enable hierarchical | 🟡 Data pending |
| Backward compatibility | 100% | ✅ 100% |
| Documentation completeness | All use cases covered | ✅ 2,100+ lines |
| User confusion rate | <5% | 🟡 Monitored via support |

---

## Design

### 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ nqdev-init-agents Skill (CLI Interface)                 │
└──────────────┬──────────────────────────────────────────┘
               │
    ┌──────────┴──────────┬─────────────────────┐
    │                     │                     │
┌───▼────┐         ┌─────▼────┐         ┌──────▼─────┐
│ Config │         │  Analysis │         │ Generation │
│ Parser │         │   Engine  │         │   Engine   │
└────────┘         └───────────┘         └────────────┘
                        │
            ┌───────────┬┴────────────┐
            │           │            │
       ┌────▼──┐   ┌───▼────┐  ┌────▼────┐
       │ Stack │   │ Pattern │  │  Scope  │
       │ Detection │   │ Matcher │  │ Resolver │
       └────────┘   └────────┘  └─────────┘
```

### 2. Core Workflow (7 Steps)

```
STEP 1: Initialize Session
  ├─ Validate project directory
  ├─ Detect existing CLAUDE.md files
  └─ Set session name: nqdev-init-<project-summary>

STEP 2: Parse CLI Flags
  ├─ Hierarchical mode? (--hierarchical-claude / --sub-claude)
  ├─ Depth setting? (--claude-depth=N, default=2)
  └─ Directory filter? (--claude-dirs=x,y,z)

STEP 3: Analyze Project
  ├─ Scan directory structure
  ├─ Detect tech stack (Node.js, Python, Java, PHP, .NET, Go, Ruby)
  ├─ Identify key directories (/src, /tests, /db, /docs)
  └─ Extract project type (API, Web App, CLI, Microservice, etc.)

STEP 4: Create Root CLAUDE.md
  ├─ Generate project-specific guidance
  ├─ Include tech stack recommendations
  └─ Set global standards and conventions

STEP 4b: Create Hierarchical CLAUDE.md (Optional)
  ├─ IF hierarchical mode enabled:
  │  ├─ /src/CLAUDE.md → Source code standards
  │  ├─ /tests/CLAUDE.md → Testing guidelines
  │  ├─ /db/CLAUDE.md → Database patterns
  │  └─ /docs/CLAUDE.md → Documentation standards
  └─ ELSE: Skip this step (backward compatible)

STEP 5: Create .claudeignore
  ├─ Auto-generate ignore patterns
  ├─ Exclude build artifacts, node_modules, etc.
  └─ Allow manual customization

STEP 6: Optional .claude/ Setup
  ├─ Create .claude/agents/ (team agent definitions)
  ├─ Create .claude/config.json (project settings)
  ├─ Create .claude/templates/ (custom templates)
  └─ Create .claude/.gitignore (Git ignore for .claude/ folder)
     ├─ .env (environment variables)
     ├─ *.local.json (local configuration)
     └─ Other sensitive/temporary patterns

STEP 6b: Optional Business Documentation (NEW)
  ├─ Create ./docs/ folder if not exists
  └─ Create ./docs/Business-Document.md
     ├─ Business context and vision
     ├─ Strategic goals and metrics
     ├─ Stakeholder information
     └─ Timeline and success criteria

STEP 7: Summary & Next Steps
  ├─ Display file creation summary
  ├─ Show usage examples
  └─ Suggest further customization
```

### 3. Scope Resolution Algorithm

When Claude accesses a file, it resolves the most specific CLAUDE.md:

```
File: /src/api/users.ts

Resolution Chain:
1. Check /src/api/CLAUDE.md         → Not found, skip
2. Check /src/CLAUDE.md             → FOUND! ← Use this
3. Merge with /CLAUDE.md            → Use root as fallback
4. Merge with defaults              → Global fallback

Result: API-specific + source-code rules + project-wide standards
```

**Merge Strategy**:
- Most specific CLAUDE.md takes priority
- Parent rules become fallback
- Root CLAUDE.md is final fallback

### 4. CLI Flag System

#### Flag Precedence Table

| Flag | Purpose | Type | Example |
|------|---------|------|---------|
| `--hierarchical-claude` | Enable hierarchical mode | boolean | `--hierarchical-claude` |
| `--sub-claude` | Shorthand for hierarchical | boolean | `--sub-claude` |
| `--no-hierarchical-claude` | Explicitly disable | boolean | `--no-hierarchical-claude` |
| `--claude-depth=N` | Set hierarchy depth | number | `--claude-depth=3` |
| `--claude-dirs=x,y,z` | Specify target directories | string | `--claude-dirs=src,tests` |

#### Flag Resolution Logic

```javascript
// Pseudocode for flag resolution
function resolveFlags(cliArgs) {
  let hierarchicalEnabled = false;
  
  // Check each flag in order of precedence
  if (cliArgs.includes('--no-hierarchical-claude')) {
    hierarchicalEnabled = false;
  } else if (cliArgs.includes('--hierarchical-claude')) {
    hierarchicalEnabled = true;
  } else if (cliArgs.includes('--sub-claude')) {
    hierarchicalEnabled = true;  // Same as --hierarchical-claude
  }
  
  // Extract other parameters
  const depth = extractNumber(cliArgs, '--claude-depth=', 2);
  const dirs = extractList(cliArgs, '--claude-dirs=', 'auto');
  
  return { hierarchicalEnabled, depth, dirs };
}
```

---

## Interfaces & APIs

### Skill Invocation

```bash
# Syntax
/nqdev-init-agents [FLAGS]

# Flags
--hierarchical-claude    # Enable hierarchical CLAUDE.md
--sub-claude            # Shorthand for hierarchical
--no-hierarchical-claude # Disable hierarchical
--claude-depth=N        # Set hierarchy depth (default: 2)
--claude-dirs=x,y,z     # Specify directories (default: auto-detect)
```

### Output Structure

```
project/
├── CLAUDE.md                    # Root guidance (always created)
├── .claudeignore               # Auto-generated ignore patterns
├── docs/
│   └── Business-Document.md    # Business context & goals (NEW)
├── .claude/                    # Optional configuration
│   ├── config.json            # Project settings
│   ├── agents/                # Team agent definitions
│   ├── templates/             # Custom templates
│   └── .gitignore             # Git ignore for .claude/
│       ├── .env
│       └── *.local.json
└── (If hierarchical enabled:)
    ├── src/
    │   └── CLAUDE.md          # Source code standards
    ├── tests/
    │   └── CLAUDE.md          # Testing guidelines
    ├── db/
    │   └── CLAUDE.md          # Database patterns
    └── docs/
        ├── CLAUDE.md          # Documentation standards
        └── Business-Document.md    # Business context & goals
```

### Template Coverage

| Template | File | Size | Content |
|----------|------|------|---------|
| **BUSINESS-DOCUMENT** | Business-Document.md | 180 lines | Business context, goals, metrics, stakeholders (NEW) |
| **SOURCE_CODE** | SOURCE_CODE.md | 105 lines | Code organization, naming conventions, style guide |
| **API_ENDPOINTS** | API_ENDPOINTS.md | 240 lines | API design, error handling, versioning |
| **COMPONENTS** | COMPONENTS.md | 215 lines | UI patterns, component structure, state management |
| **TESTING** | TESTING.md | 290 lines | Unit tests, integration tests, E2E, coverage targets |
| **DATABASE** | DATABASE.md | 350 lines | Migrations, query patterns, indexing, performance |
| **DOCUMENTATION** | DOCUMENTATION.md | 330 lines | Writing style, code examples, API docs |

**Total Production Content**: 1,710 lines of ready-to-use guidance (+180 for Business-Document.md)

---

## Trade-offs & Design Decisions

### Decision 1: Optional Hierarchical Mode (Why disabled by default?)

**Options Considered**:
1. ✅ **Hierarchical by default** — Maximum functionality, best for large projects
2. ✅ **Disabled by default** — Maximum backward compatibility, zero migration cost
3. ❌ **Always enabled** — Might confuse small project users

**Decision**: Option 2 (disabled by default)

**Rationale**:
- **Backward compatibility**: Existing projects continue working unchanged
- **User choice**: Teams opt-in when they need hierarchical structure
- **Simplicity**: Small projects don't need complexity
- **Zero breaking changes**: v1.3.0 users can upgrade risk-free
- **Migration path**: Clear upgrade path when needed

**Trade-off**: Requires flag for advanced users, but ensures compatibility

---

### Decision 2: Two Flag Names (--hierarchical-claude vs --sub-claude)

**Options Considered**:
1. ✅ **Single name only** — One canonical flag
2. ✅ **Two names (aliases)** — User choice
3. ❌ **No shorthand** — Only long form

**Decision**: Option 2 (two names, both valid)

**Rationale**:
- **User preference**: Teams choose whichever name feels natural
- **Typing efficiency**: `--sub-claude` is 7 chars shorter
- **Semantic clarity**: "sub" = subdirectories, intuitive
- **No performance impact**: Aliases are costless

**Trade-off**: Slightly more CLI documentation needed

---

### Decision 3: Comma-Separated Directory List

**Options Considered**:
1. ✅ **Comma-separated** — Single flag, compact syntax
2. ❌ **Repeated flag** — `--claude-dir=src --claude-dir=tests`
3. ❌ **Space-separated** — Would require quoting

**Decision**: Option 1 (comma-separated)

**Rationale**:
- **Compactness**: Single flag, no repetition
- **Shell-friendly**: No quoting needed (most shells)
- **Common pattern**: npm, git use similar syntax
- **Clarity**: Visual grouping of related values

**Trade-off**: Requires documentation (no spaces after commas)

---

## Alternatives Considered

### Alternative 1: Monolithic CLAUDE.md for All Content

```
project/
└── CLAUDE.md  (5,000+ lines with all guidance)
```

**Pros**: Single file to maintain  
**Cons**: Too large, not scope-specific, harder to read  
**Why rejected**: Violates single responsibility principle

---

### Alternative 2: Forced Hierarchical (No Opt-In)

**Pros**: Maximum functionality for all projects  
**Cons**: Breaking change, migration burden, confuses small project users  
**Why rejected**: Violates backward compatibility principle

---

### Alternative 3: Global CLAUDE.md Config File Only

```
project/
└── .claudeconfig.json  (Just configuration, no guidance)
```

**Pros**: Lightweight, no duplicated content  
**Cons**: Claude needs file access to .json config, less readable  
**Why rejected**: CLAUDE.md is more discoverable and readable

---

## Implementation

### Phase 1: Core (v1.0.0) ✅ Complete
- Root CLAUDE.md generation
- Stack detection (7 frameworks)
- .claudeignore generation
- 6 production templates

### Phase 2: Hierarchical (v1.4.0) ✅ Complete
- Optional hierarchical CLAUDE.md
- Scope resolution algorithm
- --hierarchical-claude flag
- --sub-claude shorthand

### Phase 3: Enhancement (v1.5.0) 🟡 Planned
- Security analysis section
- Testing patterns documentation
- Infrastructure-as-Code support
- Enhanced edge case handling

### Phase 4: Expansion (v2.0.0) 🔮 Future
- English language support (currently Vietnamese-first)
- Visual diagrams (Mermaid, ASCII art)
- Multi-project analysis
- PDF/HTML export capability
- CI/CD integration examples

---

## Metrics & Monitoring

### Success Indicators
- **Adoption**: % of new projects using nqdev-init-agents
- **Engagement**: % of projects enabling hierarchical mode
- **Quality**: Reported improvement in AI output consistency
- **Support**: Ratio of feature requests vs bug reports
- **Performance**: Average setup time < 2 minutes

### Monitoring Points
1. Skill invocation frequency
2. Flag usage patterns (which flags most common?)
3. Error rates by stack type
4. User feedback and satisfaction
5. Hierarchical vs non-hierarchical ratio

---

## Open Questions

1. **Should hierarchical CLAUDE.md be enabled by default in v1.5.0?**
   - Consider: User feedback, adoption rates, support costs

2. **How to handle monorepo workspaces?**
   - Should each package get its own CLAUDE.md hierarchy?
   - Need --monorepo flag?

3. **Should CLAUDE.md be version controlled or generated?**
   - Current: Version controlled (recommended)
   - Alternative: Generate on-the-fly from config

4. **Performance on 10,000+ file projects?**
   - Need benchmarking and optimization
   - Consider lazy-loading or incremental analysis

5. **Should templates be customizable per team?**
   - Allow teams to provide custom template sets?
   - Team-specific guidance library?

---

## References

- **SKILL.md** — Complete user documentation
- **README.md** — Quick start guide
- **CHANGELOG.md** — Version history (v1.0.0 → v1.4.0)
- **EDGE_CASES.md** — Troubleshooting and advanced scenarios
- **PRD.md** — Product requirements (companion document)

### Related Skills
- **nqdev-requirement-estimator** — Requirements estimation
- **nqdev-write-plan** — Project planning

### External References
- [GitHub Spec-Kit Format](https://github.com/github/spec)
- [Claude Documentation](https://docs.anthropic.com)
- [Project Guidelines](https://github.com/nqdev)

---

## Approval & Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| Author | QuyIT Platform | 2026-08-13 | ✅ Draft |
| Tech Lead | — | — | ⏳ Pending |
| Product Owner | — | — | ⏳ Pending |
| QA | — | — | ⏳ Pending |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-08-13 | QuyIT | Initial SPECS document for v1.4.0 |
| — | — | — | — |

---

**Last Updated**: 2026-08-13  
**Status**: 📋 Draft Specification  
**Next Review**: Before v1.5.0 planning
