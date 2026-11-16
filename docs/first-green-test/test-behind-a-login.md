---
title: Test an app behind a login
description: "Give the Wopee.io testing agent a test account: TESTING_USERNAME and TESTING_PASSWORD under More › Settings › Environment Variables, which account to use, several roles, Take control, placeholders typed literally, SSO and MFA, and saved sessions (auth.json)."
type: How-to
updated: 16 November 2026
---

# Test an app behind a login

When your app asks for a sign-in, the testing agent needs a test account. Without one it explores only the pages a visitor can see and writes tests about the sign-in page. Give it the account once, as two project variables, and every analysis and every test run signs in with it.

!!! info "For product owners and CTOs"

    Create one account for testing, the way you would for a new tester. The agent receives only the variable names. The values are filled in when the run types them, so they stay out of the agent's prompt and out of the generated tests.

## Add a test account { #add-a-test-account }

_Also called: credentials, login details, test user, username and password._

1. Open the project and go to **More** › **Settings** › **Environment Variables**. If you pinned **Settings** to the top bar, use that instead.
2. Click **Add** and type `TESTING_USERNAME` as the key. Enter the user name or e-mail address as the value.
3. Click **Add** again and type `TESTING_PASSWORD` as the key. Enter the password as the value.
4. Click **Save**.

Type the keys exactly as shown, in capital letters. The agent signs in only when both are set.

The password field is masked: Commander shows dots, and the eye icon next to the value shows it. The user name is shown in plain text. The agent never sees either value: it writes `${TESTING_USERNAME}` and `${TESTING_PASSWORD}`, and the value is filled in when the run types it. A typed password is also removed from the run's logs.

These project variables are defaults for every analysis. To use another account for one analysis only, open **Variables & Knowledge** in that analysis, click **Edit** next to the variables and fill in `TESTING_USERNAME` and `TESTING_PASSWORD` there. A value set in the analysis overrides the project value.

!!! warning "Do not put the password in Test instructions"

    The **NEW PROJECT** form has no fields for a user name or password, so the first analysis always starts without them. If you write the password into **Test instructions**, the test generator can copy it into the generated tests, and the tests are stored in your project's repository. Add the variables instead, then follow [After you add it](#after-you-add-it).

## After you add it { #after-you-add-it }

_Also called: re-run, retry, run the analysis again._

**Re-run the existing tests first.** Tests that stopped at the sign-in page, or typed `${TESTING_USERNAME}` into it, now sign in. Re-running a test costs only the steps of that test.

Start a **new analysis** when you want tests for the pages behind the login. The first analysis could not get past the sign-in page, so it did not write tests for them. A new analysis explores the app again, signs in and generates new tests.

!!! warning "A new analysis uses free-plan steps"

    On the free plan, the testing agent has 50 steps every 5 hours, counted across your projects. Every action the agent takes in the browser counts as one step, and a new run is refused when fewer than 5 steps are left. Only your very first analysis is free, together with the tests it runs. It stays used even when it stopped at a login, and an analysis of a demo app uses it too. A new analysis explores the whole app again, so its exploration and the tests it runs all count against the 50 steps.

## Which account to use { #which-account }

_Also called: test user, service account, dedicated account._

Use an account made for testing:

- **A dedicated test user.** Not your personal account: tests change data, and a test that signs out or changes settings affects whoever else uses the account.
- **Not an admin account**, unless admin features are what you test. Tests run as this user and can do everything it can do.
- **No MFA, no SSO-only sign-in.** The account must sign in with a user name and password alone. See [Google sign-in, SSO and MFA](#sso-mfa).
- **A stable password.** If the password expires or the account gets locked, every run stops at the login. When the app rejects the account, the analysis shows _"Login failed."_ with _"The agent could not sign in with the configured credentials."_
- **Safe test data.** Prefer a staging or test environment. On production, use an account whose orders, messages and payments nobody acts on.

## Several roles { #several-roles }

_Also called: admin and customer, two users, multiple accounts, user roles._

`TESTING_USERNAME` and `TESTING_PASSWORD` are the default account. For a second role, add another pair of variables under **More** › **Settings** › **Environment Variables**, for example `ADMIN_USERNAME` and `ADMIN_PASSWORD`. A key that contains `PASSWORD` is masked like the default one.

Then name the pair where it is needed:

- **In a test:** write the variables into the test's description, for example _Sign in as the admin with ${ADMIN_USERNAME} and ${ADMIN_PASSWORD}_. A test that names its own sign-in uses it instead of the default account.
- **For the whole project:** list each role and its variables in the [project context](../guides/project-context.md), under **Users and sign-in**. The template there has both roles filled in.

Create every variable before the first run. A `${NAME}` that does not exist as a variable is not filled in (see [The test typed ${TESTING_USERNAME}](#placeholder-typed-literally)). More on variables: [Variables](../concepts/intent-and-scripted-tests.md#variables).

## Take control is not saved for later runs { #take-control-is-not-saved }

_Also called: I logged in for the agent, hand-over, manual login, the tests still fail at login._

During an analysis you can click **Take control**, sign in yourself in the live browser and click **Resume agent**. The agent can ask you for this too, for example at a CAPTCHA or a one-time code. That sign-in helps only the run you are watching.

What you type during Take control is not stored. The generated tests run later without you, in a new browser, and they need the account as [variables](#add-a-test-account) or a [saved session](#auth-json). Without either, they stop at the sign-in page again.

## The test typed ${TESTING_USERNAME} into the form { #placeholder-typed-literally }

_Also called: placeholder typed literally, `${TESTING_PASSWORD}` in the field, "Username and password do not match", tests fail at login._

The generated test refers to the account as `${TESTING_USERNAME}` and `${TESTING_PASSWORD}`, but the project has no variables with these names. The run then types the text `${TESTING_USERNAME}` itself into the user name field, and the app rejects it. The run's report usually says that the variable was not configured and that the placeholder was typed as written.

To fix it:

1. [Add the test account](#add-a-test-account), with the keys spelled exactly as in the test.
2. Re-run the failed tests. They now sign in.

The same happens with any other `${NAME}`: a name that is not a project or analysis variable is typed as written. A variable that exists but has no value is typed as written too, so the field never ends up silently empty.

## Google sign-in, SSO and MFA { #sso-mfa }

_Also called: Sign in with Google, Microsoft sign-in, Okta, single sign-on, 2FA, two-factor, one-time code, OTP, TOTP, authenticator app, SMS code, magic link, passwordless._

The agent signs in by typing a user name and password into your app's form. What works today:

| Sign-in                                     | Works in test runs?      | What to do                                                                                                             |
| ------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| User name and password                      | Yes                      | [Add a test account](#add-a-test-account).                                                                             |
| Google, Microsoft or another SSO button     | Not with variables       | Give the test user a password login if your app allows it. Otherwise upload a [saved session](#auth-json).             |
| MFA with an authenticator app (TOTP)        | No                       | Switch MFA off for the test user, or upload a [saved session](#auth-json). The agent cannot generate the codes.        |
| One-time code by SMS or e-mail, magic links | No                       | Switch it off for the test user, or upload a [saved session](#auth-json). The agent cannot read your phone or mailbox. |
| CAPTCHA on the sign-in page                 | No                       | Switch it off on your test environment, or use your CAPTCHA provider's test keys there.                                |
| Windows sign-in (Kerberos)                  | Self-hosted runners only | See [Windows sign-in](#windows-sign-in).                                                                               |
| Login through your own API                  | Yes, inside a test       | See [Log in through your API](#api-login).                                                                             |

During a live analysis, the agent can hand the browser over to you for a code or a CAPTCHA: you type and submit it, then click **Resume agent**. This helps only that analysis, as described in [Take control is not saved](#take-control-is-not-saved). Unattended test runs have nobody to hand over to.

!!! note "No TOTP secret variable"

    A variable named `TESTING_TOTP_SECRET` does not produce codes. If a test uses `${TESTING_TOTP_SECRET}`, the run types the secret itself, not a 6-digit code, and the app rejects it.

## Saved browser session (auth.json) { #auth-json }

_Also called: Authentication tab, storage state, cookies, session file, logged-in state._

**More** › **Settings** › **Authentication** is not where credentials go. It holds a saved browser session: a Playwright storage state file (`auth.json`) with the cookies and local storage of a signed-in browser. With it, the agent starts already signed in and never sees the sign-in page.

Use it when the test user cannot sign in with a password alone, for example with SSO or MFA. Keep in mind:

- **Sessions expire.** When the app's session ends, the tests land on the sign-in page again. Capture a new file and upload it again.
- **It skips the sign-in page.** Tests that check the sign-in itself need the [variables](#add-a-test-account).
- **Only project admins can upload it.**

How to capture the file with Playwright and upload it at project, analysis or user story level: [Browser local storage](../guides/browser-local-storage.md).

## Log in through your API { #api-login }

_Also called: token login, bearer token, API authentication, session cookie from the API._

A test can sign in by calling your login API instead of filling the form. An HTTP request step can keep a value from the response: a response header, one cookie, or a field of the JSON body. It keeps the value under a name such as `AUTH_TOKEN`, and later steps use it as `${AUTH_TOKEN}` to set a cookie, fill a field, open a page or send the next request. The agent learns only that a value was captured and how long it is, never the value itself.

The request can go to an API on a different domain than the app, as long as the step names that address. Send the account from variables, for example `${TESTING_USERNAME}` and `${TESTING_PASSWORD}` in the request body. How HTTP request steps work: [HTTP Request Tool](../guides/http-tools.md).

## Windows sign-in (Kerberos) { #windows-sign-in }

_Also called: Windows SSO, Kerberos, Active Directory, integrated authentication, domain account._

Some company apps sign you in with your Windows account and never show a sign-in form. On **hybrid and self-hosted installations**, where the test runners sit inside your network, runs can test them: set the domain account as `KERBEROS_*` project or analysis variables, and the runner gets a Kerberos ticket before the browser starts. The app opens already signed in, and the password never reaches the agent. If the sign-in fails, the run stops with the reason, such as a wrong password, a locked account or an unreachable domain controller.

The cloud runners at [cmd.wopee.io](https://cmd.wopee.io) cannot reach your domain controller. To run your tests inside your network, see the self-hosted runner in [Enterprise Connectivity](../security/enterprise-connectivity.md#option-3-self-hosted-runner) or write to [help@wopee.io](mailto:help@wopee.io).

## Related topics

- [Read your first results](read-your-first-results.md)
- [Variables](../concepts/intent-and-scripted-tests.md#variables)
- [Project context](../guides/project-context.md)
- [Browser local storage](../guides/browser-local-storage.md)
- [POM example - Login](../concepts/pom-login-example.md)
