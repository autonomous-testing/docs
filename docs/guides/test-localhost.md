---
title: Test an app that runs on localhost
description: "Test an app on localhost or in a private network with Wopee.io: use a deployed staging or preview URL, or expose it for a moment with a Cloudflare quick tunnel or ngrok. Dev-server allowed hosts (Vite, Next.js, webpack), the ngrok warning page, keeping the tunnel up, changing the project URL, test accounts and security."
type: How-to
updated: 16 November 2026
---

# Test an app that runs on localhost

Wopee.io's testing agent runs in a browser on Wopee.io's cloud runners, not on your machine. Give it a public URL and the analysis works right away: a deployed staging or preview URL, or a tunnel that exposes your local app for the time of the test.

## Why localhost does not work

On a cloud runner, `localhost` and `127.0.0.1` are the runner itself, not your laptop, and addresses in your private network (`10.x.x.x`, `192.168.x.x`, `*.local`, intranet names) cannot be reached from the internet. When you create a project with such a URL, Commander warns "This address is on a private network, so Wopee can't check it from the cloud." and creates the project anyway. The analysis then stops with **Crawling failed** › **Starting URL unreachable** and an error such as `http://localhost:3000/ — net::ERR_CONNECTION_REFUSED`.

## Pick an option

| Option | Best for | Account | URL after a restart |
| --- | --- | --- | --- |
| [Deployed staging or preview URL](#option-1-a-deployed-staging-or-preview-url) | Repeat runs, scheduled Test Plans, CI, a team | Your hosting | Stays the same |
| [Cloudflare quick tunnel](#option-2-cloudflare-quick-tunnel) | A first analysis of a local app, in a few minutes | None | New on every start |
| [ngrok](#option-3-ngrok) | A local app at an address that stays the same | Free ngrok account | Stays the same |

Whichever you pick, open the URL once in a private browser window on a device outside your network, for example a phone on mobile data. What you see there is what the agent sees.

## Option 1: A deployed staging or preview URL

Any URL that opens from the internet works: a staging server, a preview deployment from your pull request, or a test environment. Paste it into Commander when you create the project, or sign up with it:

```text
https://cmd.wopee.io/signup?url=<your-app-url>
```

The agent must reach the app itself, not a login page in front of it:

- **Vercel:** Deployment Protection covers preview deployments by default and shows a Vercel login. Turn it off for the deployment you test, or test a domain without it.
- **Netlify:** password protection and team login on Deploy Previews stop the agent the same way.
- **Cloudflare:** an Access login or a bot check (Bot Fight Mode, Turnstile) on the hostname blocks the agent's browser. Keep them off the test hostname.

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
| "This address is on a private network, so Wopee can't check it from the cloud." when you create the project | The URL is `localhost` or a private address | Use a tunnel or a deployed URL, then [change the project URL](#when-the-url-changes-update-the-project) |
| **Crawling failed** › **Starting URL unreachable** with `net::ERR_CONNECTION_REFUSED` or `net::ERR_NAME_NOT_RESOLVED` | The project URL is private, or a tunnel address that no longer exists | Start the tunnel, update the project URL, click **Re-run crawl** |
| `Blocked request. This host (…) is not allowed.` | Vite's host check | Add the tunnel domains to `allowedHosts` and restart the dev server |
| `Invalid Host header` | webpack-dev-server's host check | Add the tunnel domains to `devServer.allowedHosts` |
| Cloudflare "502: Bad gateway" | The app is not running, or the port in `--url` is wrong | Start the app, check the port |
| Host not found right after the tunnel started | The address was opened before it existed | Wait a minute and reload |
| "You are about to visit…" with a **Visit Site** button | ngrok free-plan warning page | Use a Cloudflare quick tunnel, a paid ngrok plan or a deployed URL |
| `ERR_NGROK_3200` "The endpoint is offline." | ngrok is not running | Start `ngrok http <port>` again |
| The page loads, but lists and data stay empty | The app calls an API on `localhost` | Use a relative API path with a dev proxy, or tunnel the API too |
| A Vercel, Netlify or Cloudflare login page | Deployment protection or an access policy | Turn it off for the tested deployment or hostname |

<!--
VIDEO EMBED: add once the explainer is public on YouTube and the website PR that adds wopee.io/videos/<slug>/ has merged (same pattern as docs/guides/wopee-mcp/codex.md).
Uncomment, replace <ID>, <title>, <m:ss> and <slug>, and add the link to "More walkthroughs" in docs/index.md.

## Watch it done

<div class="yt-facade"><a href="https://youtu.be/<ID>" data-yt="<ID>" data-title="<title>"><img src="https://i.ytimg.com/vi/<ID>/hqdefault.jpg" alt="" width="480" height="360" loading="lazy"><span class="yt-facade__play">Play: Test an app on localhost with a tunnel, <m:ss></span></a></div>

A local app gets a public address with one command, and Wopee.io's agent analyzes it. <m:ss>. [Video page](https://wopee.io/videos/<slug>/){: target="\_blank"}
{ .wo-video-caption }
-->

## Related pages

- [Getting started](../ai-agent.md): create a project and run the first analysis
- [Project context](project-context.md): tell the agent how your app works
- [Variables](../concepts/intent-and-scripted-tests.md#variables): test accounts and other values the agent types
- [Enterprise connectivity](../security/enterprise-connectivity.md): permanent access to apps inside a company network
