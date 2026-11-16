---
title: Troubleshooting Commander
description: Fix the messages Wopee.io Commander shows on a new project and a first analysis - the app returned an error or is not reachable, private network, we couldn't check your app's URL, project limit, waiting for a live browser session, agent needs your input, crawling failed, ran out of time, login failed, stopped before it could report, step limit, content policy.
type: How-to
updated: 16 November 2026
---

# Troubleshooting Commander

Find the message Commander shows, then apply the fix. Each heading is the message exactly as it appears on screen, so you can search this page for the words you see. Problems with the MCP server in a coding agent are on [Troubleshooting the Wopee.io MCP server](../guides/wopee-mcp/troubleshooting.md).

!!! note "Retries count on the free plan"

    The free plan gives the testing agent 50 steps every 5 hours, counted across your projects. A run is refused when fewer than 5 steps are left. Your first analysis started in Commander does not count, once per account, even when it ends early. Every later analysis, **Re-run crawl** and test run counts. So after a fix, re-run the tests you already have first, and start a new analysis only when you need new tests.

## Enter a full URL, for example https://example.com { #enter-a-full-url }

**Also called:** URL not accepted, invalid URL.

**Where:** under the URL field in **New project**.

**Cause:** the text in the field is not a web address, for example a word without a domain.

**Fix:** paste the address you open in the browser, with `https://`, for example `https://staging.yourapp.com`.

## The app returned an error or is not reachable. { #app-not-reachable }

**Also called:** URL not reachable, can't reach my app, project created but nothing found.

**Where:** a warning under the URL field in **New project**, followed by "The project will still be created, but exploration may not find anything." It also appears on the [We couldn't check your app's URL](#couldnt-check-url) page.

**Cause:** Commander opened the address from the cloud and got no answer, or an HTTP error (400 or higher). Usual reasons: a typo, `localhost` or an address that only works inside your network or VPN, an app that is down, or a page protected by Vercel or Netlify deployment protection, basic auth or a firewall.

**Fix:**

- Open the address in a private browser window on a network outside your company (for example your phone without Wi-Fi). If it does not load there, the agent cannot reach it either.
- For an app on your computer or inside your network, use a public tunnel or a deployed preview URL.
- If you are sure the app is up, you can still create the project. The warning does not block creation.

**More:** [Can the agent reach your app?](https://docs.wopee.io/guides/test-localhost/) and [Enterprise Connectivity](../security/enterprise-connectivity.md)

## This address is on a private network, so Wopee can't check it from the cloud. Runs from your own runner may still reach it. { #private-network }

**Also called:** private IP, internal URL, localhost not allowed.

**Where:** under the URL field in **New project**, and on the [We couldn't check your app's URL](#couldnt-check-url) page.

**Cause:** the address is `localhost`, ends in `.local`, `.internal` or `.localhost`, or resolves to a private, loopback or link-local IP address (for example `10.x.x.x`, `192.168.x.x`, `127.0.0.1`). Wopee.io's cloud runners cannot open such an address.

**Fix:**

- Use a public tunnel or a deployed URL for the app.
- To test an internal app without exposing it, run the tests on your own runner or connect your network. See [Enterprise Connectivity](../security/enterprise-connectivity.md).

**More:** [Can the agent reach your app?](https://docs.wopee.io/guides/test-localhost/)

## The URL couldn't be checked right now. { #url-check-failed }

**Also called:** URL check failed.

**Where:** under the URL field in **New project**, and on the [We couldn't check your app's URL](#couldnt-check-url) page.

**Cause:** the check itself failed, not your app. Commander could not finish the request.

**Fix:** wait a moment and try again, or create the project anyway. If the app is reachable from the internet, the agent can still open it.

## Your session expired. Sign in again to continue. { #session-expired }

**Also called:** logged out, session timeout.

**Where:** under the URL field in **New project**.

**Cause:** your Commander sign-in expired while the dialog was open.

**Fix:** reload the page and sign in again, then create the project.

## We couldn't check your app's URL { #couldnt-check-url }

**Also called:** URL check page, sign-up stopped at my URL.

**Where:** a full page after you sign up with your app's URL from wopee.io. It shows the URL, the reason (one of the messages above) and two buttons.

**Cause:** the address did not pass the reachability check. See the reason under the URL:

- [The app returned an error or is not reachable.](#app-not-reachable)
- [This address is on a private network…](#private-network)
- [The URL couldn't be checked right now.](#url-check-failed)

**Fix:**

- **Use a different URL** takes you to the project list, where **New project** lets you enter another address.
- **Create project anyway** creates the project and starts the analysis on this address. Choose it when you know the app is reachable from the internet, for example when it was only down for a moment.

**More:** [Can the agent reach your app?](https://docs.wopee.io/guides/test-localhost/)

## Project limit reached { #project-limit-reached }

**Also called:** can't create a project, project locked, lock icon on my project, sign-up link only opened the project list.

**Where:** a toast when you click **New project**, for example "Project limit reached: 2/2 projects". A project above your plan's limit shows a lock icon in the project list, and opening it offers an upgrade. When none of your projects is open to you, the list shows "Try demo projects for free".

**Cause:** your plan allows a set number of projects you own; the free plan allows 2. Projects above the limit are locked; your oldest projects stay open. Demo projects are never locked. A sign-up link from wopee.io at the limit opens the project list without creating a project.

**Fix:**

- Delete a project you no longer need, then create the new one.
- Or reuse an open project: change its app address in **Project settings**.
- Or upgrade for more projects.

## Waiting for a live browser session… { #waiting-for-live-browser }

**Also called:** live view is empty, browser not loading, stuck on waiting, nothing happens.

**Where:** in the **Live** tab of an analysis, in place of the agent's browser.

**Cause:**

- In the first minute of a run: the agent's browser is still starting.
- Later: the browser session has ended. The run finished or stopped, or the agent waited too long for you, for example when you come back the next day.

**Fix:**

- Give a new run a minute. Click the refresh icon (**Refresh the browser picture**) if the picture stays empty.
- If the **Browser** | **Logs** switch is shown, switch to **Logs** to see what the agent is doing or where it stopped.
- If the run is over, open the crawl run to see its result. If it failed, follow its message below, for example [Starting URL unreachable.](#starting-url-unreachable) or [The crawl stopped before it could report.](#crawl-stopped-before-report)

**More:** [Read your first results](https://docs.wopee.io/first-green-test/read-your-first-results/)

## Agent needs your input { #agent-needs-your-input }

**Also called:** the agent is waiting for me, hand-over, take control, CAPTCHA, MFA code, the agent asks me to log in. The browser tab title starts with "(Waiting for you)".

**Where:** a card over the **Live** view with "Agent says" (what it needs) and sometimes "Suggested" (what to do), a message box and **Resume agent**.

**Cause:** the agent reached something it cannot do alone and handed the browser to you: usually a login without credentials, a CAPTCHA or a one-time code. It waits up to 60 minutes. Then it stops the run, and the logs say "Handoff timed out after 60 minutes with no user response."

**Fix:**

1. Do what the card asks, directly in the live browser: sign in, solve the challenge or enter the code.
2. Optionally type a note for the agent in the message box, for example what you did.
3. Click **Resume agent**.

A login you type in the live browser helps only this run. So that the generated tests can sign in too, add a test account to the project, then re-run the tests.

If the agent asks a question with options instead, pick one. Until you answer, the control button reads "Answer the agent's question first".

**More:** [Test an app behind a login](https://docs.wopee.io/first-green-test/test-behind-a-login/)

## Crawling failed { #crawling-failed }

**Also called:** analysis failed, crawl failed, exploration failed, red crawl card.

**Where:** a box at the top of the crawl run, in the analysis. It shows the cause in bold, **Re-run crawl**, **View logs**, how long the run lived (for example "Run failed after 19 s") and what to do. The cause is one of:

- [The crawl ran out of time.](#crawl-ran-out-of-time)
- [The crawl never started.](#crawl-never-started)
- [The run was cancelled.](#run-cancelled)
- [Starting URL unreachable.](#starting-url-unreachable)
- [Starting URL is not valid.](#starting-url-not-valid)
- [Login failed.](#login-failed)
- [The agent could not finish exploring.](#agent-could-not-finish)
- [The agent reported a problem.](#agent-reported-a-problem)
- [The crawl stopped before it could report.](#crawl-stopped-before-report)

**Re-run crawl** counts toward your steps, see the note at the top of this page.

## The crawl ran out of time. { #crawl-ran-out-of-time }

**Also called:** crawl timed out, analysis too long.

**Where:** under "Crawling failed", followed by "The run hit its time limit before the agent reported."

**Cause:** the agent was still exploring when the run reached its time limit, usually on a large app or with broad instructions.

**Fix:**

- Narrow what the agent explores with the project context in **Project settings**: name the flows that matter and the areas to skip.
- Open the logs to see how far it got.
- Then re-run the crawl.

**More:** [Project context](../guides/project-context.md)

## The crawl never started. { #crawl-never-started }

**Also called:** run did not start, stuck in queue.

**Where:** under "Crawling failed", followed by "The runner could not start the agent."

**Cause:** the cloud runner could not start the agent. This is usually temporary.

**Fix:** re-run the crawl. If it happens again, open the logs, look for the first error and send it to [help@wopee.io](mailto:help@wopee.io).

## The run was cancelled. { #run-cancelled }

**Also called:** run cancelled.

**Where:** under "Crawling failed", followed by "It was cancelled before the agent could report."

**Cause:** the run was cancelled on the runner before the agent wrote its report.

**Fix:** re-run the crawl.

## Starting URL unreachable. { #starting-url-unreachable }

**Also called:** app not reachable, can't open my site, connection refused, timeout on the first page.

**Where:** under "Crawling failed", followed by "The agent could not open the app's starting address." and, when recorded, the address with its network error.

**Cause:** the agent's browser could not open the project's app address: a typo, a missing `https://`, `localhost` or an internal address, an app that is down, or a firewall that blocks Wopee.io's runners.

**Fix:**

- Check the app's address in **Project settings**. A typo or a missing `https://` is the usual cause.
- If the app is internal, make sure Wopee.io's runners can reach it (VPN, firewall allowlist).
- Then re-run the crawl.

**More:** [Can the agent reach your app?](https://docs.wopee.io/guides/test-localhost/) and [Enterprise Connectivity](../security/enterprise-connectivity.md)

## Starting URL is not valid. { #starting-url-not-valid }

**Also called:** invalid URL.

**Where:** under "Crawling failed", followed by "The app's starting address is not a full web address."

**Cause:** the project's app address is not a full web address.

**Fix:** fix the address in **Project settings** and include `https://`. Then re-run the crawl.

## Login failed. { #login-failed }

**Also called:** can't log in, stuck on the login page, wrong password, tests only cover the login page.

**Where:** under "Crawling failed", followed by "The agent could not sign in with the configured credentials." In a test run, the agent's report says that the login did not work.

**Cause:** the agent typed the credentials it was given, and the app did not let it in: a wrong or expired password, a locked account, a second factor (MFA) or a CAPTCHA.

**Fix:**

- Check the login details and `auth.json` in **Variables & Knowledge**.
- Use a dedicated test account without MFA or CAPTCHA, or with test keys for them.
- Then re-run the tests you already have. Start a new analysis only if you need new tests for the pages behind the login.

**More:** [Test an app behind a login](https://docs.wopee.io/first-green-test/test-behind-a-login/)

## The agent could not finish exploring. { #agent-could-not-finish }

**Also called:** incomplete crawl, analysis incomplete.

**Where:** under "Crawling failed", followed by "Its report below says why."

**Cause:** the agent wrote a report with the verdict Incomplete: something stopped it, for example a page that did not load, a missing login or a blocked flow.

**Fix:** read the agent report below the box. It names the cause. Fix that, then re-run the crawl.

**More:** [Read your first results](https://docs.wopee.io/first-green-test/read-your-first-results/) and [Verdict Integrity](../concepts/verdict-integrity.md)

## The agent reported a problem. { #agent-reported-a-problem }

**Also called:** crawl failed with a report.

**Where:** under "Crawling failed", followed by "Its report below says what."

**Cause:** the agent finished and reported the crawl as Failed. Its report says what went wrong; it can be a problem in your app.

**Fix:** read the agent report below the box, then re-run the crawl.

**More:** [Read your first results](https://docs.wopee.io/first-green-test/read-your-first-results/)

## The crawl stopped before it could report. { #crawl-stopped-before-report }

**Also called:** crawl died, no report, nothing recorded, run failed after a few seconds.

**Where:** under "Crawling failed", followed by "Nothing was recorded — no agent report, steps or screenshots." or "Its partial results are below."

**Cause:** the run ended before the agent wrote its report. A failure in the first seconds is usually the runner (it could not start or was lost). Later in the run, a common cause is an AI model refusal, see [content policy](#content-policy).

**Fix:**

- Re-run the crawl. A failure this early is often temporary.
- If it fails again, open the logs and look for the first error.
- Check the app's address in **Project settings** and the login details in **Variables & Knowledge**.

## Crawling stopped { #crawling-stopped }

**Also called:** run stopped, analysis stopped.

**Where:** a box at the top of the crawl run with "The crawl was stopped before it finished."

**Cause:** someone stopped the run. This is not a failure.

**Fix:** re-run the crawl when you are ready.

## Step limit reached { #step-limit-reached }

**Also called:** usage limit, out of steps, can't run tests, free plan limit.

**Where:** a toast when you start an analysis or a run, followed by the upgrade dialog. The toast reads for example "Step limit reached: 47/50 steps used", or "Step limit reached." with the current offer. If a usage boost is active, it adds "That already includes the … boost" and when your window resets.

**Cause:** your plan's steps for the current 5-hour window are used up. On the free plan that is 50 steps, counted across all your projects, and a run is refused when fewer than 5 are left. An analysis explores your app and then runs the tests it generates, so it can use most of the budget at once.

**Fix:**

- Wait until the window resets, then run one test at a time.
- Re-run the tests you already have instead of starting a new analysis.
- Or upgrade for more steps.

**More:** [Usage limit right after the first analysis](../guides/wopee-mcp/troubleshooting.md#usage-limit-right-after-the-first-analysis)

## Image processing blocked due to content policy violation { #content-policy }

**Also called:** content policy, content filter, safety filter, AI refused.

**Where:** in the run's logs. The crawl card usually shows [The crawl stopped before it could report.](#crawl-stopped-before-report)

**Cause:** the AI model's provider refused a screenshot of a page, for example one with nudity, medical images or gambling. The message comes from the provider, not from Commander.

**Fix:**

- Re-run the crawl. A refusal does not always repeat.
- If it repeats on the same page, tell the agent to skip that page in the test instructions or the project context, and send the page to [help@wopee.io](mailto:help@wopee.io).

## The project was created, but exploring could not start. You can start it from the project. { #exploring-could-not-start }

**Also called:** project created but no analysis, empty project.

**Where:** a toast after **Create project and generate tests**. Commander then opens the new project.

**Cause:** the project exists, but the first analysis could not be started.

**Fix:** in the project's analysis, click **Create tests with AI**. If the step limit stopped it, see [Step limit reached](#step-limit-reached).

## We could not create the project. Try again. { #could-not-create-project }

**Also called:** create project failed, nothing happens on Create.

**Where:** a toast in **New project**. The dialog stays open with your values.

**Cause:** creating the project failed on the server.

**Fix:** click create again. If it keeps failing, send the time and your app's URL to [help@wopee.io](mailto:help@wopee.io).

## Still stuck?

Write to [help@wopee.io](mailto:help@wopee.io) with the message you see, the project name and the time, or ask in the [Community Q&A](https://github.com/orgs/Wopee-io/discussions/categories/q-a).
