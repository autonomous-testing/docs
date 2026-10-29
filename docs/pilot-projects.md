---
title: Pilot Projects
description: "Wopee.io pilot project: 8 weeks, up to 10 critical flows, fixed price. What we deliver, what we need from your team, how we measure, and what happens after."
---

# Pilot Projects (Wopee.io)

A pilot project is an 8-week, fixed-scope engagement to prove that autonomous testing works on your application, with your team, before you commit to a contract. It is priced, scoped and measured in advance, and it ends with a decision.

## What this page covers

Exactly what a pilot includes, what it costs, what it asks of your team, how success is measured, and what happens when it ends. If you can answer every question on this page for your own organization, you are ready for the [first call](https://wopee.io/book-demo).

---

## The offer

| Item | Detail |
| ---- | ------ |
| **Duration** | 8 weeks, run as 8 weekly sprints |
| **Price** | **Fixed.** Agreed before Sprint 1 and credited in full against your first annual contract if you continue. Everything else on this page is fixed too; only the amount is discussed on the call |
| **Scope** | Up to **10 critical user flows** of one web application, agreed before Sprint 1. Flows can be exchanged one for one during the pilot |
| **We deliver** | 5 tests built by our engineers, weekly test runs, a live stability dashboard, a benefit assessment against your baseline, a viability report, and a closure presentation for your stakeholders |
| **You deliver** | Around 20 further tests built by your team with our coaching |
| **Decision** | A named decision maker on your side commits to a go/no-go decision at the end of Sprint 8 |
| **After the pilot** | You own every test. Tests live in a Git repository you can open, diff and roll back |

**How the credit works.** If you continue after the pilot, the full pilot fee is deducted from your first year. You do not pay for the evaluation and then again for the contract.

---

## What we need from your team

This is the part most vendors leave out. A pilot only works if your team has the capacity to take part, so we say the numbers up front.

| Role | Commitment |
| ---- | ---------- |
| **QA or test lead** (your pilot owner) | Named before kickoff. Attends the weekly review, selects scope, owns the go/no-go decision or knows who does |
| **Testing team** | **3 to 5 person-days per sprint** across the team: building tests with our coaching, reviewing runs, giving feedback. Roughly 20 to 35 person-days over the 8 weeks |
| **SRE / DevOps** | Environment access and connectivity in Sprint 1, then on request |
| **Stakeholders** | Attend the Sprint 8 demo and decision |

**Before kickoff you need:**

- A non-production environment with working test accounts and stable test data
- Network access for our agents to reach that environment (VPN, allow-list, or a jump host; we will agree the route in the first call)
- The initial 5 test cases you want covered first
- A named decision maker and a date for the Sprint 8 decision

!!! note "If the numbers above do not fit"

    Say so in the first call. A pilot with a team that cannot spare the time stalls in Sprint 3, and nobody benefits from that. It is better to schedule a pilot for a quarter when the capacity exists.

---

## Week by week

| Sprint | Focus | Outcome |
| ------ | ----- | ------- |
| 1 | Training, environment access, connectivity check, scope confirmed, **baseline measured** | Everyone can run a test; the numbers we will compare against are recorded |
| 2 | First working tests: login and prerequisites, first analysis cycle | At least one runnable critical flow per area |
| 3 | Optimization: ignore regions, stabilization, advanced training if wanted | Runs are repeatable |
| 4 to 5 | Expand coverage, 10 to 15 test cases per sprint | Agreed scope covered |
| 6 to 7 | Stabilization: run, monitor, address flakiness and maintenance | Suite is trustworthy |
| 8 | Lessons-learned workshop, stakeholder demo, **go/no-go decision** | Viability report and a decision |

Sprint 1 and Sprint 8 can be on site or remote. Everything between is remote.

---

## How we measure

Every pilot records a **baseline in Sprint 1** and compares against it in Sprint 8. Success criteria are agreed in writing before work starts, not interpreted afterwards.

Typical criteria, adjusted to your context:

- Coverage of the agreed critical flows by automated tests
- Time to create a test scenario, before versus with Wopee.io
- Regression cycle time for the agreed scope
- Test stability: share of runs that fail for non-product reasons
- Team adoption: how many of your team can run and review tests unaided

We report each of these against your own baseline. We do not quote percentages from other customers as your expected result, because every application and team is different.

---

## Security and data

- Your data is stored in the EU by default. A custom region or full on-premise deployment is available.
- **We never train models on your code, test data, or screenshots.**
- Data is deleted within 30 days of the pilot ending.
- Under the EU AI Act, Wopee.io is the provider and you are the deployer. The system does not self-learn or modify model weights from your inputs.
- You can bring your own LLM account (Azure OpenAI, Google Vertex AI, Anthropic, or OpenAI) so that model usage stays under your contract.
- SOC 2 and ISO 27001 are on our roadmap. We are happy to complete your supplier security questionnaire before the pilot starts.

---

## What a pilot does not do

- It does not replace your QA team. It gives them a suite that keeps working and coaching on how to run it.
- It does not promise a defect count. Our agents build and stabilize a regression suite; how many bugs that suite surfaces depends on your application.
- It does not cover mobile native apps, desktop applications, or APIs on their own. The scope is one web application.
- It does not run indefinitely. Sprint 8 ends with a decision either way.

---

## What happens after

At the end of Sprint 8 you have a viability report, a working suite, and a decision to make.

- **Continue:** the pilot fee is credited in full against your first annual contract, the suite grows from the pilot's foundation, and your team keeps our support.
- **Stop:** the tests are yours. We revoke our access and delete your data within 30 days. Nothing runs on our side afterwards.

Either way, the tests are yours. If they are handed over and nobody maintains them, they will decay like any other test suite, which is exactly the outcome the Sprint 8 decision exists to avoid.

---

## Getting started

The first call is 30 minutes. It is not a product demo. We go through the questions on this page for your organization:

1. Which application and which flows
2. Who your pilot owner and decision maker are
3. Whether the team capacity exists in the coming quarter
4. Environment access and any security review you need from us

If it fits, we send you the pilot charter pre-filled from that conversation.

!!! success "Start the conversation"

    [:octicons-arrow-right-24: **Book the first call**](https://wopee.io/book-demo){ .md-button .md-button--primary style="display: block; margin: 0 auto; text-align: center;" }

    _30 minutes, with the founders. Bring the questions above and we will answer them plainly._

## Related topics

- [Getting Started with Wopee.io Agent testing](ai-agent.md)
- [Tools & Assertions](concepts/tools-and-assertions.md)
- [Self-Healing](concepts/self-healing.md)
- [Project Context](guides/project-context.md)
