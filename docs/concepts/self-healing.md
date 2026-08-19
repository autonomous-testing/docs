---
title: Self-Healing
description: "How Wopee.io self-healing works: accessibility-first locators with automatic fallback, a self-troubleshooting sub-agent, and per-project agent skills."
---

# Self-Healing (Wopee.io)

Self-healing is how Wopee.io keeps tests running when your UI changes. Instead of relying on stored selectors that break with every refactor, the agent reads your app's accessibility tree at run time, falls back through alternative locator strategies, troubleshoots stuck steps with a focused sub-agent, and records what it learns about your app in per-project skills.

## What this page covers

The mechanisms behind self-healing: how the agent locates elements, what happens when a step fails, and how the agent gets better at your app over time. For the full list of interaction tools and assertions, see [Tools & Assertions](tools-and-assertions.md).

---

## Accessibility tree first, not stored selectors

The agent does not replay a script of hard-coded selectors. On every step it takes a structured snapshot of the page's **accessibility tree**: the interactive elements with their roles, accessible names, and references the agent can act on.

Because the agent targets elements by role and name ("the **Checkout** button", "the **Email** field"), changes that preserve your app's semantics, such as restyled components, moved markup, or new CSS classes, do not break the step. The agent simply finds the same element in the fresh snapshot.

## Locator fallback, automatic

When the agent interacts with an element, it selects a locator strategy in this order:

1. **ARIA tree (preferred)** – Role/name-based locators from accessible markup. Stable and intent-focused.
2. **HTML attributes** – `data-testid` and other data-test IDs, element IDs, CSS/XPath.
3. **Visual location** – x, y position on screen. Last resort for canvas elements or icons without DOM hooks.

If the preferred strategy fails, the agent automatically tries the next one. The strategy that works is written into the generated test code, so the deterministic code you export uses the same locators the agent proved during the run.

!!! tip "Help the agent help you"

    Add `data-testid` (or similar data-test IDs) to key elements. When accessible markup is ambiguous, these give the fallback chain a stable second option before it has to resort to visual location.

## Self-troubleshooting sub-agent

When a step keeps failing, the agent does not blindly retry. It spawns a focused **troubleshooting sub-agent** against the same live browser session. The sub-agent examines the page with a different lens, a fresh accessibility snapshot plus browser devtools, and returns a compact diagnosis: what is actually on the page, what is blocking the step, and what to try instead.

The main agent uses that diagnosis to unstick the run. Only when troubleshooting cannot resolve the step does the agent escalate:

- **Human handoff** – The agent yields browser control to you with a reason and a suggested action (typical for CAPTCHA, MFA, or unknown credentials), then resumes autonomously once you have unblocked it.
- **Reported issue** – The step is reported as a finding with the evidence attached, instead of being silently skipped.

## Per-project agent skills

The agent maintains **skills** per project: notes about your app's flows, quirks, and patterns that it loads at the start of each run. After a run, it can write updates back, so the knowledge compounds and the agent gets better at your app over time.

Each project controls this with a skills mode:

| Mode            | Behavior                                                             |
| --------------- | -------------------------------------------------------------------- |
| **Off**         | The agent runs without project skills.                               |
| **Read-only**   | The agent loads existing skills but never modifies them.             |
| **Auto-update** | The agent loads skills and writes learned updates back after runs.   |

## Self-healing never changes a verdict

Self-healing applies to *locating and interacting* with elements. It does not apply to test verdicts. Defined assertions are never "healed": if an assertion fails, the step fails, and the result carries the evidence (screenshots and logs) so you can see exactly what happened.

## Related topics

- [Tools & Assertions](tools-and-assertions.md)
- [Analysis Process](analysis-process.md)
- [Project Context](../guides/project-context.md)
- [Getting Started with Wopee.io Agent testing](../ai-agent.md)
