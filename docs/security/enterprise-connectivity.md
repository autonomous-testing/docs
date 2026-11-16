---
description: Connect Wopee.io to apps behind VPN or firewalls. Options include IP allowlisting, VPN tunnels, and on-premise agent deployment.
---

# Enterprise Connectivity

Connect Wopee.io to applications behind VPN, firewalls, or in secure enterprise environments.

!!! tip "For a quick test"

    To test an app on your machine or in your network once, expose it for the time of the test with a tunnel, or use a deployed staging or preview URL. See [Test an app that runs on localhost](../guides/test-localhost.md). The options below are for permanent access.

## Connectivity Options

### Option 1: IP Allowlisting (Recommended)

Allow Wopee.io cloud IPs to access your internal systems.

#### Wopee.io IP Addresses

[Contact us](mailto:help@wopee.io) for the current egress IP addresses to allowlist.

### Option 2: Secure Tunnel (Enterprise Plan)

Establish a secure tunnel between Wopee.io and your internal network.

#### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Wopee.io      │    │   Secure        │    │   Your Internal │
│   Cloud         │◄──►│   Tunnel        │◄──►│   Network       │
│                 │    │   (VPN/SSH)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Option 3: Self-Hosted Runner

Run Wopee.io agents within your internal network.

#### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Wopee.io      │    │   Your Internal │    │   Your Internal │
│   Cloud         │◄──►│   Runner        │◄──►│   Applications  │
│   (Control)     │    │   (Agent)       │    │   (SUT)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Choose Connectivity Method

| Factor               | IP Allowlisting | Secure Tunnel | Self-Hosted Runner |
| -------------------- | --------------- | ------------- | ------------------ |
| **Setup Complexity** | Low             | Medium        | High               |
| **Security**         | Medium          | High          | Highest            |
| **Maintenance**      | Low             | Medium        | High               |
| **Cost**             | Free            | Enterprise    | Enterprise         |
| **Control**          | Low             | Medium        | High               |

## Related Pages

- [Getting Started Guide](../ai-agent.md) - Initial setup
- [Pilot Projects](../pilot-projects.md) - More about pilot projects
- [Start now!](https://wopee.io/book-demo) - Get started with your pilot project
