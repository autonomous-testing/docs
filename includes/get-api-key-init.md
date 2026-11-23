Run this from the repository root (Node.js 20.18.1 or newer):

```shell
npx -y @wopee-io/init@latest
```

It prints a link and three pairing words. Open the link, check that Commander shows the same words, pick the project and click **Approve**. The command then writes `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` to a git-ignored `.env` (or `.env.local` when the repository has one) and adds a key-free `wopee` MCP server entry for your coding agents. Running it again keeps a key that already works.

**With a coding agent:** the agent runs this command itself, shows you the link and the three words, and waits. Approving in Commander is your only step: the agent never hands the command to you, and the API key never passes through the chat. See [Set up Wopee.io with your coding agent](/agent-setup/).

**Manual fallback:** run `npx -y @wopee-io/init@latest --manual` in your own terminal. It asks for the project UUID and a key from the **API Keys** page in a hidden prompt and writes the same files. In CI the command never pairs: set `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` as CI secrets. To copy the values yourself:
