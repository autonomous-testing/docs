---
title: Read your first results
description: "Tell a real bug in your app from a test problem or a run with no result: the three kinds of red, how to confirm a bug, what to fix and re-run, Passed, Failed, Incomplete and the amber ring, why the first board is red, and green tests that only checked the login page."
type: How-to
updated: 16 November 2026
---

# Read your first results

Your first analysis has run its first tests, and some of them are red. A red test can mean three different things, and each needs a different next step. This page shows how to tell them apart from the run's report, and why a green result is not always good news.

!!! info "For product owners and CTOs"

    A red first board is normal. The agent runs the tests most likely to find a bug first, so a red result often means it found something worth a look. Count only the red results you have confirmed as real bugs. A test problem or a run with no result says nothing about your app.

## Three kinds of red { #three-kinds-of-red }

_Also called: is it a real bug, false failure, false positive, failed test, why did my test fail._

Open the red test and click **Report**. The report tells you which of three kinds it is:

| Kind                       | What happened                                                                                                        | How the report shows it                                                                                                                         | Next step                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **A real bug in your app** | The app did something wrong. Running the test again fails the same way.                                              | **Issues Encountered** describes what the app did wrong, or a step marked ❌ shows the value the app should have shown and the one it showed.    | [Confirm it by hand](#real-bug), then report it to your team.               |
| **A test problem**         | The test was wrong: it looked for something that isn't there, it needed data it didn't have, or it couldn't sign in. | The verdict is **Failed**, but **Issues Encountered** says _None observed_ or describes the test rather than the app.                           | [Fix the test or the project context](#test-problem), then re-run the test. |
| **No result**              | The run never got far enough to judge your app: the app did not load, the sign-in was rejected or the run stopped.   | The verdict is **Incomplete**, the run is **Stopped**, or a message names the cause, such as _"Starting URL unreachable."_ or _"Login failed."_ | [Fix access](#no-result), then re-run the test.                             |

Wopee.io sorts finished runs the same way internally: a failure that names an application defect, a failure whose report names none, and a run that never reached a verdict about the app.

## A real bug { #real-bug }

_Also called: defect, the agent found a bug, possible issue, finding._

Signs that the red test found a real bug:

- **Issues Encountered** describes something the app did wrong. This section lists defects in the app only. Problems with the test itself, such as a locator that did not match, are listed apart.
- A step is marked ❌ and its **Expected Outcome** names a concrete value, such as a total, a status or a message, that the app did not show.
- The screenshot of that step under **Steps** shows the wrong value or the wrong page.

Confirm it by hand before you report it:

1. Open your app in your own browser, signed in as the same test user.
2. Repeat the steps from the report, with the same data.
3. Compare what you see with the step's **Expected Outcome**.

If you see the same problem, it is a real bug. Report it to your team with the run's link, the failed step and its screenshot. **Do not re-run the test to make it green**: it fails the same way until the bug is fixed. Re-run it after the fix to confirm.

If the app behaves correctly when you try it, or the expected value was wrong, it is a [test problem](#test-problem).

## A test problem { #test-problem }

_Also called: the test is wrong, flaky test, bad locator, wrong expectation, missing test data._

The app is fine; the test needs a fix. Typical causes:

- **A guessed expectation.** The test expects a text the app never shows. In the test's steps, such a step can carry the mark _"The crawl never saw this expected text on the page. It may be guessed: check it before trusting a failure."_
- **Missing test data.** The test needs a product, a customer or a file that does not exist in your test environment.
- **The sign-in.** The test stopped at the sign-in page or typed `${TESTING_USERNAME}` into it. See [Test an app behind a login](test-behind-a-login.md#placeholder-typed-literally).
- **A rule the agent did not know.** The test treats intended behaviour as a bug. See [It is by design](#by-design).

Fix the cause, then **re-run the test**. You don't need a new analysis: it explores the whole app again, and on the free plan it costs far more steps than a re-run.

- To change one test, open it, click **Edit** and correct its description or its steps. For how to write a description the agent can check, see [Intent-driven and Scripted Tests](../concepts/intent-and-scripted-tests.md).
- To change every test, add the rule or the test data to the [project context](../guides/project-context.md). Runs that start after you save it use the new text.

### It is by design { #by-design }

When the app works as intended but the test calls it a bug, tell the agent once. Add a line to the **By design (not a bug)** section of the [project context](../guides/project-context.md#optional-sections), for example: _"Prices on the product list are rounded; the cart shows the exact price."_ Then edit the test or re-run it.

## No result { #no-result }

_Also called: Incomplete, Stopped, the run never started, app not reachable, login failed, no verdict._

The run did not reach a verdict about your app. It says nothing about whether your app works, so there is nothing to confirm or report. Common causes and where to fix them:

- **The app did not load for the agent.** The message reads _"Starting URL unreachable."_ The tests run in the cloud, so the app must be reachable from the internet. See [Can the agent reach your app?](https://docs.wopee.io/guides/test-localhost/).
- **The sign-in was rejected or never happened.** The message reads _"Login failed."_, or every test stops at the sign-in page. See [Test an app behind a login](test-behind-a-login.md).
- **The run stopped.** It was cancelled, it ran out of time or the test browser was lost. The report lists browser and runner problems in a separate **Test environment (not the application)** section. Re-run the test.
- **The run could not prove its result.** The verdict is **Incomplete**. See [Incomplete and the amber ring](#incomplete-and-amber).

For the exact messages Commander shows and what each one means, see [Commander troubleshooting](https://docs.wopee.io/troubleshooting/commander/).

## Incomplete and the amber ring { #incomplete-and-amber }

_Also called: verdict labels, status colours, amber dot, orange, yellow, verdict gate disagreed, shadow verdict._

Every test shows a coloured dot. Hover it for the label.

| What you see                 | Label in the tooltip                   | What it means                                                                                                                                                         |
| ---------------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Green dot                    | _Test passed_                          | The run checked what the test asks for and found it.                                                                                                                  |
| Red dot                      | _Test failed_                          | The run found the app not behaving as the test expects. Read the report: it is a [real bug](#real-bug) or a [test problem](#test-problem).                            |
| Red dot                      | _Execution stopped_                    | The run was stopped before it reached a verdict. It is [no result](#no-result), not a failure.                                                                        |
| Steady amber dot             | _Test incomplete_                      | The run did not prove its result, or could not finish. It is not a bug in your app.                                                                                   |
| Green dot with an amber ring | _Test passed · verdict gate disagreed_ | The agent reported a pass, but an evidence check found that something was not proven. The tooltip names the check, for example _Verdict gate disagreed: fabrication_. |
| Blinking dot                 | _Queued_ or _Execution running_        | The test is still waiting or running.                                                                                                                                 |
| Grey dot                     | _Not run_                              | The test has not run yet.                                                                                                                                             |

The analysis overview counts the same way: **Passed**, **Incomplete**, **Failed**, **Running / queued** and **Not run**. Incomplete is never counted as a pass.

**The verdict gate** is a set of evidence checks that runs after every test. It compares the agent's verdict with what the run really recorded: no proof, no pass. The tooltip and the report name a check by a short code. In plain words:

| Code in the tooltip                                        | What the check found                                            |
| ---------------------------------------------------------- | --------------------------------------------------------------- |
| `fabrication`                                              | The report quotes a value that no check in the run recorded.    |
| `evidence-floor`                                           | The run clicked and typed but verified nothing.                 |
| `defined-step-completeness`, `defined-assert-completeness` | A step or a check the test defines did not happen.              |
| `undelivered-input`                                        | Something the agent typed or pressed never reached the page.    |
| `unsupported-failure`                                      | The run reported a failure that nothing in its record supports. |

What the gate does depends on the project's mode, under **More** › **Settings** › **Verdict**:

- **Report only** (the default): the verdict stays as the agent reported it. A disputed pass gets the amber ring, and the report gets a **Verdict Integrity** section.
- **Enforce**: a disputed pass becomes **Incomplete**, and a failure nothing supports becomes **Incomplete** too.

To clear an amber ring or an Incomplete, open the report's **Verdict Integrity** section, add the check the test is missing (for example, assert the value the report quotes), and re-run the test. More on the checks and the two modes: [Verdict Integrity](../concepts/verdict-integrity.md).

## Why the first board is red { #why-the-first-board-is-red }

_Also called: all my tests failed, mostly red, only 4 tests ran, the rest are not run._

At the end of the first analysis, the agent picks up to 3 of the tests it wrote to run straight away. It picks the ones most likely to catch a bug: first every test that reproduces a problem it saw while exploring your app, then the main flows. One main flow that worked during exploration runs on top of them. So up to 4 tests run, and the rest wait under **NOT RUN**.

A red first board therefore often means the agent saw something odd while exploring, and these tests check it. [Read each red result](#three-kinds-of-red) before you decide anything about your app.

To run the tests that are waiting, run them one by one, or select several and run them together. On the free plan, every run counts against your steps; only the first analysis and the tests it starts are free.

## Green tests on the login page { #green-on-the-login-page }

_Also called: all green but nothing tested, the tests only check the login, shallow tests, the agent stayed on public pages._

When the agent cannot sign in, it explores only the pages a visitor can see. The analysis still counts as passed, because the agent explored and wrote tests. The tests it wrote are about the sign-in page: the form is shown, a wrong password is rejected, the "Forgot password" link works. They pass.

**Green here does not mean your app is covered.** Check the names of the tests and the **Application description** of the analysis. If they mention only the sign-in page and public pages, the agent never got in.

To fix it, [add a test account](test-behind-a-login.md#add-a-test-account) and [start a new analysis](test-behind-a-login.md#after-you-add-it), so the agent explores the pages behind the login and writes tests for them.

## Related topics

- [Test an app behind a login](test-behind-a-login.md)
- [Verdict Integrity](../concepts/verdict-integrity.md)
- [Roll out Enforce in 2 weeks](../guides/roll-out-enforce.md)
- [Intent-driven and Scripted Tests](../concepts/intent-and-scripted-tests.md)
- [Project context](../guides/project-context.md)
