# Network Design Labs — SD-WAN and Security

Two network designs built end to end in EVE-NG, each driven by a realistic scenario rather than a feature checklist: a multi-tenant SD-WAN fabric for an airline customer, and a zero-trust enterprise access design built around identity rather than IP addresses.

Both were built to work through the hard parts — tenant separation, failover behaviour, identity-based policy — rather than to produce a screenshot of a working tunnel.

> Looking for my network automation work? It lives in its own repositories — see [Elsewhere](#elsewhere) at the bottom.

---

## Multi-Tenant Versa SD-WAN — Airline Hub and Branch

`sd-wan/versa-sdwan/`

**Scenario.** A Brussels hub with two VOS edges serves three airline tenants across branch sites at Schiphol and Frankfurt. Each tenant needs its own routing, its own policy and its own internet path, over shared physical infrastructure.

**What it covers**

- Multi-tenant separation across a shared hub — three tenants, one fabric
- Dual underlay: MPLS and public internet, with SLA-based failover between them
- Centralized breakout for tenants whose traffic must egress through the hub, and local breakout for tenants where it shouldn't
- Shared services — RADIUS and NTP — reachable per tenant
- Per-tenant security profiles

**The interesting part.** Breakout policy is where multi-tenancy stops being a configuration exercise. One tenant's security posture requires internet traffic to leave through the hub where it can be inspected; another needs local breakout at the branch for latency. Both tenants ride the same edges.

---

## Zero-Trust Enterprise Access — Palo Alto NGFW

`network-security/zero-trust-enterprise-access-palo-alto/`

**Scenario.** HQ and branch firewalls connected over site-to-site IPsec, with remote users terminating on GlobalProtect, and an application published in a DMZ. Access is decided by who the user is, not where their packet came from.

**What it covers**

- Site-to-site IPsec between HQ and branch
- GlobalProtect remote access for roaming users
- AD/LDAP integration with User-ID, so policy is written against users and groups rather than source addresses
- Source and destination NAT
- A DMZ-hosted application reachable from both the branch and remote users, under the same identity-based policy

**The interesting part.** Writing the whole policy set without a source-IP rule. Once identity drives the decision, a user gets the same access from the branch, from home, or from a hotel — and revoking a group membership revokes it everywhere at once.

---

## What's in each folder

Topology diagrams, configuration exports, and validation output captured while building — the state before and after each piece of configuration, so the behaviour is demonstrated rather than asserted.

These are lab builds on virtualised appliances, not production deployments. Scale is small by design: the point is the design decisions, not the device count.

---

## Elsewhere

My network automation work lives in its own repositories:

- **netbox-intent-pipeline** — a GitLab CI/CD pipeline that treats NetBox as the source of truth: renders device configuration, validates it offline, builds an ephemeral Cisco CML lab with Terraform, deploys with Ansible, and verifies with pyATS that the live network matches declared intent — rolling back automatically when it doesn't. → LINK_HERE
- **CDP-driven interface description automation** — discovers topology over CDP and writes interface descriptions from what it finds, with pre/post snapshot-diff gating and an idempotency check. → LINK_HERE

---

**Victor-Codrin Buta** — network engineer working on airport networks across 20+ international sites. Amsterdam.
[LinkedIn](https://www.linkedin.com/in/victor-codrin-buta-97aa25208/)
- Palo Alto NGFW design and operations
- SD-WAN architecture
- Network automation
- Realistic lab documentation for portfolio projects
