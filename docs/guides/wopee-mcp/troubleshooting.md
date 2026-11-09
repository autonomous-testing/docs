---
title: Troubleshooting the Wopee.io MCP server
description: Fix Wopee.io MCP server problems - server not visible until restart, GUI apps without shell environment variables, disabled or untrusted project servers, AUTH_ERROR, Not Authorised!, NETWORK_ERROR, USAGE_LIMIT_EXCEEDED after the first analysis, localhost URLs.
type: How-to
updated: 9 November 2026
---

# Troubleshooting the Wopee.io MCP server

Find the message or symptom, then apply the fix. The server returns errors as normal text, so your client may show the tool call as successful while the answer contains an error such as `[AUTH_ERROR]`. Client-specific problems are also on each [client's page](index.md#add-it-to-your-agent).

## The server does not show up

### Not visible until restart

Most clients load MCP servers when they start. A server added in a running session, or values exported after the client started, are not picked up.

- **Claude Code:** quit, then start `claude` again from the terminal that has `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID`. For a project server in `.mcp.json`, choose **Use this MCP server** when Claude Code asks. Check with `/mcp`.
- **Cursor:** open **Customize** › **MCPs** and check the `wopee` entry.
- **VS Code:** open `.vscode/mcp.json` and click **Start** (or **Restart**) above the entry.
- **Codex, Copilot CLI, Gemini CLI, Devin Desktop:** restart the app or CLI from a terminal that has the values.

### GUI apps do not see your shell environment

Apps started from the Dock, the Start menu or a launcher do not get the variables you exported in a terminal. A reference such as `${env:WOPEE_API_KEY}` then resolves to nothing, and every call returns `[AUTH_ERROR] WOPEE_API_KEY or WOPEE_AUTH_TOKEN must be set`.

- **Cursor, VS Code:** use `envFile` with a git-ignored `.env` in the project root, or start the editor from the terminal that has the values (for VS Code `code .`).
- **Devin Desktop:** start it from a terminal, or use `${file:...}`, see [Devin Desktop](devin-desktop-windsurf.md).
- **Claude Desktop:** put the real values into `env` in `claude_desktop_config.json`, a user-level file outside your repository, then quit and restart Claude Desktop. See [Other MCP clients](other-clients.md#claude-desktop).

The same applies to `npx` itself: a GUI app may not find Node.js from a version manager, see `spawn npx ENOENT` below.

### Project servers start disabled or need trust

Several clients do not start a server from a project file until you allow it:

| Client | What you see | Fix |
| --- | --- | --- |
| Cursor | The server is listed as **Disabled** | Open the server in **Customize** › **MCPs** and switch on the `.cursor/mcp.json` source |
| Gemini CLI | The server stays disconnected | Trust the folder with `gemini trust` |
| OpenAI Codex | The project `.codex/config.toml` is ignored | Codex reads project config only in trusted projects; trust the project, or use `~/.codex/config.toml` |
| Copilot CLI | The project `.mcp.json` or `.github/mcp.json` is not loaded | Project config loads only in trusted folders; trust the folder |
| Visual Studio | The `wopee` tools are not offered | The tools of a new server are disabled by default; enable them in the Copilot Chat tools picker |

## Error messages

| Symptom or message | Cause | Fix |
| --- | --- | --- |
| `[AUTH_ERROR] WOPEE_API_KEY or WOPEE_AUTH_TOKEN must be set` | The server started without the key | Set `WOPEE_API_KEY` in the environment the agent starts from, or check the variable reference syntax for your client. Restart the agent |
| `WOPEE_PROJECT_UUID is not set` or `Failed to parse input: WOPEE_PROJECT_UUID is not set` | The project UUID is missing | Add `WOPEE_PROJECT_UUID` to the server's `env` and restart |
| `[GRAPHQL_ERROR] Not Authorised!` | Wrong or deleted key, a key from another project, or a chat tool | Copy the UUID and a new key from the same project's **API Keys** screen, see [Find your API key and project UUID](../api-keys.md) |
| `Not Authorised!` behind a company gateway with a valid key | The gateway drops headers with underscores; the server sends the key as `api_key` | Ask your network team to allow the `api_key` header |
| `[NETWORK_ERROR] ...` on every call, and your config has `WOPEE_API_URL` | The variable is set to an empty string, which is not replaced by the default | Remove `WOPEE_API_URL`, or set it to the value from the **API Keys** screen |
| `[NETWORK_ERROR]` or timeouts in a corporate network | Proxy | Set `HTTPS_PROXY` in the server's `env` |
| `unable to get local issuer certificate`, `self-signed certificate` | TLS inspection | Set `NODE_EXTRA_CA_CERTS` to your company's root certificate (PEM). Do not turn off TLS verification |
| Server fails to start, errors about `undici`, `fetch` or engine versions | Node.js too old | Install Node.js 20.18 or newer (22 recommended) |
| `npx: command not found` or `spawn npx ENOENT` | The client does not see your Node.js installation (common with version managers and GUI apps) | Use the full path to `npx` in `command` (`which npx`, on Windows `where npx`), or start the editor from a terminal |
| Server not listed, no error | Invalid JSON (for example a trailing comma), wrong top-level key, or no restart | Validate the file, check `mcpServers` / `servers` / `mcp` for your client, restart the agent |
| `[HTTP_ERROR] HTTP 503` | Wopee.io API update in progress | Retry in a few minutes |
| VS Code shows **Error** next to the server before the first message | The chat session type is **Copilot** | Switch the session type to **Local** under the chat input, then click **Start** |
| The agent reports a started run but no verdict | Runs take minutes; some agents stop polling early (Copilot after about 45 seconds) | Ask "Check the result now" |
| `[RATE_LIMITED]` or "rate limit" | More than one dispatch in 10 seconds | Wait; dispatch tools retry automatically |
| `Multiple test cases are not allowed for non-premium users` | Several test cases in one dispatch on a plan below Premium | Dispatch one test case per call |
| `[USAGE_LIMIT_EXCEEDED]` or `Usage limit reached` | The plan's usage limit is reached | See [Usage limit right after the first analysis](#usage-limit-right-after-the-first-analysis) |
| `Failed to create GitHub issue. Make sure the project has a GitHub repository linked.` | No connected repository, or the GitHub App lacks permissions | Connect a repository; the Wopee.io GitHub App needs Issues (read and write) and, for screenshots, Contents (read and write) |
| No **API Keys** in **More** › **Settings** | You are not a project admin | Ask a project admin to generate the key |

## Usage limit right after the first analysis

The free plan gives the testing agent 50 steps every 5 hours, counted across your projects. A dispatch is refused when fewer than 5 steps are left. An analysis explores your app and runs the tests it generates, so it can use most of that budget at once. The next dispatch then fails, for example:

```text
DISPATCH FAILED — tests were NOT started.
Reason: Usage limit reached. 47/50 steps consumed in current session. Session resets at 2026-11-09T15:00:00.000Z.
This is a dispatch/infrastructure error, not a test failure. Suggest the user try again.
```

The text is an abbreviated example; the numbers and the time are your own. Despite the last line, trying again does not help before the time in `Session resets at`.

- **Start the first analysis in Commander, not through MCP.** On the free plan, your first analysis started in Commander, for example through `https://cmd.wopee.io/signup?url=<your-app-url>`, does not count toward the limit. An analysis started with `wopee_dispatch_analysis` always counts.
- **Run one test at a time** and ask your agent not to start analyses or regenerate tests unless you ask.
- **Wait for the reset**, or upgrade in Commander.

## `localhost` URLs do not work

The testing agent runs in a browser on Wopee.io's cloud runners, not on your machine, so it cannot open `localhost`, `127.0.0.1` or an address in your private network. The analysis or the run fails to load the app.

- Use a URL the runners can reach: a staging or preview deployment.
- Set the app URL on the project in Commander. The MCP tools cannot pass a URL.
- For apps behind a VPN or a firewall, see [Enterprise connectivity](../../security/enterprise-connectivity.md).

## Still stuck?

Write to [help@wopee.io](mailto:help@wopee.io) with the exact message, your client and its version, and the `wopee-mcp` version you start.
