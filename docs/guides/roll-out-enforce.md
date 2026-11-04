---
title: Roll out Enforce in 2 weeks
description: "A two-week plan to move a Wopee.io project from Report only to Enforce: read the flagged passes, switch on Enforce for one project, resolve each Incomplete and widen to more projects."
---

# Roll out Enforce in 2 weeks

[Verdict integrity](../concepts/verdict-integrity.md) checks every claimed pass against the record of the run. This guide takes you from watching those checks to letting them decide what counts as green: one week of reading, one week of Enforce on a single project, then the rest of your projects. Verdict integrity is an **experimental preview**.

## Before you start

- **Report only** is on by default for every agent project. It never changes a stored result: verdicts, counts and pass rates stay exactly as the agent reported them.
- **Enforce** turns a pass the evidence does not support into **Incomplete**, so an unproven pass can never count as green.
- Only project admins can change the mode, under **More › Settings › Verdict**. The change applies to future runs.

## Week 1: Report only

Run your tests as usual and read what the integrity checks would have done.

1. Open the **Analysis**, **Scenarios** or **Runs** tab of a project and look for green dots with an **amber ring**. Each one is a pass the integrity checks dispute. Hover it to see which check disagreed.
2. Open the run report of a flagged run and read its **Verdict Integrity** section. **Gates triggered** names the integrity check that fired; **Shadow verdict** is the verdict the evidence supports.
3. For each flagged test, decide whether the test should prove what the agent reported. Usually it should: add the missing check now (see [Resolve each Incomplete](#resolve-each-incomplete)) and the ring goes away on the next run.
4. Note which project people rely on most, for example the one whose results gate a release or a CI pipeline. That is your first Enforce project.

By the end of the week you know how many of your passes are proven, and which tests need another check.

## Week 2: Enforce on one project

1. As a project admin, open the project, go to **More › Settings › Verdict**, choose **Enforce** and save.
2. Run the project's tests or wait for the next scheduled run. Every pass that the evidence does not support is now stored as **Incomplete** (amber), and Incomplete counts with the failures in totals, pass rates and filters.
3. Work through each Incomplete as described below. Expect the list to shrink run by run as the tests gain the checks they were missing.

If you need to step back, switch the project to **Report only**. Future runs follow the new setting.

## Resolve each Incomplete

An Incomplete means the run did not prove its result. It does not mean your app is broken.

1. Open the run report and read the **Verdict Integrity** section. It names what the run did not prove, for example a value the report quotes that no assertion recorded.
2. Add the missing check to the test: an assertion that reads that value or confirms that step on the page. Check every value the result depends on, not only the final one (for example, the item price and the tax, not only the total).
3. Run the test again. With the check in place, the run proves its result and goes green, with Enforce still on.
4. If the report lists a test-environment problem instead, such as a lost browser connection or an expired login session, run the test again. It says nothing about your app.

The video on the [Verdict Integrity](../concepts/verdict-integrity.md) page shows this loop end to end: a pass the agent claimed becomes Incomplete under Enforce, checks for the reported values are added, and the rerun goes green with Enforce still on.

## Widen to more projects

Move the next project to Enforce when the first one is settled:

- new Incompletes on the first project are rare, and each one has a clear cause you can act on;
- the team reads an amber result as "add a check", not as "the app is broken";
- the next project has had at least a week in Report only, so its flagged passes are already known.

Go one project at a time, starting with the projects whose results gate releases or CI pipelines. Projects that keep Report only lose nothing: their reports still carry the Verdict Integrity section and the amber rings.

## Related topics

- [Verdict Integrity](../concepts/verdict-integrity.md)
- [Tools & Assertions](../concepts/tools-and-assertions.md)
- [Getting Started with Wopee.io Agent testing](../ai-agent.md)
