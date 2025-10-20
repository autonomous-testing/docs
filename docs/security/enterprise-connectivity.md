# Enterprise Connectivity

Connect Wopee.io to applications behind VPN, firewalls, or in secure enterprise environments.

## Connectivity Options

### Option 1: IP Allowlisting (Recommended)

Allow Wopee.io cloud IPs to access your internal systems.

#### Wopee.io IP Ranges

**Production IPs** (to be provided by Wopee.io):

```
# Primary Wopee.io Cloud IPs
203.0.113.0/24    # Wopee.io Cloud - Primary
198.51.100.0/24   # Wopee.io Cloud - Secondary
192.0.2.0/24      # Wopee.io Cloud - Backup

# Regional IPs (if applicable)
# North America: 203.0.113.0/24
# Europe: 198.51.100.0/24
# Asia Pacific: 192.0.2.0/24
```

!!! caution "IP Addresses"

    The IP ranges above are placeholders. Contact Wopee.io support for actual IP addresses for your region.

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
