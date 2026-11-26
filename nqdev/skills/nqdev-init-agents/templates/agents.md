# Agent Routing Guide

This file serves as a routing guide for AI agents working on this project. It directs you to the main project documentation (CLAUDE.md) and project-specific rules (.claude/rules/).

---

## 🎯 Start Here: Read CLAUDE.md First

**All AI agents must read the main project guidance files:**

### Root Level
- 📖 **CLAUDE.md** — Main project guidance & standards
  - Project overview & objectives
  - Tech stack best practices
  - Coding standards & conventions
  - Testing requirements
  - Deployment guidelines
  - All project-wide rules

### Hierarchical Level (if using --sub-claude)
Read these scope-specific CLAUDE.md files for your working area:

| File | Scope | Content |
|------|-------|---------|
| **src/CLAUDE.md** | Source Code | Code organization, naming, style guide |
| **tests/CLAUDE.md** | Testing | Testing frameworks, patterns, coverage |
| **db/CLAUDE.md** | Database | Migrations, queries, indexing, performance |
| **docs/CLAUDE.md** | Documentation | Writing style, code examples, formats |

---

## ⭐ Project Rules

**For project-specific rules, read:**

### .claude/rules/
- 📋 **testing-rules.md** — Testing guidelines & restrictions
  - Phone number testing rules (CRITICAL)
  - Unit testing standards
  - Integration testing guidelines
  - E2E testing requirements
  - Code review requirements for tests

- 📋 **code-rules.md** — General code guidelines (if present)
  - Code organization patterns
  - Naming conventions
  - Error handling standards
  - Security requirements

**Critical Rule Summary**: Phone number testing ONLY uses `0909090909` and `0765418062`. See `.claude/rules/testing-rules.md` for details.

---

## 📋 Agent Workflow

### Step 1: Review Documentation
- [ ] Read **CLAUDE.md** (root level)
- [ ] If working on specific area, read relevant sub-CLAUDE.md
- [ ] Read **project rules** in `.claude/rules/` (testing-rules.md, code-rules.md)
- [ ] Read related templates (TESTING.md, etc.)
- [ ] Understand project standards & conventions

### Step 2: Follow Project Rules
- [ ] Review `.claude/rules/testing-rules.md` for testing guidelines
- [ ] Follow phone number restrictions (0909090909, 0765418062 only)
- [ ] Follow coding standards from CLAUDE.md
- [ ] Respect project-specific patterns
- [ ] Apply rules from `.claude/rules/code-rules.md` if present

### Step 3: Execute Tasks
- [ ] Apply learned standards and rules
- [ ] Reference CLAUDE.md and `.claude/rules/` when uncertain
- [ ] Use approved test data only
- [ ] Follow established patterns

### Step 4: Verify Compliance
- [ ] Ensure code follows standards
- [ ] Validate against project rules (.claude/rules/)
- [ ] Check test data compliance (approved phone numbers only)
- [ ] Check against project patterns
- [ ] Update documentation if needed

---

## 🔗 Quick Navigation

| Need | Read This | Location |
|------|-----------|----------|
| Project Overview | CLAUDE.md | Root |
| Coding Standards | CLAUDE.md or src/CLAUDE.md | Root or src/ |
| **Project Rules** | **testing-rules.md** | **.claude/rules/** |
| **Code Rules** | **code-rules.md** | **.claude/rules/** |
| Testing Guidelines | TESTING.md or tests/CLAUDE.md | templates/ or tests/ |
| Database Patterns | DATABASE.md or db/CLAUDE.md | templates/ or db/ |
| API Design | API_ENDPOINTS.md | templates/ |
| Business Context | Business-Document.md | docs/ |
| Code Organization | SOURCE_CODE.md | templates/ |
| UI Patterns | COMPONENTS.md | templates/ |
| Documentation Style | DOCUMENTATION.md | templates/ |

---

## 📝 Test Data Reference

| Test Value | Purpose | Usage | Rule Location |
|-----------|---------|-------|----------------|
| 0909090909 | Primary test phone | Any phone number test | `.claude/rules/testing-rules.md` |
| 0765418062 | Secondary test phone | Any phone number test | `.claude/rules/testing-rules.md` |

**No other phone numbers should be used in test data.**  
**See `.claude/rules/testing-rules.md` for complete testing rules.**

---

## 🎓 For Different Agent Types

### Code Generation Agents
1. Read CLAUDE.md (root) first
2. If working in src/, read src/CLAUDE.md
3. Read `.claude/rules/code-rules.md` if present
4. Follow coding standards exactly
5. Use approved test data only

### Testing Agents
1. Read **`.claude/rules/testing-rules.md`** (REQUIRED)
2. Read tests/CLAUDE.md or TESTING.md
3. Reference CLAUDE.md for general rules
4. Use ONLY approved test phone numbers (0909090909, 0765418062)
5. Log all test data and validate against rules

### Documentation Agents
1. Read DOCUMENTATION.md in templates/
2. Read docs/CLAUDE.md if it exists
3. Reference docs/Business-Document.md for project context only if it has been filled in (skip placeholders); module requirements are in docs/brd/
4. Follow established writing style
5. Check `.claude/rules/` for documentation-specific rules

### Database Agents
1. Read DATABASE.md in templates/
2. Read db/CLAUDE.md if it exists
3. Reference CLAUDE.md for general rules
4. Check `.claude/rules/code-rules.md` for database patterns
5. Follow migration patterns

---

## ⚠️ Violation Reporting

If you find code using phone numbers outside approved values:
1. Flag it immediately
2. Document location and context
3. Request correction
4. Report to project maintainers

---

## 🔄 File Hierarchy

```
project/
├── CLAUDE.md                 ← START HERE (main project guidance)
├── agents.md                 ← You are here (routing guide)
├── .claude/
│   ├── rules/               ← Project-specific rules (NEW v1.4.4)
│   │   ├── testing-rules.md ← Testing & phone number rules (CRITICAL)
│   │   └── code-rules.md    ← Code-specific rules
│   ├── agents/
│   ├── config.json
│   └── templates/
├── src/CLAUDE.md            ← Scope-specific guidance
├── tests/CLAUDE.md          ← Scope-specific guidance
├── db/CLAUDE.md             ← Scope-specific guidance
├── docs/
│   ├── CLAUDE.md            ← Documentation standards
│   └── Business-Document.md ← Business context
└── .claudeignore            ← Files to ignore for AI
```

---

## 📌 Key Principles

1. **CLAUDE.md is Primary** — Always refer to CLAUDE.md for main guidance
2. **Hierarchical Files are Scope-Specific** — Read sub-CLAUDE.md for your area
3. **One Test Phone Rule** — Only use 0909090909 or 0765418062
4. **Documentation is Authoritative** — Follow what's written in CLAUDE.md
5. **When in Doubt, Ask** — Reference CLAUDE.md or reach out to maintainers

---

## 📞 Support

**Questions about?** → **Read This File:**

| Question | File | Location |
|----------|------|----------|
| **Project rules** | **testing-rules.md** | **.claude/rules/** |
| **Code rules** | **code-rules.md** | **.claude/rules/** |
| **Phone testing** | **testing-rules.md** | **.claude/rules/** |
| Project standards | CLAUDE.md | Root |
| Code organization | src/CLAUDE.md or SOURCE_CODE.md | src/ or templates/ |
| Testing practices | tests/CLAUDE.md or TESTING.md | tests/ or templates/ |
| Database work | db/CLAUDE.md or DATABASE.md | db/ or templates/ |
| API design | API_ENDPOINTS.md | templates/ |
| Documentation | DOCUMENTATION.md or docs/CLAUDE.md | templates/ or docs/ |
| UI components | COMPONENTS.md | templates/ |
| Business context | Business-Document.md | docs/ |

---

**Status**: Active  
**Purpose**: Routing guide for AI agents  
**Last Updated**: [Current Date]  
**Next Step**: Read CLAUDE.md for full project guidance
