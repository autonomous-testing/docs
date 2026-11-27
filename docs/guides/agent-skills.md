---
title: "Agent Skills: good practices"
description: "Choose the right Wopee.io Agent Skills mode and Run Queue per project stage, write and curate SKILL.md files, review the agent's commits in Git, measure whether skills help, and fix common problems."
type: How-to
updated: 27 November 2026
---

# Agent Skills: good practices

This guide helps you get value from Agent Skills without letting them quietly make results worse. It covers which mode to use when, how to combine it with the Run Queue, how to write and review skills, how to measure their effect, and what to do when something goes wrong. For how skills and the Run Queue work, see [Agent Skills and Run Queue](../concepts/agent-skills.md).

!!! info "For product owners and CTOs"

    Skills help most when they are short, written or reviewed by people, and limited to what the agent cannot see on the page. Knowledge the agent writes for itself can be wrong, and one wrong skill affects every later run. Treat **Auto-update** as a supervised learning phase, use **Read-only** for runs whose results you rely on, and check with a simple comparison that the skills actually help.

## The short version

1. Start with **Off** and note how your tests do without skills.
2. Write two or three skills by hand for the things the agent gets wrong. Turn on **Read-only**.
3. If you want the agent to learn, run one batch with **Auto-update**, **Sequential** and **Stop queue on failure**. Switch back to **Read-only**, then review the batch's commits.
4. Run regression and release checks on **Read-only**.
5. Compare **Off** and **Read-only** on the same tests from time to time. Keep only skills that help.

---

## Choose a mode for each stage

| Stage | Agent Skills | Run Queue | Stop queue on failure |
| --- | --- | --- | --- |
| New project, first runs | **Off** for a baseline, then **Read-only** with a few hand-written skills | **Sequential** | Off for the baseline, then On |
| Learning phase | **Auto-update** for one batch at a time, reviewed after each batch | **Sequential** | On |
| Regression, CI, release gates | **Read-only**, after you reviewed the latest skill commits | **Parallel** if tests are independent, otherwise **Sequential** | On for smoke checks and gates, off for full regression (applies only on **Sequential**) |
| After a redesign or a new sign-in flow | **Auto-update** for one batch on a representative set of tests, then back to **Read-only** | **Sequential** | On |
| Measuring or debugging | **Off** and **Read-only**, compared on the same tests | Either | Off |

Runs always use the latest skills on the default branch. You cannot point a run at an older commit or a tag. A "reviewed state" means no unreviewed commits are waiting under `wopee/skills/`: nobody runs **Auto-update**, and hand edits go in only after review.

Why **Read-only** for runs you rely on: the knowledge stays fixed, so a flaky page, an outage or a wrong verdict in one run cannot rewrite what the next run is told. With **Auto-update**, every run can change the skills, and the change goes straight to the default branch with no review.

When to use **Off**:

- To get a baseline before you add skills.
- When a test suddenly behaves differently and you want to know whether a skill is the cause.
- When you compare models, agent versions or configurations.
- Right after a big redesign, until stale skills are fixed or moved aside.

!!! warning "Do not learn from an unhealthy environment"

    Do not run **Auto-update** while the test environment is down or unstable, against a half-deployed build, during an A/B experiment, or with unusual test data. The agent may record an outage or a one-off state as "how the app works", and every later test follows it.

## Combine skills with the Run Queue

| Combination | Use it for | Watch out for |
| --- | --- | --- |
| **Auto-update** + **Sequential** + Stop queue on failure | Learning batches. Each test starts with the skills the tests before it committed. | Tests run one at a time, so the batch takes longer. |
| **Read-only** + **Parallel** | Fast regression on reviewed skills. | Tests must not share accounts or data whose state they change. |
| **Read-only** + **Sequential** | Tests that share accounts or data, or an environment that cannot take many runs at once. | Order gives no learning benefit here. |
| **Auto-update** + **Parallel** | Rarely useful: only when the tests touch unrelated parts of the app. | Tests in the batch do not learn from each other, and two updates to the same skill overwrite each other completely. The next batch does see the surviving updates. |

Only a **Sequential** batch passes lessons from one test to the next. Separate starts run at the same time and start from the same skills; later starts see what earlier batches committed. A Library **Run (N)** across several analyses makes one queue per analysis. To run a mixed set strictly in order, use a test plan.

### Stop queue on failure

Turn it **on** when:

- an early failure makes the rest meaningless, for example a broken sign-in;
- you run **Auto-update** batches, so a failing run does not keep feeding the rest of the batch. Its own update is still committed, so review it;
- you run a short smoke or gate suite.

Turn it **off** when:

- you want the full list of failures, for example in a nightly regression run;
- you measure the effect of skills, because stopping early drops the later results.

Remember that the queue stops on **Incomplete** and on runs that error out, not only on **Failed**. A stopped queue is a partial result: tests that never ran are untested, not passed. Rerun the full set after the fix.

On **Parallel** the checkbox is hidden, but its saved value still applies to the scenarios the agent runs after a crawl, which always run one by one.

### Make tests safe to run in parallel

Before you switch a project to **Parallel**:

- Each test creates the data it needs and gives new records a unique suffix.
- Tests that change an account's state (cart, profile, settings) use different accounts.
- No test relies on another test having run first.
- Nobody deploys to the test environment during the run.

A good check: run the suite once **Sequential** and once **Parallel**, both on **Read-only**. If verdicts change, some test depends on state left by another test. Fix the test, not the order.

## Write skills by hand

Start with hand-written skills. You know things the agent cannot discover, and in published tests curated skills help while self-generated ones on average do not ([SkillsBench](https://arxiv.org/abs/2602.12670)).

1. Watch a few runs and note where the agent struggles or makes the same mistake twice.
2. For each problem, add or extend one skill in `wopee/skills/<name>/SKILL.md` and commit it to the default branch.
3. Run the affected tests again on **Read-only**. In the run's logs, check that the skill appears in `[SKILLS] Loaded ... valid skill(s)` and that the agent now gets the step right. If your catalog is larger than the preload budget, also check that the skill appears in the `Skills used:` line (with a small catalog every skill is always listed).

Open the repository with **Repo** in the Commander **More** menu, or clone it. To push, you need to have accepted the project's GitHub invitation (see [Where skills live](../concepts/agent-skills.md#where-skills-live)).

### Structure

- **One skill per concern.** One screen, widget or flow per skill: `login-one-time-code`, `booking-date-picker`, `cookie-consent`. Not one skill per test, and not one skill for the whole app.
- **A description that triggers.** Start with the screen or widget, then say when to use the skill, using the words your tests use. Add symptoms: "Use when Search stays disabled after dates were entered."
- **Most important first.** Put preconditions and the one thing that breaks at the top, for example in a `## Gotchas` section.
- **Short.** Most skills need a few dozen lines. Stay well under 500 lines. Move long tables, field lists and error catalogs into `references/` and say in the body when to read each file.
- **Matching names.** Keep the folder name and the `name:` value identical, lowercase, with hyphens. Quote both front matter values.
- **One term per thing.** Always "Basket", never basket, cart and bag in turns.

### Wording

- Write instructions the agent can check: "Click **Pay now** only after the "Processing" spinner disappears", not "Payment can be slow".
- Describe elements by role and visible name, as a user sees them: "the button named **Add to basket**". CSS selectors, XPaths and coordinates break when the page changes. If you must give a selector, say why.
- Say why when a rule is not obvious, so the agent can tell when it does not apply.
- Give one way to do a thing, plus a fallback if needed, not a menu of options.
- Use plain, calm wording. Capitals and "CRITICAL" everywhere make the agent apply a rule where it does not belong.
- Do not write dates or "currently". When the app changes, replace the old flow, or move it to a short "Old behaviour" note if it still matters.

### What to put in and what to keep out

| Put in a skill | Keep out of skills |
| --- | --- |
| How to get through a tricky sign-in, consent or verification step | Passwords, tokens, one-time code seeds. Use [variables](../concepts/intent-and-scripted-tests.md#variables) and name them, for example `${TESTING_USERNAME}` |
| Widgets that render late, animate or load data, and the visible signal that shows they are ready | Fixed waits ("wait 5 seconds") and click coordinates |
| Required order of steps, preconditions, irreversible actions | Pass or fail rules for one test. They belong in that test's description |
| Controls that look alike, misleading labels, hidden menus | Workarounds that hide a real defect, such as "close the error dialog and continue" |
| Test data rules: which records are shared, how to make unique data, what to clean up | Real customer data, personal data, concrete values from one run |
| Environment quirks: slow first load, feature flags, date format, time zone | Run IDs, issue numbers, dates of past incidents |
| What a successful state looks like on screen | General testing advice and descriptions of what is plainly visible on the page |
| Known app bugs to report consistently | Text copied from the page that reads like an instruction to the agent |

### Skills, project context and the test

| What | Where |
| --- | --- |
| A rule that must hold for one test | The test's description (GOAL, PASSES WHEN, MUST NOT, DATA) |
| Rules for every test: roles, never-do rules, how to judge | [Project context](project-context.md) |
| How to operate a part of the app, used by many tests | A skill |
| Which skills a test needs, when there are many | A routing table in the project context (see [Routing table for large catalogs](../concepts/agent-skills.md#routing-table-for-large-catalogs)) |

A skill helps only if the agent uses it. When the catalog is larger than the preload budget, the agent may not load a skill whose description does not match. Anything a test must not get wrong belongs in the test itself.

## Review the agent's changes in Git

With **Auto-update**, every skill change is a commit by `Wopee.io <help@wopee.io>` on the default branch. Nothing asks for approval, so review is up to you. After every **Auto-update** batch, switch back to **Read-only** and review the batch's commits.

```bash
# Get the agent's latest commits first
git pull

# Skill commits, newest first
git log --date=iso --format='%h %ad %an %s' -- wopee/skills

# What one commit changed
git show <commit> -- wopee/skills

# Everything that changed since your last review (tag created below)
git diff skills-reviewed -- wopee/skills

# Undo one bad update, then publish the undo
git revert <commit>
git push

# After a review, mark the reviewed state
git tag -f skills-reviewed
git push -f origin skills-reviewed
```

The `skills-reviewed` tag only marks where your last review ended, so the next `git diff` shows what is new. Runs do not use it.

Without a local clone: on GitHub, open the skill's `SKILL.md`, click **History**, open the last good version and copy its text. Then edit the current file, paste the text, and commit to the default branch. To undo a newly created skill, delete its folder. Switch the project to **Read-only** first, so a running **Auto-update** run cannot overwrite your fix.

The commit message does not name the run. To find the run behind a commit, compare the commit time with the run history in Commander.

### Review checklist

- **True about the app, not about one run?** Delete one-off data states, timing guesses and values from a single run.
- **Hides a defect?** Revert anything that teaches the agent to work around an error. It turns real failures into passes.
- **Secrets or personal data?** Wopee.io does not check updates for them. Revert and rotate anything sensitive. Deleting the file later does not remove it from Git history.
- **Selectors?** The reviewer is asked to record the selectors that worked, so **Auto-update** skills often contain CSS selectors. Rewrite them as role and visible name where you can.
- **Instructions copied from the page?** Text from the app under test, such as user content or third-party widgets, can end up in a skill as a command. Remove it.
- **Content lost?** An update replaces the whole file. Compare with the previous version and restore anything still true that the agent dropped, including extra front matter fields.
- **Renamed or duplicated?** A changed `name:` creates a new folder next to the old skill. Merge duplicates into one skill and delete the extra folder.
- **Description still specific?** It should still name the screen and when to use the skill, not drift toward one test.
- **Still short?** If a skill keeps growing, split it or move detail to `references/`.

Tips:

- Switch to **Read-only** while you curate skills by hand. Otherwise a run that started before your commit can rewrite the skill from its older copy.
- Anyone who can push to the project repository can edit `wopee/skills/` and so changes what the agent is told on every run. Keep project membership to people who should have that.
- If a password or token ever lands in a skill, change that password or token. Deleting the line is not enough, because Git history keeps the old version.
- A skill that changes after almost every run is a warning sign: the app or the environment is unstable, or the skill is too tied to single runs.

## Measure whether skills help

More knowledge is not automatically better. Long or wrong skills cost time and money and can lower pass rates. Measure on your own tests.

1. **Pick the tests.** Choose 10 to 30 tests that represent your app, including some that fail now and then. This costs runs: 10 tests × 3 runs × 2 arms is already 60 runs, and swapping the order (step 5) doubles that. Start small, for example 10 tests × 3 runs, and add step 5 only when the first result is close.
2. **Keep the skills fixed.** Use **Read-only** and make no commits under `wopee/skills/` until both arms are done. Note the latest skill commit so you can tell later what you measured. Never use **Auto-update** for the comparison, because it changes the skills while you measure.
3. **Run without skills.** Set Agent Skills to **Off**. Run each test 3 to 5 times. Turn **Stop queue on failure** off so every run counts.
4. **Run with skills.** Set **Read-only** with the same skills and run the same tests the same number of times, on the same build and with the same test data.
5. **Swap the order (optional).** Repeat both arms once in reverse order, so time of day and data drift do not favour one arm.
6. **Compare per test**, not only the suite total:
    - how many tests passed in **every** run (a test that goes from 3 of 5 to 5 of 5 became stable);
    - how many runs ended **Incomplete**;
    - how long each run took and how many steps it needed;
    - if your catalog is larger than the preload budget, whether the right skills appear in the `Skills used:` line (with a small catalog every skill is always listed).
7. **Check the verdicts.** Open a sample of passes and failures in both arms. A skill that turns real failures into passes is a regression, not an improvement.
8. **Decide.** Keep skills that help. Fix or remove skills behind tests that got worse. If both arms perform the same, the skills are not earning their cost for these tests.

Repeat the comparison after large skill changes, after upgrades of the agent or the AI model, and after major releases of your app. A skill that no longer beats **Off** can be retired.

!!! note "Cost"

    Skills make runs cost a little more, and **Auto-update** adds a review call after every run. See the cost row in [The three modes](../concepts/agent-skills.md#the-three-modes).

With only a few tests and a few runs each, small differences are noise. Do not declare a winner on a difference of one or two tests.

## Troubleshooting

### The Skills tab is missing

The **Skills** tab exists only in agent projects. Integration projects, which receive screenshots from your own Playwright, Cypress, WebdriverIO or Robot Framework tests, do not have it.

### The controls are greyed out

Only project admins can change the settings. Ask a project admin.

### Save is disabled

**Save** saves the whole Project Settings dialog. Check the other tabs for errors such as an invalid project URL, an empty project name or a duplicate variable name.

### The agent does not use my skill

Check the run's logs (open the run and switch to **Logs**) of a run started after your commit:

- `Skills: OFF` – the project is on **Off**. Switch to **Read-only** and save.
- Your skill is not in `[SKILLS] Loaded ... valid skill(s)` – check the path (`wopee/skills/<folder>/SKILL.md`, file name exactly `SKILL.md`), the branch (the default branch, not a pull request) and the front matter (`name` and `description` present and quoted). Look for a skip warning naming your folder.
- `Skills: <mode> — catalog empty` together with `[SKILLS] Failed to load skills` – one skill has front matter that breaks loading for all skills. Quote every `name` and `description` value.
- The skill is in the catalog but not in `Skills used:` – the catalog is larger than the preload budget and the test did not ask for it. Make the description match the words the test uses, mention the skill name in the test, or add a routing table to the project context.

### My hand edit was overwritten

A run with **Auto-update** that started before your commit rewrote the skill from its older copy. Restore your version from Git history and switch to **Read-only** while you curate.

### Auto-update does not commit anything

- No update line in the log: the reviewer found nothing new. That is normal.
- `Skills update skipped: skillsMode is ...`: the mode was changed while the run was going.
- `Skills update skipped: could not parse skill name from YAML frontmatter`: the reviewer's answer had no usable `name:` line, so nothing was committed and your skills are unchanged. No action needed. If it happens often, tell [help@wopee.io](mailto:help@wopee.io).
- `Skills update failed: ...`: the commit to GitHub failed. If the default branch requires pull requests or signed commits, GitHub rejects the commit. Use **Read-only** and change skills through pull requests instead.
- A crawl you stopped, or a run where the agent crashed, does not save an update.
- `Skills: <mode> — catalog empty` after `[SKILLS] Failed to load skills`: the review step was skipped. Fix the front matter that breaks loading.

### Duplicate or contradicting skills

The reviewer created a new skill instead of updating the existing one, or renamed a skill. Merge the content into one skill, delete the extra folder and commit. Contradictions are worse than gaps, because the agent may follow either side.

### Results got worse after a skill change

Rerun the affected tests with **Off**. If they pass without skills, look at the latest commits under `wopee/skills/`, revert the one that caused it, and stay on **Read-only** until the skill is fixed.

### Tests ran at the same time although the project is Sequential

The queue applies per start. Separate clicks, two people starting runs, or a Library **Run (N)** with tests from several analyses each start their own queue. Run them as one selection in one analysis, or as a test plan.

### The queue stopped although no test failed

**Stop queue on failure** also stops on **Incomplete** and on runs that errored out, including runs Wopee.io closed because they never reported back. Open the last finished test to see why.

### The queue is stuck on one test

The running test may still be waiting for a free runner, which can take as long as runners are busy. A run whose workflow ended without reporting is closed as **Incomplete** automatically, usually a few minutes after GitHub marks it completed. A run that GitHub still shows as queued or in progress is never closed automatically. To move on now, use **Stop queue** and start the remaining tests again.

### Parallel runs fail randomly

Tests probably share an account or records. Run the same set **Sequential**: if failures disappear, give each test its own data or account (see [Make tests safe to run in parallel](#make-tests-safe-to-run-in-parallel)).

## FAQ

**What happens to my skills when I switch modes?**
Nothing. Switching never adds, changes or deletes files, only what later runs do with them. See [Switching modes](../concepts/agent-skills.md#switching-modes).

**Does Parallel learn?**
With **Auto-update**, yes, but only from one batch to the next. Tests inside a **Parallel** batch do not see each other's updates, and two updates to the same skill overwrite each other.

**How do I undo a bad update?**
Revert the commit in Git, or restore the previous file version on GitHub. See [Review the agent's changes in Git](#review-the-agents-changes-in-git).

**Is Parallel faster or more expensive?**
Faster when runners are free. Each test is one run either way.

**Can I see or edit skills in Commander?**
No. Skills are files in the project repository. Use **Repo** in the **More** menu, or a local clone.

**Can a skill change a verdict?**
Yes, indirectly: the skills the agent reads during a run steer what it does and how it judges the result, so they can change that run's verdict. The **Auto-update** review that writes skills runs after the verdict is final and cannot change it. That is why skills need review.

**Does Auto-update learn only from passing runs?**
No. It can save a skill after **Passed**, **Failed** or **Incomplete** runs. Its instructions tell it to skip infrastructure failures, but that is the AI's judgement, not a hard rule.

**Are skills shared between projects?**
No. Each project has its own `wopee/skills/` folder. To reuse a skill, copy the folder to the other project's repository.

**Can I delete a skill?**
Yes. Delete its folder on the default branch. The agent never deletes skills, but on **Auto-update** it may create a similar one again.

**Who can read my skills?**
Anyone with access to the project repository. Skill text is also sent to the AI model on runs. Never put secrets or personal data in it.

**Do skills replace the project context?**
No. The project context holds rules for every test and goes into every run. Skills hold know-how about operating parts of the app. See [Skills, project context and the test](#skills-project-context-and-the-test).

**Does `allowed-tools` in the front matter limit the agent?**
No. The agent accepts the field and ignores it. Hard limits belong in the test environment and the test accounts' permissions.

**Do I need a Premium plan?**
The skills setting is available in every agent project. Starting several tests at once, which is where the Run Queue matters most, needs a Premium or Enterprise plan.

**Does Auto-update cost more?**
Yes. It adds one review call after every run, whether or not anything is saved. See the cost row in [The three modes](../concepts/agent-skills.md#the-three-modes).

## Further reading

- [Agent Skills specification](https://agentskills.io/specification) – the open `SKILL.md` format Wopee.io uses.
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (Anthropic) – concise skills, descriptions that trigger, progressive disclosure.
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (Anthropic) – how skills load and why to audit them.
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Anthropic) – repeated trials, pass^k, capability and regression sets.
- [Agent Workflow Memory](https://arxiv.org/abs/2409.07429) – research showing web agents improve by reusing routines learned in earlier runs.
- [An empirical study of memory management in LLM agents](https://arxiv.org/abs/2505.16067) – why agents copy stored experience and why learning only from verified results matters.
- [SkillsBench](https://arxiv.org/abs/2602.12670) – curated skills help, self-generated skills on average do not.
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) – memory and context poisoning (ASI06) and how to limit it.

## Related topics

- [Agent Skills and Run Queue](../concepts/agent-skills.md)
- [Project Context](project-context.md)
- [Intent-driven and Scripted Tests](../concepts/intent-and-scripted-tests.md)
- [Verdict Integrity](../concepts/verdict-integrity.md)
- [Self-Healing](../concepts/self-healing.md)

!!! note "Need help?"

    For questions about Agent Skills or the Run Queue, contact our support team at [help@wopee.io](mailto:help@wopee.io) or visit our [community discussions](https://github.com/orgs/Wopee-io/discussions).
