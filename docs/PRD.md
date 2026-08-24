# {{PROJECT_NAME}} — Product Requirements Document

<!-- Written for someone who already knows what a PRD is. No section explains
     itself. Every heading is here because its absence has cost a project
     something. Delete a section only when you can say why it does not apply. -->

**Status:** draft · in review · **approved** — <!-- one of the three -->
**Owner:** {{OWNER}} · **Last updated:** <!-- YYYY-MM-DD, on every change -->
**Approved by:** <!-- name + date. An unapproved PRD is a proposal. -->

---

## 1. Problem

<!-- The problem, not the solution. Evidence, not conviction: what was
     observed, measured, or heard, and from whom. If the only evidence is
     "it seems obvious", say so — an assumption named is cheap, an assumption
     hidden is not. -->

**Evidence:** <!-- data, interviews, support tickets, existing workaround -->
**Cost of doing nothing:** <!-- what keeps happening if this ships never -->

## 2. Users and jobs to be done

| Segment | Job to be done | Today's workaround | Frequency |
|---|---|---|---|
| | | | |

**Primary segment:** <!-- one. Serving two primaries means serving neither. -->

## 3. Outcomes

<!-- Outcomes, not output. Each metric needs a baseline: a target without a
     baseline cannot be evaluated, only argued about. -->

| Metric | Baseline | Target | By when | How measured |
|---|---|---|---|---|
| | | | | |

**Counter-metric:** <!-- what must NOT degrade while we chase the above -->

## 4. Non-goals

<!-- The section that saves the most time later. What this product will not
     do, and what someone will reasonably ask for that the answer is no. -->

- 

## 5. Scope

**In, v1:**
- 

**Out, and why:**
| Cut | Reason | Revisit when |
|---|---|---|
| | | |

## 6. Primary journey

<!-- The one path that must work. Numbered steps, from entry point to the
     moment the user got what they came for. Everything else is secondary. -->

1. 

**Entry point:** <!-- how they arrive. A journey with no entry point is a demo. -->

## 7. Functional requirements

<!-- Numbered, testable, each traceable to an outcome in §3. FR-n survives
     into the acceptance criteria of a story — same wording, so a reviewer can
     match them without interpreting. -->

| # | Requirement | Serves outcome | Priority |
|---|---|---|---|
| FR-1 | | | P1 |

## 8. Non-functional requirements

| Attribute | Requirement | Verified how |
|---|---|---|
| Performance | | |
| Accessibility | | |
| Security | | |
| Personal data | <!-- what is collected, why, retention, deletion --> | |
| Availability | | |

<!-- Personal data is filled in before the first line of code that stores it,
     not before launch. Retrofitting deletion is a migration and a rewrite. -->

## 9. Dependencies and risks

| Risk / dependency | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| | | | | |

## 10. Assumptions to validate

<!-- Each one is a bet. Name how it gets tested and by when — an assumption
     with no test date is a belief. -->

| Assumption | If false | Test | By when |
|---|---|---|---|
| | | | |

## 11. Open decisions

<!-- 🔴 Every row needs an owner AND a date. A decision log without dates is a
     list of regrets. -->

| # | Decision | Options | Owner | Needed by |
|---|---|---|---|---|
| D-1 | | | | |

## 12. Launch criteria

<!-- Go / no-go. Binary, checkable by someone who was not in the room. -->

- [ ] 

## 13. Decision history

<!-- Appended, never rewritten. What changed, why, and what it invalidated. -->

| Date | Decision | Rationale | Invalidates |
|---|---|---|---|
| | | | |

---

**Downstream:** stories and business rules in [`specification.md`](specification.md) ·
technical shape in [`ARCHITECTURE.md`](ARCHITECTURE.md) ·
data structure in [`SCHEMA.md`](SCHEMA.md)
