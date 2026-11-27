---
title: Agent Skills and Run Queue
description: "How Wopee.io Agent Skills work: SKILL.md files in the project repository, how the agent loads them, the Off, Read-only and Auto-update modes, and how the Sequential and Parallel Run Queue and Stop queue on failure interact with them."
---

# Agent Skills and Run Queue

**Agent Skills** are short Markdown files with know-how about your app that the AI agent reads while it tests: how a tricky widget works, what to wait for, which order of steps the app needs. They live in your project's Git repository. A project setting decides whether the agent ignores them, only reads them, or also writes new ones after runs.

The **Run Queue** decides how tests that you start together are executed: one after another, or all at once. It sits next to the skills setting because the order of runs decides whether a test can use what an earlier test in the same batch just learned.

!!! info "For product owners and CTOs"

    Skills are the agent's notebook about your app, kept as plain files in your repository. With **Read-only**, the agent uses the notebook but never changes it, so results depend only on knowledge your team has reviewed. With **Auto-update**, the agent adds to the notebook after each run and commits the change straight to the repository, with no approval step. Both settings are off by default.

## What this page covers

Where the settings are, what each mode does, how the Run Queue works and how it combines with skills, what a skill is and where it lives, how the agent loads skills, and how Auto-update writes them. A reference section at the end lists the file format rules, the log lines and the limits. For advice on which mode to use when, how to write skills and how to review the agent's changes, see [Agent Skills: good practices](../guides/agent-skills.md).

---

## Where to find the settings

Open the project and go to **More** › **Settings** › **Skills**. This opens the **Skills** tab of the Project Settings dialog. The tab has two sections:

- **Agent Skills** – a toggle with **Off**, **Read-only** and **Auto-update**. The help text under it changes with your choice.
- **Run Queue** – a toggle with **Sequential** and **Parallel**. When **Sequential** is selected, a **Stop queue on failure** checkbox appears below it.

| Setting | Default |
| --- | --- |
| Agent Skills | **Off** |
| Run Queue | **Sequential** |
| Stop queue on failure | Not checked |

Projects that never saved this tab behave exactly like the defaults.

Click **Save**. When the changes take effect:

- **Agent Skills** and **Run Queue** apply to runs and batches that start after you save. Tests already **Queued** keep running one by one, even if you switch to **Parallel**.
- **Stop queue on failure** is checked each time a test finishes, so it also applies to a batch that is already running.
- Leaving **Auto-update** also drops the skill update of a run that is in progress.

If you close the dialog with unsaved changes, Commander asks whether to discard or save them.

Some details:

- The **Skills** tab exists only in agent projects. Integration projects, which receive screenshots from your own tests, do not have it.
- Every project member can see these settings. Only project admins can change them, including the Run Queue. For other members the controls are greyed out.
- **Save** saves the whole Project Settings dialog. If another tab has an error, such as an invalid project URL or a duplicate variable name, **Save** stays disabled until you fix it, even if you changed only the **Skills** tab.
- In an analysis, **Variables & Knowledge** › **Skills** opens this tab. It does not show the skill files.

!!! note "Commander does not show skill files"

    Commander has no viewer or editor for skills. To read, add, edit or delete skills, open the project's repository on GitHub (**Repo** in the **More** menu) or a local clone of it. See [Where skills live](#where-skills-live).

## The three modes

| | **Off** | **Read-only** | **Auto-update** |
| --- | --- | --- | --- |
| Agent loads skills | No | Yes | Yes |
| Agent writes skills | No | No | Yes, at most one per run |
| Extra cost per run | None | Longer agent instructions (up to the preload budget) and an occasional **loadSkill** call | Same as **Read-only**, plus one review call after every run, even when nothing is saved |
| First skills line in the run's logs | `Skills: OFF` | `Skills: READ_ONLY — ...` | `Skills: AUTO_UPDATE — ...` |

### Off

The agent runs without skills. It does not read `wopee/skills/` and has no skill tools, and nothing is written to the repository. Use **Off** for a baseline run, or to check whether a skill is causing a problem.

### Read-only

The agent loads and uses the skills as described in [How the agent uses skills](#how-the-agent-uses-skills), and never writes. Only people change skills, by committing to the repository. During a run, **Read-only** and **Auto-update** use skills in the same way. The only difference is what happens after the verdict.

### Auto-update

The agent uses skills like **Read-only** and, after each run, can save what it learned as a skill. See [How Auto-update writes skills](#how-auto-update-writes-skills).

### Switching modes

Switching modes never adds, changes or deletes skill files. It only changes what runs that start after you save do with them. Skills committed under **Auto-update** stay in the repository when you switch to **Read-only** or **Off**, and are used again as soon as the mode is **Read-only** or **Auto-update**.

A run that is already going keeps its mode, with one exception: if you switch away from **Auto-update**, that run's skill update is dropped.

## Run Queue

The Run Queue applies to tests that are **started together**: in one click, one run request or one test plan.

| Mode | What happens |
| --- | --- |
| **Sequential** (default) | The first test starts. The others show as **Queued** and start one by one, each after the previous run has its final verdict and, with **Auto-update**, its skill update is committed. They run oldest first, in the order they were sent. |
| **Parallel** | Every test starts at once, each as its own run. How many really run at the same time depends on free test runners; the rest wait for a runner. |

Speed and cost: each test is one run in both modes, so the queue mode does not change how a single run is executed or counted. Only the total time differs. A **Sequential** batch takes at least the sum of its runs, plus processing between them: ten five-minute tests take 50 minutes or more. A **Parallel** batch takes about as long as its slowest test, if enough runners are free.

### Stop queue on failure

With **Stop queue on failure** checked, a test that ends badly stops the rest of its queue: all tests still **Queued** in that batch become **Stopped**, and the batch shows as failed. A test ends badly when its verdict is **Failed** or **Incomplete**, or when the run errors out. Not only **Failed** counts: an **Incomplete** verdict from [Verdict Integrity](verdict-integrity.md), a cancelled job or a run that never reported back stop the queue too.

Unchecked, a failed test does not hold up the queue: the next test starts as soon as the failure is recorded.

Two exceptions:

- If Wopee.io fails to process a finished test, the remaining queued tests are stopped even when **Stop queue on failure** is unchecked.
- A failed skill commit does not stop the queue.

The checkbox is hidden when **Parallel** is selected, but its saved value is kept and still applies to the scenarios the agent runs after a crawl. Those are always queued one by one, even on a **Parallel** project.

### What counts as started together

Each start makes its own queue. A second start in the same project within 10 seconds of the previous one is refused with "Dispatch rate limit exceeded". Starts further apart each make their own queue and run at the same time on a **Sequential** project.

| How you start tests | Queues |
| --- | --- |
| Run one test | Starts at once. |
| Select several tests in an analysis and run them | One queue. |
| **Run all N tests** in the analysis workspace | One queue. |
| Run a test plan | One queue across all analyses in the plan. |
| **Run (N)** in the Library with tests from several analyses | One queue **per analysis**, all starting at once. With tests from three analyses, three tests run at the same time. If one analysis is refused with "Dispatch rate limit exceeded", run its tests again after 10 seconds. |
| Scenarios the agent runs automatically after a crawl (up to 4 by default) | Their own queue, always run one by one, even on a **Parallel** project. |

To run a mixed selection strictly one at a time, put the tests into a test plan and run the plan.

Starting several tests at once needs a Premium or Enterprise plan. On other plans, tests start one per click, so the Run Queue mainly affects test plans and the scenarios run after a crawl.

### Stopping a queue

- In the analysis test list, **Stop queue** opens "Stop all queued tests?". **Stop all** stops the current test and cancels every queued one.
- Each test's menu has **Stop/Dequeue** for a single test.

Stopping marks the tests **Stopped** in Commander at once, but does not cancel a job that is already running. That run keeps going, its result can replace **Stopped**, and with **Auto-update** it can still commit a skill update. To prevent that, switch to **Read-only** before it finishes.

### Runs that never report back

If a running test's workflow finished without reporting back, Wopee.io closes it as **Incomplete** automatically, usually a few minutes after GitHub reports the run as completed. If GitHub never created a workflow run for the start, it is closed after about 15 minutes. Only then does the queue continue, or stop if **Stop queue on failure** is checked.

A run that GitHub still reports as queued or in progress, for example while it waits for a free runner, is never closed automatically, however long it takes. A **Sequential** queue waits behind it. A longer time limit applies only when GitHub cannot be asked about the run at all.

## How Run Queue and skills work together

With **Auto-update** and **Sequential**, Wopee.io commits a run's skill update before it starts the next test in the queue. The next test uses the repository after that commit, so it can use what the previous test learned. This is what the **Sequential** help text means by "each run benefits from skills learned in previous runs".

| Combination | Effect |
| --- | --- |
| **Auto-update** + **Sequential** | Each test in the batch starts with the skills committed by the tests before it, and a wrong lesson spreads the same way. **Stop queue on failure** ends the batch at the first Failed or Incomplete run, but that run's update is still committed, and lessons from passed runs are never stopped. Review the commits after the batch. |
| **Auto-update** + **Parallel** | Every test can still commit one skill, so the next batch starts with what this batch learned. Tests inside this batch do not see each other's updates. If two tests update the same skill, the later commit replaces the earlier one completely. |
| **Read-only** + **Parallel** | All tests read the same reviewed skills. Fast, and nothing is written. |
| **Read-only** + **Sequential** | No learning between tests. Useful when tests share accounts or data, or the test environment cannot take many runs at once. |
| **Off** + either | No skills. The queue only controls order and load. |

The agent itself does not know the Run Queue mode. Ordering and stopping are handled by Wopee.io between runs. Only a **Sequential** batch passes lessons from one test to the next. Separate starts run at the same time and start from the same skills; later starts see what earlier batches committed.

## What a skill is

A skill is one folder with a `SKILL.md` file. The file starts with a short header (name and description) and continues with Markdown instructions. Skills hold reusable knowledge about operating your app that many tests need, for example:

- how to get through a sign-in step with a one-time code
- which button really saves a form when two look alike
- what a date picker accepts and what it silently ignores
- what to wait for after a slow search, and how to tell it has finished
- which step has to come first, such as accepting the cookie banner

A skill is guidance for the agent. It is not a test, it does not decide pass or fail, and it cannot block the agent from doing anything. Pass and fail rules belong in each test's description (see [Intent-driven and Scripted Tests](intent-and-scripted-tests.md)), and project-wide rules belong in the [project context](../guides/project-context.md).

### The SKILL.md format

Wopee.io uses the open [Agent Skills format](https://agentskills.io/specification): YAML front matter between two `---` lines, then a Markdown body. The front matter needs a `name` and a `description`; see [Front matter fields](#front-matter-fields) for the rules.

````markdown
---
name: "booking-date-picker"
description: "Booking page date range picker (Check-in and Check-out fields). Use when a test picks travel dates or changes the length of a stay, or when Search stays disabled after dates were entered."
---

# Booking date picker

## Gotchas

- Typed dates are cleared when the field loses focus. Pick dates by clicking days in the calendar.
- The calendar always opens on the current month. Use the button named "Next month" to move forward. There is no year selector.
- Days before today are shown but cannot be clicked.

## Pick a date range

1. Click the **Check-in** field. A dialog named "Choose dates" opens.
2. Click the check-in day, then the check-out day.
3. Click **Apply**.

## You are done when

- Both fields show a date in DD/MM/YYYY format, the text under them reads "N nights", and **Search** is enabled.

## More detail

- Read `references/blackout-dates.md` when a test needs dates around public holidays.
````

## Where skills live

Skills are files in the project's GitHub repository, on its default branch.

Each agent project has its own repository. Open it with **Repo** in the **More** menu. To add or edit skills you need push access to that repository. Project members get push access through the project's GitHub team after they accept the invitation with **GitHub Invite** in the user menu. If you still cannot push, ask [help@wopee.io](mailto:help@wopee.io).

```text
wopee/
  skills/
    booking-date-picker/
      SKILL.md
      references/
        blackout-dates.md
    login-one-time-code/
      SKILL.md
```

- Each folder directly under `wopee/skills/` is one skill and must contain a file named exactly `SKILL.md`. A folder without one is skipped. Loose files in `wopee/skills/` and folders nested deeper are ignored.
- A skill can have a `references/` folder with extra `.md` files for detail the agent reads only when it needs it. Only `.md` files directly inside `references/` are listed for the agent. Files in subfolders are not listed, but the agent can still read one if the skill body names its path. Symbolic links and files whose names start with a dot are not listed. Each reference file can be up to 256 KiB.
- A new project has no `wopee/skills/` folder. It appears when you commit the first skill, or when an **Auto-update** run saves one.
- Each run uses the latest commit on the default branch at the moment it is dispatched (for a queued test, when it leaves the queue). Skills on other branches or in open pull requests are not used until they are merged.
- Interactive runs on Wopee.io's pre-warmed runners, such as a live crawl and the scenarios it runs afterwards, do not read the repository and run without skills.

Skills belong to one project. Other projects do not see them.

## How the agent uses skills

In short: if all your skills together fit in about 96,000 characters (roughly 1,500 lines of Markdown), the agent reads every skill at the start of every run. If they do not fit, it reads only the skills the test names. It can load others later when a step matches their description. That is why a clear description matters more as your catalog grows.

In detail, with **Read-only** or **Auto-update** the agent prepares its skills at the start of every run:

1. **Find.** It reads every `wopee/skills/<folder>/SKILL.md` in the repository and lists the `references/` files of each skill with their sizes.
2. **Check.** It applies the [validation rules](#validation-rules) and keeps the valid skills. Together they form the skill catalog.
3. **List.** The name and description of every skill in the catalog go into the agent's instructions, after the project context and the application description.
4. **Preload.** The agent puts the full text of skills into its instructions before the first step, within a budget of 24,000 estimated tokens. That is about 96,000 characters across all skills.
    - **If the whole catalog fits**, every skill is preloaded, sorted by name, on every run. The agent does not need to load anything.
    - **If the catalog is larger**, only the skills the test asks for are preloaded, as many as fit. A test asks for a skill when its text names the skill (upper and lower case are ignored) or uses a trigger from a routing table (see below). Skills are taken in the order the test first mentions them.
5. **Load on demand.** Skills that were not preloaded stay in the list. The agent can load up to five of them at a time with its **loadSkill** tool when a step needs them. When everything was preloaded, the agent does not get this tool at all.
6. **Read references.** When a skill has `references/` files, the agent gets a **loadSkillResource** tool and reads a reference file only when it needs it. It cannot read files outside the skill's `references/` folder.

Because the agent decides itself whether to load a skill that was not preloaded, write each description so that it names the screen, the widget or the symptom it covers. A skill whose description does not match the test is not used.

The skills the agent reads during a run steer what it does and how it judges the result, so they can change that run's verdict.

### Routing table for large catalogs

When your skills together exceed the preload budget, you can tell the agent which skills a test needs. Add a Markdown table to the [project context](../guides/project-context.md) that names a skill in backticks in one cell and lists triggers in the other cells, each trigger in backticks or double quotes:

```markdown
## Skills to use

| Skill | Use when a test mentions |
| --- | --- |
| `booking-date-picker` | "Check-in", "Check-out", "stay length" |
| `login-one-time-code` | "one-time code", "OTP" |
```

Triggers are matched case-sensitively and only as whole words: "Check-in" does not match "check-in", and "OTP" does not match "OTP-SMS". The application description of an analysis can carry a routing table too.

## How Auto-update writes skills

After the run's verdict is final, the agent makes one more, separate AI call to review the run. This call cannot change the verdict. On errors it is retried up to twice.

1. The reviewer receives the verdict, the run report, the test, the application description, the name, description and body of every existing skill (not their `references/` files or other front matter fields) and the log of the agent's actions. It does not see the project context.
2. It answers with either one complete `SKILL.md` or nothing. It is told to answer with nothing when the run taught nothing new about the app, when existing skills already cover it, or when the run failed because of the infrastructure, such as timeouts or network errors.
3. Wopee.io checks the project's skills mode again. If it is no longer **Auto-update**, the update is dropped.
4. Wopee.io takes the skill name from the `name:` line and commits the whole text to `wopee/skills/<name>/SKILL.md` on the repository's default branch.

The reviewer follows Wopee.io's skill-authoring instructions, which ask it to record the selectors and sequences that worked. Expect **Auto-update** skills to contain CSS selectors. When you review them, rewrite selectors as role and visible name where you can.

What the commit looks like:

| | |
| --- | --- |
| Author | `Wopee.io <help@wopee.io>` |
| Message | `Create wopee/skills/<name>/SKILL.md` or `Update wopee/skills/<name>/SKILL.md` |
| Branch | The default branch, directly. No pull request, no review step. |
| Run reference | None. The message does not name the run, so match commit times with the run history. |

### What it writes

- **One skill per run.** A run creates or updates at most one `SKILL.md`. It never writes `references/` files and never deletes a skill.
- **Whole-file replace.** An update replaces the whole file with the reviewer's new version. Nothing is merged, so content the reviewer leaves out is gone. To restore an older version, see [Review the agent's changes in Git](../guides/agent-skills.md#review-the-agents-changes-in-git).
- **Extra front matter is lost.** The reviewer sees only the name, description and body of existing skills. Fields such as `license` or `metadata` usually disappear when it rewrites a skill.
- **A new name means a new skill.** If the reviewer changes the `name:` of a skill, the update lands in a new folder and the old skill stays. The reviewer can also add a second skill on a topic an existing skill already covers. Merging such duplicates is manual.
- **Test runs and crawls.** Both test runs and analysis crawls can write a skill. A crawl you stop does not save one.
- **Any verdict.** The reviewer runs after **Passed**, **Failed** and **Incomplete** runs alike. Only its instructions tell it not to learn from infrastructure failures.

### When it does not write or can go wrong

- **No update after a crash.** If the agent itself errors out, no update is sent.
- **No update when loading fails.** If the skill catalog fails to load (see the [Quote the values](#validation-rules) tip), the review step is skipped and nothing is saved.
- **Mode switch during a run.** Switching away from **Auto-update** while a run is going drops that run's update. Switching to **Auto-update** during a run has no effect on that run.
- **Stopping does not prevent a commit.** A run you stop keeps going on its runner and can still commit its update. Switch to **Read-only** first.
- **Hand edits can be overwritten.** A run that started before you committed a hand edit rewrites the skill from the older version it used.
- **No checks before the commit.** Wopee.io does not check the update before committing it: the folder name is the `name:` value exactly as written, and the front matter is not validated. An update with invalid YAML is committed, and later runs skip it (or, with a date or number value, skip every skill). Check new skills in the logs of the next run.
- **No content checks.** Wopee.io does not check updates for passwords, tokens, personal data or test data before committing them.

## What you see in Commander

- The **Skills** tab (**More** › **Settings** › **Skills**) shows the two settings. No skill content is shown anywhere in Commander.
- Queued tests show **Queued** (in the analysis test list and the Library) or sit in the **QUEUED** column of the analysis board. A blinking dot means a test is queued or running.
- Tests stopped by **Stop queue on failure** or by you show **Stopped**.
- To see what happened with skills in a run, open the test run and switch the report view to **Logs**. For a crawl, the same log opens with **View logs**. The lines are listed in [Log lines](#log-lines).

## Reference

### Front matter fields

| Field | Required | Rule |
| --- | --- | --- |
| `name` | Yes | Lowercase letters, digits and single hyphens, at most 64 characters, same as the folder name. |
| `description` | Yes | What the skill covers and when to use it, at most 1024 characters. |
| `license`, `compatibility`, `metadata`, `allowed-tools` | No | Accepted but not used by the agent. `allowed-tools` does not limit what the agent can do. |

### Validation rules

The agent checks each skill when it loads it:

| Problem | What happens |
| --- | --- |
| `name` or `description` missing or empty | The skill is skipped, with a warning in the run's logs. |
| No front matter at all | The skill is skipped (it has no description). |
| Front matter is not valid YAML | That skill is skipped, with `[SKILLS] Failed to parse SKILL.md in "<folder>"`. |
| Name too long, uppercase letters, spaces, `--`, or a name different from the folder | Warning only. The skill still loads, under the name in its front matter. |
| Description over 1024 characters, `compatibility` over 500 characters | Warning only. The skill still loads. |
| Two skills with the same name (upper and lower case count as the same) | Only one is used, in directory listing order (not alphabetical). The other is dropped without a log line. This happens when a folder name differs from its `name:` and **Auto-update** then writes `wopee/skills/<name>/` next to it. |

!!! tip "Quote the values"

    Put the `name` and `description` values in double quotes. YAML reads an unquoted value such as `2026-01-01` or `123` as a date or a number, not as text, and such a value can make the agent skip every skill for that run. The log then shows `[SKILLS] Failed to load skills: ...` followed by `catalog empty`. On **Auto-update**, such a run also saves no skill update, because the review step is skipped when the catalog fails to load.

### Log lines

With **Off** the run's logs show only `Skills: OFF`. With **Read-only** or **Auto-update**:

| Log line | Meaning |
| --- | --- |
| `[SKILLS] Discovered 4 skill(s)` | `SKILL.md` files found, before checking. |
| `[SKILLS] Loaded 3 valid skill(s): booking-date-picker, login-one-time-code, ...` | Skills that passed the checks. |
| `[SKILLS] Directory "<folder>" has no SKILL.md — skipped` | A folder without `SKILL.md`. |
| `[SKILLS] No valid skills found after validation` | No skill passed the checks. |
| `Skills: READ_ONLY — 3 in catalog, 3 preloaded (~2.1k tokens): ...` | Summary: catalog size, preloaded skills, and how many are left for loading on demand. |
| `Skills: <mode> — catalog empty` | No usable skills for this run. |
| `Tool 'loadSkill' called for skill(s): ...` | The agent loaded skills during the run. |
| `Tool 'loadSkillResource' called: <skill> :: references/<file>.md` | The agent read a reference file. |
| `Skills used: booking-date-picker (preloaded); login-one-time-code (loadSkill)` | End of run: skills put into the instructions up front (preloaded) or loaded by the agent (loadSkill). A preloaded skill is listed even if the agent never needed it. When the whole catalog fits the budget, every skill is listed on every run. `Skills used: none` if none. |

With **Auto-update**, the logs also show the result of the update after the verdict:

| Log line | Meaning |
| --- | --- |
| `Skill "<name>" updated successfully at wopee/skills/<name>/SKILL.md` | The skill was committed. |
| `Skills update skipped: skillsMode is <mode>` | The project was no longer on **Auto-update** when the run finished. |
| `Skills update skipped: could not parse skill name from YAML frontmatter` | The update had no usable `name:` line. Nothing was committed. |
| `Skills update failed: <reason>` | The commit to the repository failed. |
| `[SKILLS] generateSkillsUpdate failed, skipping skill persistence: ...` | The review call failed. The verdict is not affected. |

When the reviewer decides there is nothing new to save, no update line appears.

### Limits and defaults

| Item | Value |
| --- | --- |
| Skills location | `wopee/skills/<name>/SKILL.md` on the default branch of the project repository |
| Folder depth | One level under `wopee/skills/`; `references/` one level under the skill |
| Required front matter | `name` and `description`, both non-empty |
| Name | At most 64 characters, lowercase letters, digits and hyphens, same as the folder (warning only) |
| Description | At most 1024 characters (warning only) |
| Size of `SKILL.md` | No hard limit; keep it under about 500 lines |
| Reference file | `.md` only, up to 256 KiB each |
| Preload budget | 24,000 estimated tokens (about 96,000 characters) for the whole catalog |
| Skills loaded per `loadSkill` call | 1 to 5 |
| Skills written per Auto-update run | At most 1 |
| Scenarios run after a crawl | Up to 4 by default, always one by one |
| Starts you make in one project | At most one every 10 seconds (test plans and scenarios run after a crawl are not limited) |
| Default modes | Agent Skills **Off**, Run Queue **Sequential**, Stop queue on failure unchecked |
| Who can change the settings | Project admins |

## Related topics

- [Agent Skills: good practices](../guides/agent-skills.md)
- [Project Context](../guides/project-context.md)
- [Self-Healing](self-healing.md)
- [Verdict Integrity](verdict-integrity.md)
- [Intent-driven and Scripted Tests](intent-and-scripted-tests.md)
- [Read your first results](../first-green-test/read-your-first-results.md)

!!! note "Need help?"

    For questions about Agent Skills or the Run Queue, contact our support team at [help@wopee.io](mailto:help@wopee.io) or visit our [community discussions](https://github.com/orgs/Wopee-io/discussions).
