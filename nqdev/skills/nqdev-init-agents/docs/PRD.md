---
name: nqdev-init-agents
version: 1.4.1
document_type: Product Requirement Document (PRD)
created_date: 2026-08-13
updated_date: 2026-08-13
status: Active
---

# PRD: nqdev-init-agents v1.4.0

## Executive Summary

**Product Name**: nqdev-init-agents  
**Version**: 1.4.0  
**Status**: ✅ Production Ready  
**Release Date**: August 10, 2026  

**One-Line Description**: An AI skill that automatically initializes standardized Claude guidance files (CLAUDE.md) in software projects, with optional hierarchical scope-specific guidance for larger codebases.

**Business Value**: Reduces project setup time from hours to minutes, ensures consistent AI-assisted development practices, and scales from small to large teams.

---

## Product Overview

### What Is nqdev-init-agents?

A reusable AI skill that:
1. **Analyzes** your project structure and tech stack
2. **Creates** Claude agent guidance files (CLAUDE.md) automatically
3. **Configures** optional hierarchical guidance for complex projects
4. **Generates** project-specific patterns and standards
5. **Supports** 7+ programming ecosystems (Node.js, Python, Java, .NET, PHP, Go, Ruby)

### Who Benefits?

| User Type | Benefit |
|-----------|---------|
| **Engineering Teams** | Consistent AI-assisted coding practices |
| **Startups** | Fast project setup, reducing onboarding time |
| **Enterprises** | Scalable guidance for monorepos and microservices |
| **Solo Developers** | Instant project documentation and patterns |
| **Development Agencies** | Template-based client project setup |
| **Open Source Projects** | Community guidelines for AI contributors |

---

## Problem Statement

### Current Challenges

1. **Manual Setup Overhead**
   - Teams spend 2-4 hours manually creating project guidance
   - Documentation is inconsistent across projects
   - Updates are difficult to propagate

2. **Scale Limitations**
   - Root-only guidance doesn't cover large project complexity
   - Scope-specific standards (API vs UI vs DB) aren't separate
   - Claude agents lack directory-level context

3. **Knowledge Fragmentation**
   - Best practices live in multiple places (README, wiki, verbal)
   - New team members don't know the standards
   - Guidelines aren't enforced or updated consistently

4. **AI Output Quality**
   - Without clear guidance, Claude generates inconsistent code
   - Violations of team standards go unnoticed
   - Onboarding AI to team practices takes manual effort

5. **Team Growth Pain**
   - Hard to scale to 10+ engineers with diverse backgrounds
   - Architectural decisions aren't documented consistently
   - New team members repeat same mistakes

### Market Gap

Existing solutions:
- ❌ Manual CLAUDE.md creation (tedious, error-prone)
- ❌ Generic templates (not project-specific)
- ❌ No automation (not scalable)
- ❌ Flat structure (doesn't scale to large projects)

**Solution**: Automated, intelligent, scalable skill that adapts to your project

---

## Goals & Objectives

### Product Goals (OKRs)

**Objective 1: Adoption & Usage**
- Goal: 80% of nqdev projects use nqdev-init-agents by Q4 2026
- KR1: 500+ projects initialized
- KR2: 60%+ enable hierarchical mode for medium/large projects
- KR3: <5% churn rate (projects stop using)

**Objective 2: Quality & Satisfaction**
- Goal: Achieve 4.5/5 ⭐ user satisfaction
- KR1: 90%+ of guidance is considered "useful"
- KR2: 70%+ report improved AI output consistency
- KR3: <2% bug report rate

**Objective 3: Feature Completeness**
- Goal: Support 95%+ of common project types
- KR1: 7 framework stacks covered (✅ Done)
- KR2: 6 production templates included (✅ Done)
- KR3: Hierarchical mode for complex projects (✅ Done)

**Objective 4: Scalability**
- Goal: Support projects of any size efficiently
- KR1: <2 minute setup for projects <500 files
- KR2: <5 minute setup for projects 500-5,000 files
- KR3: Support 10,000+ file projects (monitoring)

---

## Requirements

### Functional Requirements

#### FR1: Automatic Project Analysis
- **Requirement**: Skill must detect project type, tech stack, and structure without manual input
- **Success Criteria**:
  - Detects 95%+ of common frameworks automatically
  - Identifies correct entry points and API routes
  - Categorizes files accurately (test, config, source)
- **Acceptance Tests**:
  - Node.js Express project → Correctly identified
  - Python FastAPI project → Correctly identified
  - Java Spring Boot project → Correctly identified

#### FR2: Root CLAUDE.md Generation
- **Requirement**: Create comprehensive root-level guidance file
- **Success Criteria**:
  - Contains project-specific standards
  - Includes tech stack best practices
  - Guides all subsequent Claude interactions
  - Is customizable and maintainable
- **Content**:
  - Project overview
  - Tech stack assumptions
  - Coding standards (naming, style)
  - Testing requirements
  - Deployment guidelines

#### FR3: Hierarchical CLAUDE.md (Optional)
- **Requirement**: Support directory-level guidance files for complex projects
- **Success Criteria**:
  - Creates scope-specific guidance (src/, tests/, db/, docs/)
  - Properly resolves scope when Claude accesses files
  - Merges parent and child rules correctly
  - Doesn't break existing projects (opt-in)
- **Activation**: Via `--hierarchical-claude` or `--sub-claude` flag

#### FR4: Template System
- **Requirement**: Provide production-ready templates for 6 major areas
- **Templates**:
  1. SOURCE_CODE.md — Naming, organization, style
  2. API_ENDPOINTS.md — REST/GraphQL design, versioning
  3. COMPONENTS.md — UI patterns, state management
  4. TESTING.md — Unit, integration, E2E strategies
  5. DATABASE.md — Migrations, queries, indexing
  6. DOCUMENTATION.md — Writing style, examples
- **Quality**: All templates should be immediately usable

#### FR5: .claudeignore Generation
- **Requirement**: Auto-generate ignore patterns for Claude
- **Success Criteria**:
  - Excludes build artifacts (node_modules, dist/, build/)
  - Excludes sensitive files (.env, secrets)
  - Excludes third-party code (vendor/, packages/)
  - Allows manual customization

#### FR6: CLI Interface
- **Requirement**: Simple, intuitive command-line interface
- **Flags**:
  - `--hierarchical-claude` — Enable hierarchical mode
  - `--sub-claude` — Shorthand for hierarchical
  - `--no-hierarchical-claude` — Explicitly disable
  - `--claude-depth=N` — Set hierarchy depth (default: 2)
  - `--claude-dirs=x,y,z` — Specify directories
- **Documentation**: All flags explained with examples

---

### Non-Functional Requirements

#### NFR1: Performance
- **Setup Time**: < 2 minutes for typical projects
- **Memory Usage**: < 100 MB during execution
- **Compatibility**: Works on Windows, macOS, Linux
- **Offline**: Can run without internet access

#### NFR2: Reliability
- **Success Rate**: 99%+ for supported project types
- **Error Handling**: Clear error messages for edge cases
- **Idempotency**: Running multiple times is safe (no duplicates)
- **Rollback**: Old CLAUDE.md files are not overwritten

#### NFR3: Maintainability
- **Code Quality**: 90%+ test coverage
- **Documentation**: Every feature documented with examples
- **Extensibility**: Easy to add new templates
- **Version Management**: Semantic versioning (major.minor.patch)

#### NFR4: Usability
- **Learning Curve**: New users should succeed without reading 50+ pages
- **Self-Documenting**: Help text explains every option
- **Guidance**: Tool suggests best practices ("Use --sub-claude for medium+ projects")
- **Accessibility**: Works with screen readers, clear text output

---

## User Stories & Use Cases

### Use Case 1: New Project Setup (Small Team)

**Actor**: Founder/Tech Lead  
**Scenario**: Starting new project, want to establish coding standards

```
GIVEN: New TypeScript Express project
WHEN: Run `/nqdev-init-agents`
THEN:
  ✓ CLAUDE.md created with Express best practices
  ✓ .claudeignore generated
  ✓ Ready to use Claude for pair programming
EXPECTED TIME: < 1 minute
```

---

### Use Case 2: Scaling to Multiple Codebases (Growing Team)

**Actor**: Tech Lead (10+ engineers)  
**Scenario**: Managing multiple services, need consistent standards

```
GIVEN: Monorepo with 3 services (API, Web, Workers)
WHEN: Run `/nqdev-init-agents --sub-claude --claude-dirs=services/api,services/web,services/workers`
THEN:
  ✓ Root CLAUDE.md for monorepo standards
  ✓ Service-specific CLAUDE.md for API/Web/Workers
  ✓ Claude understands scope-specific requirements
  ✓ Teams work independently with consistent patterns
EXPECTED TIME: < 2 minutes
BENEFIT: No context switching between codebases
```

---

### Use Case 3: Large Enterprise Project

**Actor**: Enterprise Architect  
**Scenario**: 500+ file codebase, multiple teams, complex structure

```
GIVEN: Large Spring Boot microservice with complex domain
WHEN: Run `/nqdev-init-agents --sub-claude --claude-depth=3`
THEN:
  ✓ Root guidance
  ✓ Layer-specific guidance (/src, /src/services, /tests, /db)
  ✓ Deep scope resolution
  ✓ Claude provides layer-appropriate suggestions
EXPECTED TIME: < 5 minutes
BENEFIT: Scaled to enterprise complexity
```

---

### Use Case 4: Open Source Project

**Actor**: Open Source Maintainer  
**Scenario**: Want consistent contributions from community/AI

```
GIVEN: Popular Node.js library
WHEN: Run `/nqdev-init-agents`
THEN:
  ✓ CLAUDE.md published in repo
  ✓ Contributors understand guidelines
  ✓ AI pull requests follow project standards
  ✓ Reduced review time for AI-generated PRs
EXPECTED TIME: < 1 minute
BENEFIT: Community can use same Claude guidance
```

---

## Success Metrics

### Quantitative Metrics

| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| Adoption | 500+ projects | # of initialized projects | Monthly |
| Setup Time | <2 min avg | Time from invocation to completion | Per run |
| Error Rate | <1% | Failed initializations / total runs | Daily |
| Hierarchical Usage | >50% | # using --hierarchical-claude | Monthly |
| User Satisfaction | 4.5/5 ⭐ | Survey feedback | Quarterly |

### Qualitative Metrics

- **User Testimonials**: Positive feedback on setup speed
- **Adoption Patterns**: Which flags/templates are most used
- **Community Engagement**: GitHub issues, feature requests
- **Expert Opinion**: Reviews from team leads and architects

---

## Feature Roadmap

### v1.4.0 ✅ (August 10, 2026) — CURRENT
- ✅ Hierarchical CLAUDE.md (optional, disabled by default)
- ✅ Scope resolution algorithm
- ✅ `--hierarchical-claude` and `--sub-claude` flags
- ✅ 6 production templates
- ✅ 100% backward compatibility

### v1.5.0 🟡 (September 15, 2026) — PLANNED
- 🟡 Security analysis section
- 🟡 Testing patterns module
- 🟡 Infrastructure-as-Code support
- 🟡 Enhanced edge case handling
- 🟡 Performance optimization for large projects

### v2.0.0 🔮 (Q4 2026) — FUTURE
- 🔮 English language support (multilingual)
- 🔮 Visual diagrams (Mermaid, ASCII art)
- 🔮 Multi-project analysis
- 🔮 PDF/HTML export
- 🔮 CI/CD pipeline integration

---

## Constraints & Limitations

### Technical Constraints
1. **File System Access**: Requires read/write access to project directory
2. **Network**: Can run offline (no external dependencies)
3. **Disk Space**: ~20 KB per project (minimal)
4. **Runtime**: Python 3.8+ or Node.js 14+ (depending on implementation)

### Business Constraints
1. **Support Scope**: Only covers common project types (95% coverage)
2. **Customization**: Basic CLAUDE.md generation (users can enhance)
3. **Maintenance**: Active support for 7 tech stacks
4. **Scalability**: Optimized for <10,000 file projects

### Design Constraints
1. **Backward Compatibility**: Must maintain v1.3.0 compatibility
2. **Optionality**: Hierarchical features must be opt-in
3. **Simplicity**: CLI should not exceed 6 main flags
4. **Documentation**: All features must be documented with examples

---

## Dependencies & Integrations

### External Dependencies
- None required (skill is self-contained)

### Internal Dependencies
- **nqdev-requirement-estimator** — For requirements estimation
- **nqdev-write-plan** — For planning integration

### Ecosystem Integrations
- **Claude Code** — Skill framework
- **Cowork** — Deployment platform
- **GitHub** — Version control (for .claude/ metadata)
- **CI/CD** — Optional integration for automated setup

---

## Risk Assessment

### Risk 1: User Confusion with Multiple Flags

**Probability**: Medium | **Impact**: Medium  
**Description**: Users confused by `--hierarchical-claude` vs `--sub-claude` vs `--no-hierarchical-claude`

**Mitigation**:
- ✅ Clear help text: `--sub-claude` is just a "shorthand"
- ✅ Examples for each scenario
- ✅ Explicit guidance: "Use --sub-claude for medium+ projects"

---

### Risk 2: Backward Compatibility Break

**Probability**: Low | **Impact**: Critical  
**Description**: Changes could break existing v1.3.0 projects

**Mitigation**:
- ✅ Hierarchical disabled by default
- ✅ Extensive testing on v1.3.0 projects
- ✅ Clear migration documentation
- ✅ Rollback procedure documented

---

### Risk 3: Scope Resolution Conflicts

**Probability**: Low | **Impact**: Medium  
**Description**: Conflicting rules in parent/child CLAUDE.md files

**Mitigation**:
- ✅ Documented merge strategy (most specific wins)
- ✅ Clear examples
- ✅ Validation tool to check for conflicts
- ✅ Decision tree in troubleshooting guide

---

### Risk 4: Performance on Large Projects

**Probability**: Medium | **Impact**: Low  
**Description**: 10,000+ file projects might be slow

**Mitigation**:
- ✅ Lazy-loading strategy planned for v1.5.0
- ✅ Performance monitoring from day 1
- ✅ Caching optimization
- ✅ User guidance: "For 10,000+ files, consider..."

---

## Competitive Analysis

### vs Manual CLAUDE.md Creation
| Aspect | nqdev-init-agents | Manual |
|--------|-------------------|--------|
| Setup Time | 1-5 min | 2-4 hours |
| Consistency | ✅ High | ❌ Low |
| Scalability | ✅ High | ❌ Low |
| Customization | ✅ Easy | ✅ Easy |

**Win**: nqdev-init-agents is 40-80x faster

---

### vs Generic Templates
| Aspect | nqdev-init-agents | Generic |
|--------|-------------------|---------|
| Project-Specific | ✅ Yes | ❌ No |
| Tech Stack Detection | ✅ Auto | ❌ Manual |
| Hierarchical Support | ✅ Yes | ❌ No |
| Maintenance | ✅ Active | ❌ Varies |

**Win**: nqdev-init-agents is more intelligent and adaptive

---

## Go-to-Market Strategy

### Phase 1: Early Adoption (August-September 2026)
- **Target**: Technical founders, engineering teams
- **Channel**: GitHub, technical blogs, nqdev community
- **Message**: "Setup AI coding standards in minutes, not hours"

### Phase 2: Mainstream (October-December 2026)
- **Target**: Growing startups, medium enterprises
- **Channel**: Tech conferences, YouTube tutorials
- **Message**: "Scale AI-assisted development across teams"

### Phase 3: Enterprise (2027)
- **Target**: Large enterprises, Fortune 500
- **Channel**: Enterprise sales, industry partnerships
- **Message**: "Governance-grade AI guidance for large organizations"

---

## Success Definition

### Shipped Successfully When:
- ✅ v1.4.0 released and documented
- ✅ 100 projects initialized in first month
- ✅ 4.0+ ⭐ user rating
- ✅ <1% error rate across common stacks
- ✅ All documented use cases working

### Long-Term Success (6 months):
- ✅ 500+ active projects
- ✅ 60%+ enable hierarchical mode
- ✅ Positive case studies from 3+ teams
- ✅ Merged into nqdev standard toolkit
- ✅ Planning v1.5.0 features

---

## Documentation Requirements

### User Documentation
- ✅ SKILL.md — Complete feature documentation
- ✅ README.md — Quick start guide
- ✅ CHANGELOG.md — Version history

### For This Release
- ✅ SPECS.md — Technical specification (GitHub Spec-Kit)
- ✅ PRD.md — Product requirements (this document)
- ✅ EDGE_CASES.md — Troubleshooting guide
- ✅ Examples for each use case

### Planned
- 📋 Video tutorial (setup walkthrough)
- 📋 Blog post (why you need AI standards)
- 📋 Case study (success story from real team)

---

## Approval

| Role | Name | Date | Approved? |
|------|------|------|-----------|
| Product Manager | QuyIT Platform | 2026-08-13 | ✅ Yes |
| Engineering Lead | — | — | ⏳ Pending |
| UX Lead | — | — | ⏳ Pending |
| Legal/Compliance | — | — | ⏳ Pending |

---

## Document History

| Version | Date | Author | Status |
|---------|------|--------|--------|
| 1.0 | 2026-08-13 | QuyIT Platform | ✅ Draft |
| — | — | — | — |

---

**Last Updated**: August 13, 2026  
**Next Review**: Before v1.5.0 planning (September 1, 2026)  
**Maintenance**: Quarterly review recommended
