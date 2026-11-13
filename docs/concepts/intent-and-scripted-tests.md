---
title: Intent-driven and Scripted Tests
description: "Intent-driven tests (description only) and scripted tests (saved steps) in Wopee.io: how each runs, when to use which and how to switch."
---

# Intent-driven and Scripted Tests

A Wopee.io test can be written in two ways. An **intent-driven test** says what the user wants and what must be true afterwards; the AI agent works out the clicks on every run. A **scripted test** has saved steps that the agent replays in order. The rule is short: **write the goal and the proof, and let the agent find the clicks. Save steps only when the path must not change.**

!!! info "For product owners and CTOs"

    Intent-driven tests survive UI changes such as a renamed button or a reordered form, because the agent finds the path again on each run. Scripted tests repeat the same path every time, which makes them predictable but more likely to break when the UI changes. Most teams write new coverage as intent tests and save steps only for stable regression flows.

## What this page covers

This page explains what each kind of test is and how their runs differ. It also covers when to use which, how to write an intent test that proves something, how to switch a test from one kind to the other in Commander, and the mistakes to avoid. For rules that every test in a project shares, see [Project Context](../guides/project-context.md).

Commander calls a test case a **scenario** and groups scenarios by user story. The paths below use the Analysis workspace.

---

## The difference is the steps

Commander has no "intent" or "scripted" switch. The difference is whether the test has steps:

| | Intent-driven test | Scripted test |
| --- | --- | --- |
| What it contains | A name and a description, no steps | A name, a description and saved steps |
| How you recognise it | The steps panel shows **No steps yet**; the scenario card shows no step count | The scenario card shows the step count after the status, for example `Passed · 6 steps` |
| What the agent does | Reads the name and description, plans, and finds every element on the live page | Follows the saved steps in order, starting from each step's recorded locator |
| Run dialog | Shows *This test doesn't have detailed steps yet. It will be executed by an AI agent that interprets the description and performs the test autonomously.* and the **Save steps from this run** switch | Plain **Run** |

## How each one runs

### Intent-driven test

The agent receives the test's name and description and is told to carry out that test. It plans first:

1. It finds the main goal in the name and description.
2. It looks at the screen.
3. It decides which preparation the goal needs, such as signing in.
4. It postpones actions that change the screen for good (signing in, submitting, leaving the page) until it has checked everything that needs the current screen.

Every element is found on the page as it is now, so a renamed or moved button does not break the test.

An intent test must still prove its result. If the agent tries to finish after interacting with the app without checking anything, the run is sent back up to two times and asked to assert the test's acceptance criteria. A pass with real interactions and no passing assertion is flagged by [verdict integrity](verdict-integrity.md). A test is exempt only if its name starts with Open, Go to, Navigate to, Setup, Log in or Sign in and its name and description ask for no check.

### Scripted test

The agent is told to follow the saved steps strictly and in order. The description still goes along as background.

- Saved steps keep the locator that worked on the recorded run. The agent tries it first.
- If the recorded locator no longer matches, the fallback described in [Self-Healing](self-healing.md) applies, and the repair is listed under **Locator recoveries** in the report. A heal may change how the element is found, but never which element: a step recorded on **Finish** is never moved to **Continue**.
- If the agent still cannot find a step's target after repeated tries, it abandons that step and either moves on or troubleshoots.
- Some locators are recorded as plain words instead of a real selector, for example "shopping cart container". These are not run as selectors. The agent matches such a step by intent, so the step is not deterministic.

Integrity checks also confirm that every saved step and every saved assertion actually ran.

!!! note "Scripted is not the same as no AI"

    A scripted test is still run by the AI agent; it follows the saved steps instead of planning its own. For the Playwright code Wopee.io can generate from a run, see [Tools & Assertions](tools-and-assertions.md).

## Pros and cons

| | Intent-driven | Scripted |
| --- | --- | --- |
| UI changes (renamed button, new layout) | Adapts | Heals the locator, or fails the step and reports it |
| Same path every run | No, the route can differ between runs | Yes |
| Values checked during the recorded run | Read fresh each run | A value checked as a literal is saved as that literal, and the replay fails when it changes. A change checked against a starting value (the balance decreased by the amount withdrawn, one more row than before) is saved as a relative check and replays |
| Writing effort | A few lines of text | Recorded from a passing run or generated, then maintained |
| Main risk | The agent reaches the goal another way than you meant (a coupon, a guest checkout) unless MUST NOT rules it out | Breaks when the UI changes; an edited description does not update the steps |

## When to use which

Use an **intent-driven test** when:

- you are adding new coverage, or the app still changes often;
- the outcome is stable but the exact clicks may vary;
- the test reads values that differ between runs, such as balances, stock or dates, and you want it to adapt to them.

Use a **scripted test** when:

- the flow is stable and you want the same path every run, for example a regression suite gating a release;
- the exact order of the interaction is what you are testing;
- the values it checks are stable, or are checked relative to a starting value.

Apps whose element IDs are generated anew on every page load are hard to replay. Prove one replay before you rely on saved steps there.

---

## Write a good intent test

Put the whole test in the **Description** field and leave the steps empty. Use these four labels, in capitals, each at the start of its own line:

```text
GOAL: <who the user is and what they want to achieve, in one sentence>
PASSES WHEN:
- <one observable fact, with its expected value written out>
- <another observable fact>
MUST NOT:
- <what makes the test fail even if the goal is reached>
DATA: <which account, items and values to use; ${VARIABLES} for anything secret or changing>
```

Leave out clicks, element IDs, CSS selectors and lists of pages to open. If you name a button, field or menu, use its visible label and state it as a fact.

A filled example:

```text
GOAL: A signed-in customer buys two units of one in-stock product and pays by card.
PASSES WHEN:
- The cart shows quantity 2 and a subtotal of 2 × the product's listed price.
- Checkout shows a total equal to subtotal + shipping − discounts, to the cent.
- A confirmation page with an order number is shown.
- The order appears once in My orders with status "Paid".
MUST NOT:
- An error message appears at any point.
- The order is placed as a guest or with a promo code.
DATA: Sign in with ${TESTING_USERNAME} and ${TESTING_PASSWORD}. Pay with the test card in ${TEST_CARD_NUMBER}.
```

!!! tip "The labels are a writing convention"

    Wopee.io does not parse GOAL, PASSES WHEN, MUST NOT or DATA as fields; the agent reads them as text. Commander does display them well: an all-capital label at the start of a line, ending in a colon, starts its own section in the description, while `Goal:` in mixed case does not. Put GOAL first, because the scenario list shows the first two lines as a preview.

### What makes an intent test strong

- **One behaviour per test.** One goal, one set of outcomes.
- **A value you can check.** "Checkout works" proves nothing. "The total is subtotal + shipping, to the cent" does. Every PASSES WHEN line names one fact and its expected value.
- **A durable outcome.** Check what stays: a record in a list, its status, a URL or the order history. Do not rely on a toast, a spinner or an e-mail.
- **Computed expectations.** For a change, say how the new value relates to the starting one: "the balance decreased by the amount withdrawn", "the list has one more row than before". The agent reads the starting value, then checks the result against it.
- **Contains, not equals, for text that changes.** Order numbers, dates and generated names change on every run. Check that they exist, or that they contain a fixed part.
- **Its own data.** A test creates the records it needs and does not depend on another test. Give new records a unique suffix, such as a timestamp.
- **Explicit comparisons and counts.** Words such as *matches*, *equals*, *increased* or *changed* tell the agent a comparison is needed, and it checks that it made one. An explicit count, such as "add 3 different products", is checked too.
- **Something the agent can see.** The agent judges the page. It cannot read page source or invisible metadata. It knows the date and time when the run starts, but not how much time has passed, so "after 5 minutes" does not work as a rule.

### Variables

Write secrets and changing values as `${NAME}`. The agent receives the names of your variables, never their values. Credentials arrive as `${TESTING_USERNAME}` and `${TESTING_PASSWORD}`.

The agent fills in `${NAME}` when it types, selects, opens a URL or checks text with a text assertion. It does not fill it in inside a visual check or in its own reasoning. If the agent must judge a value by eye, write the value out in the description or the project context.

Create every variable before the first run:

- **For one analysis:** in **Variables & Knowledge**, click **Edit** next to the variables and use **Add variable**. `TESTING_USERNAME` and `TESTING_PASSWORD` are already listed there.
- **For the whole project:** go to **More** › **Settings** › **Environment Variables**. These values are defaults; a variable with the same name in an analysis overrides them.

A variable that does not exist is not filled in.

---

## Run an intent test

1. In **Analysis**, select the scenario and click its run control (**Run scenario**). You can also click **Run** inside the test-case dialog.
2. The **Run test case** dialog shows that the test has no detailed steps yet.
3. To keep the test intent-driven, switch **Save steps from this run** off. It is on by default and turns back on every time the dialog opens.
4. **Interactive mode** is on when you run from the scenario card and off when you run from inside the test-case dialog. Switch it off for a headless run. *Watch the agent run in real time. Send instructions mid-test or take over the browser when needed.*

!!! warning "Runs that save steps or skip intent tests"

    - The **Run all** link in an analysis e-mail opens a **Run all N tests?** confirmation with no switch. It saves steps for every test that has none, so a test that passes in that run becomes scripted. To keep it intent-driven, delete its steps afterwards (see [Switch a scripted test back to intent](#switch-a-scripted-test-back-to-intent)).
    - A bulk run from the **Scenarios** tab skips tests without steps: the dialog marks them **(no steps)** and says they will be skipped.

!!! tip "Run intent tests repeatedly or on a schedule"

    Put them in a **Test Plan**. A plan's run starts without a Save steps choice and saves no steps, so the tests stay intent-driven.

The [project context](../guides/project-context.md) shapes how tests are written. It cannot stop steps from being saved. Switch **Save steps from this run** off, or run the tests from a Test Plan.

---

## Switch an intent test to scripted

The actions below are in the test-case dialog. To open it, click a step of the scenario's run, or use **Open in Analysis** from the **Scenarios** tab.

There are three ways to give a test steps.

**Save the steps of a passing run.** Run the test with **Save steps from this run** switched on. *If the run succeeds, the recorded interactions and assertions will be saved as the test's detailed steps. Future runs will replay these steps directly — more predictable, and less adaptive to app changes.* No steps are saved from a run that is Failed or Incomplete, so a failed attempt is never saved. A passing run can still take a route you did not intend. Check the path of the first passing run before you keep its steps.

**Generate the steps.** In the test-case dialog, click **Generate steps**. The button is shown only while the test has no steps. The steps are written from the name, the description and the analysis screenshots, without a run. Generating steps also:

- deletes the test's earlier runs and its generated Playwright code;
- rewrites the description to remove a step-by-step section (for example `STEPS:`). The goal, test data and expected results stay.

When you generate steps for several selected tests at once, Commander asks first: *This will overwrite the existing data in the selected test cases!* The **Assistant** can also generate steps for a test (**Generate steps for** that test).

**Add them by hand.** In the test-case dialog, click **Edit**, then **Add test step**.

## Switch a scripted test back to intent

1. Open the test-case dialog.
2. Open the **⋮** menu and, under **Test case**, choose **Delete all steps**.
3. Confirm **Delete all steps?** with **Delete**. *This removes every step from this test case. This cannot be undone.*
4. Check that the description still says everything the test needs (GOAL, PASSES WHEN, MUST NOT, DATA). If the steps carried the knowledge, write it into the description now.
5. On the next run, switch **Save steps from this run** off.

## Change what a scripted test checks

Editing the description of a test that has steps does not change its steps. The next run still replays the old steps. To make the steps match the new description, do one of the following:

- Delete all steps (as above), then click **Generate steps** or run the test once with **Save steps from this run** on.
- Delete all steps and keep the test intent-driven.
- Apply the Assistant's **Generate steps for** that test.

The same applies to changes made through the **Assistant**. A proposed change to a test says whether it removes the recorded steps or keeps them out of date, and offers **Generate steps for** that test.

When you generate scenarios again, keep **Keep existing scenarios** on. With it off, the scenarios in scope are replaced, and their steps and run history are dropped.

---

## Common mistakes

| Mistake | What happens | Fix |
| --- | --- | --- |
| A vague goal ("Test checkout") | The agent passes on anything | Add PASSES WHEN lines with values |
| No MUST NOT | The agent reaches the goal another way: a coupon, a guest checkout, Cancel instead of Confirm | Name the routes and side effects that count as failure, and read the path the agent took on the first runs |
| A numbered click list in the description | The test breaks on the next UI change, like a script | Keep the goal and the proof; drop the clicks |
| An over-strict PASSES WHEN (an exact label, a value that depends on tax or date) | A correct app fails | Check presence or a stable part of the value, or compute the value |
| Tests that share one record | One test's data breaks another | Each test creates its own data with a unique suffix |
| Leaving **Save steps from this run** on by habit | The test turns scripted after its first pass | Switch it off for tests that should stay intent-driven |
| Saving steps from a run that checked a changing value as a literal | Replays fail on the value saved from the recorded run | State the expectation relative to a starting value, or keep the test intent-driven |
| Editing a scripted test's description only | The old steps still run | Delete the steps, then generate them again or keep the test intent-driven |
| Repeating shared rules in every test | Contradictions between tests and slower runs | Put shared rules in the [project context](../guides/project-context.md) once |

## Related topics

- [Project Context](../guides/project-context.md)
- [Verdict Integrity](verdict-integrity.md)
- [Self-Healing](self-healing.md)
- [Tools & Assertions](tools-and-assertions.md)
- [Prompting Guidelines](prompting-guidelines.md)
- [Getting Started with Wopee.io Agent testing](../ai-agent.md)
