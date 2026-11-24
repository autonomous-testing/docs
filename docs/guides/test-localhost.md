---
title: "Can the agent reach your app on localhost?"
description: "Can Wopee.io's agent reach your app? Check it from outside your network, what Commander's URL check means (“The app returned an error or is not reachable.”, “This address is on a private network…”), Create anyway, Starting URL unreachable. Fixes for localhost, internal DNS, non-standard ports and IP allowlists, Vercel and Netlify deployment protection (Protection Bypass for Automation), Cloudflare and CAPTCHA (test keys), basic auth, an API host or a store page instead of the app. Expose a local app with a Cloudflare quick tunnel or ngrok, dev-server allowed hosts, changing the project URL, test accounts and security."
type: How-to
updated: 16 November 2026
---

# Apps on localhost or a private network: can the agent reach your app?

Wopee.io's testing agent runs in a browser on Wopee.io's cloud runners, not on your machine. It reaches what a stranger's browser on the internet reaches, and nothing more. Give it a URL that opens from the internet and leads straight to your app: a deployed staging or preview URL, or a tunnel that exposes your local app for the time of the test.

## Check from outside your network { #check-from-outside }

Open the URL in a private browser window on a device outside your network, for example a phone with Wi-Fi off. What you see there is what the agent sees.

| What you see | What to do |
| --- | --- |
| Your app | The agent can reach it. |
| Your app's own login page | Fine: give the agent a [test account](#give-the-agent-a-test-account). See [Test an app behind a login](https://docs.wopee.io/first-green-test/test-behind-a-login/). |
| An error, a timeout or "site can't be reached" | [Localhost](#localhost), [internal DNS](#internal-dns) or a [port or IP allowlist](#port-or-ip-allowlist) |
| A Vercel or Netlify login or password page | [Vercel and Netlify deployment protection](#vercel-netlify-protection) |
| "Verify you are human", a Cloudflare check or a CAPTCHA | [Cloudflare, bot checks and CAPTCHA](#cloudflare-captcha) |
| A browser pop-up that asks for a username and password | [Basic auth](#basic-auth) |
| JSON, an API description or a 404 | [An API host instead of the app](#api-host) |
| An app store, marketplace or download page | [A store or download page instead of the app](#store-page) |

## What Commander's URL check means { #url-check }

When you paste your own app's URL into **NEW PROJECT**, Commander checks it from Wopee.io's cloud as you type. If the check fails, a warning appears under the field and ends with "The project will still be created, but exploration may not find anything."

| Warning | What it means |
| --- | --- |
| "This address is on a private network, so Wopee can't check it from the cloud. Runs from your own runner may still reach it." | The host is `localhost`, ends in `.localhost`, `.local` or `.internal`, or resolves to a private, loopback or link-local address. See [Localhost](#localhost) and [internal DNS](#internal-dns). |
| "The app returned an error or is not reachable." | No answer within 3 seconds, a host name that does not resolve on the internet, or an HTTP error status (4xx or 5xx). A basic-auth prompt (401), a bot check that answers 403 and an API root that answers 404 all land here. |
| "The URL couldn't be checked right now." | The check itself failed, not your app. Try again in a moment. |
| "Your session expired. Sign in again to continue." | Sign in to Commander again. |

The check never shows the status code or the address it saw. This is deliberate: it keeps the check from being used to probe networks. Use the [check from outside](#check-from-outside) to find the cause.

No warning does not prove the agent gets in. The check counts any redirect as an answer, so a URL that redirects to a Vercel login, a Cloudflare Access login or your company's single sign-on passes, and so does a store page. What counts is what the [check from outside](#check-from-outside) shows.

## Create anyway { #create-anyway }

The warning does not block you: **Create project and generate tests** still creates the project and starts the analysis.

- **Go ahead** when the check from outside shows your app, for example an app that takes more than 3 seconds to answer the first request after a cold start.
- **Fix the URL first** when the check from outside fails too. The agent cannot get further than your check did, and on the free plan a failed first analysis still uses up the free first analysis.
- **Not sure yet?** Open **Advanced settings** and turn off **Explore the app and generate tests**; the button changes to **Create project**. When the URL opens from outside, start with **New analysis**.

If the agent cannot open the URL, the analysis stops with **Crawling failed** › **Starting URL unreachable.** "The agent could not open the app's starting address." The callout shows the URL and the browser's error, for example `http://localhost:3000/ — net::ERR_CONNECTION_REFUSED` or `net::ERR_NAME_NOT_RESOLVED`. Fix the cause below, [update the project URL](#when-the-url-changes-update-the-project) if it changed, and click **Re-run crawl**.

## Localhost { #localhost }

On a cloud runner, `localhost` and `127.0.0.1` are the runner itself, not your laptop, and addresses in your private network (`10.x.x.x`, `172.16.x.x`–`172.31.x.x`, `192.168.x.x`, `*.local`) cannot be reached from the internet. Commander shows the private-network warning above, creates the project anyway, and the analysis stops with **Starting URL unreachable.**

Fix: use a [deployed staging or preview URL](#option-1-a-deployed-staging-or-preview-url), or expose the local app with a [Cloudflare quick tunnel](#option-2-cloudflare-quick-tunnel) or [ngrok](#option-3-ngrok).

## Internal DNS { #internal-dns }

Also called: intranet name, VPN-only host, split DNS.

A host name that resolves only inside your company network or VPN, such as `app.corp.example` or `staging.internal`, does not exist for the cloud runner. Commander warns "The app returned an error or is not reachable." (or the private-network warning, when the name resolves to a private address), and the crawl fails with `net::ERR_NAME_NOT_RESOLVED`.

Fix, from quick to permanent:

- **A staging URL on the internet**, if your team has one.
- **A tunnel from a machine inside the network**, with your IT's permission. `cloudflared` and `ngrok` forward to any address that machine can open, for example `cloudflared tunnel --url http://app.corp.example:8080`. Read [Expose it for a moment](#expose-it-for-a-moment) first.
- **For regular runs**, run tests from inside your network or connect it to Wopee.io: [Enterprise connectivity](../security/enterprise-connectivity.md).

An app with a certificate from your company's own certificate authority fails the same way even when it is reachable: the runner's browser does not trust it and stops with `net::ERR_CERT_AUTHORITY_INVALID`. Use a URL with a public certificate.

## Non-standard port or IP allowlist { #port-or-ip-allowlist }

Also called: firewall, IP whitelist, IP restriction, port 8080 or 8443.

- **Non-standard port.** A URL such as `https://staging.example.com:8443` works when that port is open to the internet. Company and cloud firewalls often open only 80 and 443. If the check from outside fails, open the port, or serve the app on 443.
- **IP allowlist.** A firewall, a WAF rule or a hosting setting that lets in only known IP addresses blocks the cloud runners. Commander warns "The app returned an error or is not reachable.", and the crawl fails with a refused connection or a timeout. Wopee.io does not publish a fixed list of cloud runner addresses here: write to [help@wopee.io](mailto:help@wopee.io) before you plan an allowlist, or see [Enterprise connectivity](../security/enterprise-connectivity.md) for running tests from inside your network.

## Vercel and Netlify deployment protection { #vercel-netlify-protection }

Also called: Vercel Authentication, "Log in to Vercel", Deployment Protection, Netlify password protection, Deploy Preview team login.

The agent opens the protection page, not your app. Because these pages often answer with a redirect, Commander's check may show no warning.

**Vercel:** Deployment Protection covers preview deployments by default. Pick one:

- Test the production domain, or a domain that Deployment Protection does not cover.
- Turn off Vercel Authentication for the project in Vercel's **Settings** › **Deployment Protection**.
- Use Vercel's [Protection Bypass for Automation](https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection/protection-bypass-automation){: target="\_blank"}. The agent cannot send custom headers, so put the secret into the project URL as query parameters:

    ```text
    https://<your-preview>.vercel.app/?x-vercel-protection-bypass=<secret>&x-vercel-set-bypass-cookie=true
    ```

    `x-vercel-set-bypass-cookie=true` makes Vercel set a cookie, so the pages the agent opens next get through too. The secret is then part of the project URL: everyone in the project sees it, and screenshots, video and traces can show it. Use a secret only for testing and revoke it in Vercel when you are done.

**Netlify:** password protection and team login on Deploy Previews stop the agent the same way. Turn them off for the deploy you test, or test a deploy without them. A `Basic-Auth` rule in Netlify's `_headers` file is [basic auth](#basic-auth).

## Cloudflare, bot checks and CAPTCHA { #cloudflare-captcha }

Also called: "Verify you are human", "Checking your browser", Turnstile, reCAPTCHA, hCaptcha, Bot Fight Mode, Cloudflare Access.

The agent runs a real browser from a cloud data centre, which bot protection often challenges. It does not solve CAPTCHAs. In an analysis you are watching, it can hand you the browser to solve one, but every run starts in a fresh browser and meets the challenge again. Remove the challenge from the environment you test:

- **A staging URL without the challenge.** On Cloudflare, keep Bot Fight Mode, Under Attack mode, challenge rules and Access logins away from the hostname you test. Bot Fight Mode is set for a whole domain: if you cannot turn it off, test on a domain without it.
- **CAPTCHA test keys** in your test environment. With these keys the widget always passes; never use them in production:

    | Provider | Test site key | Test secret key |
    | --- | --- | --- |
    | Cloudflare Turnstile | `1x00000000000000000000AA` (always passes, visible) | `1x0000000000000000000000000000000AA` |
    | Google reCAPTCHA v2 | `6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI` | `6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe` |
    | hCaptcha | `10000000-ffff-ffff-ffff-000000000001` | `0x0000000000000000000000000000000000000000` |

    The reCAPTCHA test widget shows a warning that it is for testing only; reCAPTCHA v3 has no test keys, so create a separate key for the test environment. Sources: [Turnstile](https://developers.cloudflare.com/turnstile/troubleshooting/testing/){: target="\_blank"}, [reCAPTCHA](https://developers.google.com/recaptcha/docs/faq){: target="\_blank"}, [hCaptcha](https://docs.hcaptcha.com/#integration-testing-test-keys){: target="\_blank"}.

- **A switch in your app** that turns the CAPTCHA off in the test environment.

## Basic auth { #basic-auth }

Also called: HTTP authentication, the browser's "Sign in" pop-up, `.htpasswd`, Basic-Auth.

When the browser itself asks for a username and password before any page loads, the server uses HTTP authentication. Commander warns "The app returned an error or is not reachable." because the server answers 401.

Give the agent's browser the credentials as project variables. Go to **More** › **Settings** › **Environment Variables** and add:

- `BASIC_AUTH_USER`: the username
- `BASIC_AUTH_PASSWORD`: the password

The browser answers the server's prompt with them on every run. They also work for NTLM (Windows sign-in), with the user as `DOMAIN\user` or `user@domain`. Ignore the warning and [create the project anyway](#create-anyway), or create it with **Explore the app and generate tests** off, add the variables, then start **New analysis**.

## An API host instead of the app { #api-host }

The agent tests the app the way a person uses it: in a browser. A URL such as `https://api.example.com`, `/graphql` or `/swagger` shows JSON, an API description or a 404, and there is nothing to explore. Commander warns "The app returned an error or is not reachable." when the API answers 404 at that address; JSON with a 200 passes the check, and the agent still finds no app.

Fix: paste the address where people open your app in a browser, usually the front end, such as `https://app.example.com`. To call an API inside a test, see the [HTTP Request Tool](http-tools.md).

## A store or download page instead of the app { #store-page }

A page on the App Store, Google Play, the Chrome Web Store, a marketplace or a download site belongs to that store, not to you. The agent would test the store's page, and stores often block automated browsers. The URL check passes, so Commander does not warn you.

Fix: paste the URL of your web app itself. Wopee.io's agent tests web apps in a browser; for a mobile or desktop app, [contact us](mailto:help@wopee.io).

## Test only apps you own or are authorised to test { #own-apps-only }

The agent clicks, fills in and submits forms, and records everything it sees. Point it only at apps that you or your company own, or that you have the owner's permission to test. Do not point it at someone else's site, a social network, a competitor or a copy of someone's login page. Wopee.io's [Terms of Use](https://wopee.io/terms-and-conditions/){: target="\_blank"} require you to have the permissions needed for what you test and the data you use.

Prefer a staging environment to production: the agent creates real records, such as sign-ups, orders and e-mails. Use [test data and a test account](#expose-it-for-a-moment).

## Pick an option

| Option | Best for | Account | URL after a restart |
| --- | --- | --- | --- |
| [Deployed staging or preview URL](#option-1-a-deployed-staging-or-preview-url) | Repeat runs, scheduled Test Plans, CI, a team | Your hosting | Stays the same |
| [Cloudflare quick tunnel](#option-2-cloudflare-quick-tunnel) | A first analysis of a local app, in a few minutes | None | New on every start |
| [ngrok](#option-3-ngrok) | A local app at an address that stays the same | Free ngrok account | Stays the same |

Whichever you pick, [check the URL from outside your network](#check-from-outside) before you start the analysis.

## Option 1: A deployed staging or preview URL

Any URL that opens from the internet works: a staging server, a preview deployment from your pull request, or a test environment. Paste it into Commander when you create the project, or sign up with it:

```text
https://cmd.wopee.io/signup?url=<your-app-url>
```

The agent must reach the app itself, not a login page or a bot check in front of it: see [Vercel and Netlify deployment protection](#vercel-netlify-protection) and [Cloudflare, bot checks and CAPTCHA](#cloudflare-captcha).

Your app's own login is fine: give the agent a [test account](#give-the-agent-a-test-account).

## Option 2: Cloudflare quick tunnel

A quick tunnel needs no account and no domain. It gives your local app a random public `https://….trycloudflare.com` address until you stop it.

1. Start your app. With Vite:

    ```shell
    npm run dev
    ```

    It serves `http://localhost:5173`. Use your own port in the next steps.

2. Install `cloudflared`:

    === "macOS"

        ```shell
        brew install cloudflared
        ```

    === "Windows"

        ```shell
        winget install --id Cloudflare.cloudflared
        ```

    === "Linux"

        Install the package for your distribution from [Cloudflare's downloads page](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/){: target="\_blank"}.

3. In a second terminal, start the tunnel:

    ```shell
    cloudflared tunnel --url http://localhost:5173
    ```

    After a few seconds it prints your URL in a box:

    ```text
    Your quick Tunnel has been created! Visit it at …
    https://<four-random-words>.trycloudflare.com
    ```

4. Wait a few more seconds, then open the URL in your own browser. When your app loads, paste the URL into Commander: into **NEW PROJECT**, into the sign-up link above, or as the new [project URL](#when-the-url-changes-update-the-project). Your browser shows a host-not-found error? You opened it before the address existed; wait a minute and reload. A "Blocked request" or "Invalid Host header" page means your dev server needs the [tunnel host allowed](#allow-the-tunnel-host-in-your-dev-server).

5. Leave both terminals open until the analysis and its runs are finished. Press Ctrl+C in the tunnel terminal to stop it; the URL stops working.

!!! tip "Print only the URL"

    The full log is long. This prints just the address as soon as it exists:

    ```shell
    cloudflared tunnel --url http://localhost:5173 2>&1 | grep --line-buffered -o 'https://[a-z0-9-]*\.trycloudflare\.com'
    ```

    Keep `--line-buffered`; without it nothing is printed.

Quick tunnels are for testing: they have no uptime guarantee, allow up to 200 requests at a time and do not support Server-Sent Events. For an app that streams responses, such as an AI chat or a live dashboard, use ngrok or a deployed URL. For an address that stays the same, Cloudflare also offers named tunnels on your own domain (Cloudflare account required).

## Option 3: ngrok

ngrok needs a free account. Its free plan gives you one dev domain, `<your-name>.ngrok-free.dev`, which stays the same on every start, so you set the project URL once.

1. Create an account at [ngrok.com](https://ngrok.com){: target="\_blank"} and copy your authtoken from its dashboard.
2. Install ngrok and add the token (macOS shown; other systems: [ngrok's getting started](https://ngrok.com/docs/getting-started/){: target="\_blank"}):

    ```shell
    brew install ngrok
    ngrok config add-authtoken <your-authtoken>
    ```

3. Start your app, then the tunnel:

    ```shell
    ngrok http 5173
    ```

    The **Forwarding** line shows your URL.

!!! warning "The free plan shows a warning page before your app"

    On the free plan, ngrok shows browsers a page that starts with "You are about to visit…" and has a **Visit Site** button. You can skip it with the `ngrok-skip-browser-warning` header, but Wopee.io's agent cannot send custom headers and starts every run in a fresh browser. Every analysis and every run starts on that page, not on your app. Use a [Cloudflare quick tunnel](#option-2-cloudflare-quick-tunnel), a paid ngrok plan or a deployed URL instead. The page also shows your public IP address.

The free plan also limits traffic to 20,000 requests and 1 GB a month. An analysis loads many pages and their assets, so a heavy app uses up the quota faster.

## Allow the tunnel host in your dev server

Dev servers answer only to `localhost` by default and reject requests for another hostname. Through a tunnel, the agent then sees an error text instead of your app. Add the tunnel domains, then **restart the dev server**: a running server does not pick up the change. The tunnel can stay up while you restart, with the same URL.

=== "Vite"

    Without this, the page says `Blocked request. This host ("….trycloudflare.com") is not allowed.`

    ```js title="vite.config.js"
    import { defineConfig } from "vite";

    const tunnelHosts = [
      ".trycloudflare.com",
      ".ngrok-free.app",
      ".ngrok-free.dev",
      ".ngrok.app",
    ];

    export default defineConfig({
      server: { allowedHosts: tunnelHosts },
      preview: { allowedHosts: tunnelHosts },
    });
    ```

    A leading dot allows the domain and all its subdomains, so a new quick-tunnel name works without another change. `preview` covers `vite preview`.

=== "Next.js"

    ```js title="next.config.js"
    module.exports = {
      allowedDevOrigins: ["*.trycloudflare.com", "*.ngrok-free.dev"],
    };
    ```

    Hostnames only, without `https://` or a port. `next start` (a production build) does not need it.

=== "webpack-dev-server"

    Without this, the page says `Invalid Host header`.

    ```js title="webpack.config.js"
    module.exports = {
      devServer: {
        allowedHosts: [".trycloudflare.com", ".ngrok-free.dev"],
      },
    };
    ```

Do not set `allowedHosts: true` or `'all'`: it lets every hostname through, and Vite and webpack warn that this opens your dev server to DNS rebinding attacks. Backend frameworks have the same kind of list, for example `ALLOWED_HOSTS` in Django and `config.hosts` in Rails.

!!! tip "Tunnel a production build"

    A production build loads faster for the agent, has no hot-reload noise and is closer to what you ship. With Vite, build and serve it, then tunnel port 4173 from a second terminal:

    ```shell
    npm run build && npm run preview
    ```

    ```shell
    cloudflared tunnel --url http://localhost:4173
    ```

## Make the app work from another address

- **API calls to `localhost`.** If the front end calls an absolute address such as `http://localhost:8080/api`, the agent's browser calls the runner's own `localhost`: the page loads, the data does not. Call the API with a relative path and a dev proxy (Vite `server.proxy`, Next.js rewrites), so one tunnel carries both. Or start a second tunnel for the API and point the app at it.
- **Social login (OAuth).** The provider sends the browser back only to redirect URLs you registered. Add the tunnel address there, or let the agent sign in with an e-mail and password test account. An address that stays the same (ngrok, a named Cloudflare tunnel) saves registering a new one every time.

## Give the agent a test account

Create a test account in your local app and give it to the agent as variables:

- **For one analysis:** in **Variables & Knowledge**, click **Edit** next to the variables and fill in `TESTING_USERNAME` and `TESTING_PASSWORD`.
- **For the whole project:** go to **More** › **Settings** › **Environment Variables**.

The agent receives the names of the variables, never their values. Details: [Variables](../concepts/intent-and-scripted-tests.md#variables). Tell the agent about the app itself in the [project context](project-context.md).

## Keep the tunnel up for the whole job

- **Until the runs finish, not only the analysis.** An analysis takes several minutes, can wait in a queue first, and runs the tests it generates. Keep the app and the tunnel running, and your computer awake, until the last run is done. On a Mac, `caffeinate -i cloudflared tunnel --url http://localhost:5173` keeps it from sleeping while the tunnel runs.
- **Every later run opens the project URL again.** A tunnel that is closed, or a laptop that is asleep, fails every run and every scheduled Test Plan. For schedules and CI, use a [deployed URL](#option-1-a-deployed-staging-or-preview-url).
- **A tunnel can answer without your app.** If the app stops while the tunnel runs (Cloudflare "502: Bad gateway") or ngrok is offline (`ERR_NGROK_3200` "The endpoint is offline."), the agent gets that error page and reports on it instead of your app. A stopped quick tunnel's address no longer exists, so the run fails as unreachable.

## When the URL changes, update the project

A quick tunnel gets a new address on every start, so update the project before the next analysis or run:

1. In the project, go to **More** › **Settings** › **General**. Next to **Url**, click **Change**.
2. In **Danger Zone** › **Change Project URL**, paste the new address into **Project URL** and click **Update URL**. Only project admins see **Danger Zone**.
3. Open the analysis and click **Re-run crawl**. It uses the new URL.

The project URL applies to every run. Steps that use a relative path follow the new URL; steps that saved a full address with the old host keep opening the old one. For repeat runs, an address that stays the same saves this work. The MCP tools cannot change the project URL: change it in Commander.

## Expose it for a moment

While a tunnel runs, anyone with the URL can open your app. The ngrok free dev domain is fixed, so it is not a secret that changes.

- **Tunnel one port: the app.** Never a database, an admin console, a debug port or a whole machine.
- **Use test data and a test account.** Everything the agent sees is recorded in screenshots, video and a trace, and kept in the project.
- **Allow only the tunnel domains** in your dev server, never every host.
- **Prefer a production build** to a dev server, which serves source maps and dev-only endpoints.
- **Stop the tunnel** with Ctrl+C when the analysis and its runs are done.
- **For anything permanent**, such as scheduled runs, CI or an app inside a company network, use a deployed staging URL or [Enterprise connectivity](../security/enterprise-connectivity.md).

## Troubleshooting

| What you see | Cause | Fix |
| --- | --- | --- |
| "This address is on a private network, so Wopee can't check it from the cloud. Runs from your own runner may still reach it." when you create the project | The URL is `localhost`, a private address or a name that resolves to one | [Localhost](#localhost), [internal DNS](#internal-dns) |
| "The app returned an error or is not reachable." when you create the project | No answer within 3 seconds, a name that does not resolve on the internet, or an HTTP error status | [Check from outside](#check-from-outside), then the matching section; [Create anyway](#create-anyway) if your app opens there |
| "The URL couldn't be checked right now." | Commander's check failed, not your app | Try again in a moment |
| **Crawling failed** › **Starting URL unreachable.** with `net::ERR_CONNECTION_REFUSED` or `net::ERR_NAME_NOT_RESOLVED` | The project URL is private or internal, blocked by a firewall, or a tunnel address that no longer exists | Fix the cause, [update the project URL](#when-the-url-changes-update-the-project), click **Re-run crawl** |
| **Starting URL unreachable.** with `net::ERR_CERT_AUTHORITY_INVALID` | A certificate from your own certificate authority | Use a URL with a public certificate ([internal DNS](#internal-dns)) |
| **Crawling failed** › **Starting URL is not valid.** | The project URL is not a full web address | Fix it in the project settings, include `https://` |
| `Blocked request. This host (…) is not allowed.` | Vite's host check | Add the tunnel domains to `allowedHosts` and restart the dev server |
| `Invalid Host header` | webpack-dev-server's host check | Add the tunnel domains to `devServer.allowedHosts` |
| Cloudflare "502: Bad gateway" | The app is not running, or the port in `--url` is wrong | Start the app, check the port |
| Host not found right after the tunnel started | The address was opened before it existed | Wait a minute and reload |
| "You are about to visit…" with a **Visit Site** button | ngrok free-plan warning page | Use a Cloudflare quick tunnel, a paid ngrok plan or a deployed URL |
| `ERR_NGROK_3200` "The endpoint is offline." | ngrok is not running | Start `ngrok http <port>` again |
| The page loads, but lists and data stay empty | The app calls an API on `localhost` | Use a relative API path with a dev proxy, or tunnel the API too |
| A Vercel or Netlify login or password page | Deployment protection | [Vercel and Netlify deployment protection](#vercel-netlify-protection) |
| "Verify you are human", a Cloudflare check or a CAPTCHA | Bot protection | [Cloudflare, bot checks and CAPTCHA](#cloudflare-captcha) |
| The browser asks for a username and password before any page | HTTP basic auth | Set `BASIC_AUTH_USER` and `BASIC_AUTH_PASSWORD` ([basic auth](#basic-auth)) |
| JSON, an API description or a 404 | The project URL is an API host | [Use the app's address](#api-host) |

## Watch it done

<div class="yt-facade"><a href="https://youtu.be/2xLDkZYCiWE" data-yt="2xLDkZYCiWE" data-title="How to test localhost with a cloud testing agent"><img src="https://i.ytimg.com/vi/2xLDkZYCiWE/hqdefault.jpg" alt="" width="480" height="360" loading="lazy"><span class="yt-facade__play">Play: test an app on localhost with a tunnel, 2:00</span></a></div>

A local app gets a public address with one command, and Wopee.io's agent analyzes it. 2:00.
{ .wo-video-caption }

## Related pages

- [Getting started](../ai-agent.md): create a project and run the first analysis
- [Project context](project-context.md): tell the agent how your app works
- [Variables](../concepts/intent-and-scripted-tests.md#variables): test accounts and other values the agent types
- [Enterprise connectivity](../security/enterprise-connectivity.md): permanent access to apps inside a company network
- [Test an app behind a login](https://docs.wopee.io/first-green-test/test-behind-a-login/): test accounts, sign-in steps and one-time codes
- [Commander troubleshooting](https://docs.wopee.io/troubleshooting/commander/): other messages in Commander and what to do
