# Networking Projects Portfolio

This repository documents a collection of hands-on networking, network security, SD-WAN, multicast, firewall automation, and network automation projects built throughout my network engineering journey.

The goal of this repository is to show practical engineering ability through realistic lab scenarios, clear documentation, diagrams, screenshots, validation outputs, and configuration examples where available.

The projects are organized by technology area and focus on both implementation and verification.

---

## About This Repository

This repository is built around practical network engineering projects, not theory-only notes.

Each project is intended to show:

- The problem or scenario being simulated
- The topology and design choices
- The technologies configured
- The validation method used to prove the lab works
- Screenshots, command outputs, diagrams, or documentation where available

Some older projects may have fewer screenshots or configuration exports than newer projects. Newer projects are documented more thoroughly with diagrams, matrices, traffic validation, and evidence-based README files.

---

## Project Areas

| Area | Focus |
|---|---|
| SD-WAN | Versa SD-WAN, hub-and-spoke design, multi-tenancy, SLA-based forwarding, internet breakout, centralized services |
| Network Security | Palo Alto NGFW, User-ID, GlobalProtect, IPsec VPN, NAT, DMZ publishing, identity-based access control |
| Firewall Automation | Palo Alto policy-as-code, Ansible roles, Python backups, address objects, security rules, NAT, conditional commits |
| Automation | Ansible, Python, Netmiko, Jinja2, YAML, configuration backups, inventory collection, templated deployments |
| Multicast | PIM Sparse Mode, Bidirectional PIM, Source-Specific Multicast |
| Campus Networking | VLANs, SVIs, trunking, routed access, campus LAN automation |

---

# Featured Projects

## Versa SD-WAN Multi-Tenant Airline Connectivity Lab

**Project path:** `sd-wan/versa-sdwan/`

This project simulates a managed multi-tenant SD-WAN environment for airline connectivity across multiple airport locations.

The lab is built around a regional hub in Brussels that provides SD-WAN connectivity and centralized services to three fictional airline tenants operating from Schiphol and Frankfurt airport sites.

### Scenario

Three airline tenants share the same Versa SD-WAN platform but have different connectivity and internet breakout requirements.

| Tenant | Connectivity Model | Internet Breakout |
|---|---|---|
| Dutch Airways | Spoke-to-hub only | Centralized through Brussels hub |
| German Airways | Spoke-to-spoke via Brussels hub | Centralized through Brussels hub |
| French Airways | Spoke-to-hub only | Local DIA at each airport |

### Key Features

- Versa Director, Controller, and Analytics
- Versa VOS appliances
- Brussels regional hub
- Two VOS edge devices at the hub for redundancy
- Schiphol and Frankfurt airport spoke sites
- Airline tenants implemented as Versa suborganizations
- MPLS and Internet transport underlays
- SLA-based forwarding and failover
- MPLS preferred for private traffic
- Internet transport used when SLA conditions are breached
- Centralized internet breakout for Dutch Airways and German Airways
- Local DIA breakout for French Airways
- Centralized RADIUS and NTP services at the hub
- Security features including decryption profile, antivirus profile, and zone protection
- Validation evidence for breakout behavior, failover, SLA violations, and centralized services

### Skills Demonstrated

| Area | Skills |
|---|---|
| SD-WAN Design | Hub-and-spoke architecture, dual transports, SLA-based forwarding |
| Versa SD-WAN | Director, Controller, Analytics, VOS edges, forwarding profiles, policies |
| Multi-Tenancy | Tenant separation using Versa suborganizations |
| Resiliency | Redundant VOS edge design at the regional hub |
| Internet Breakout | Centralized breakout and local DIA models |
| Security | Decryption, antivirus, zone protection, security policies |
| Operations | RADIUS, NTP, monitoring, validation, troubleshooting |

---

## Palo Alto Zero Trust Enterprise Access Lab

**Project path:** `network-security/palo-alto-enterprise-security-lab/`

This project is a Palo Alto Networks NGFW lab focused on enterprise access control, remote access, NAT, VPN connectivity, and identity-based security policy enforcement.

The lab simulates an enterprise environment with an HQ site, branch connectivity, DMZ application publishing, Active Directory integration, User-ID, LDAP group mapping, GlobalProtect, and IPsec VPN.

### Scenario

The project focuses on building a more realistic enterprise security design where users are not allowed access only because they are in the correct subnet or zone. Instead, access is controlled using identity, group membership, source zone, destination zone, and required service.

### Key Features

- Palo Alto NGFW in EVE-NG
- HQ and branch firewall design
- Site-to-site IPsec VPN
- GlobalProtect remote access VPN
- Active Directory / LDAP integration
- User-ID mapping
- LDAP group mapping
- Identity-based firewall policies
- Source NAT for outbound internet access
- Destination NAT for DMZ application publishing
- DMZ application access validation
- Security policy allow/deny testing
- Traffic logs proving user-based policy enforcement

### Skills Demonstrated

| Area | Skills |
|---|---|
| Firewall Design | Zones, interfaces, policies, routing, NAT |
| Identity Security | User-ID, LDAP group mapping, identity-based access control |
| Remote Access | GlobalProtect VPN |
| VPN | Site-to-site IPsec between HQ and branch |
| NAT | Source NAT and Destination NAT |
| DMZ Design | Published application behind firewall |
| Validation | Traffic logs, policy match testing, allowed/denied access verification |

---

## Configuration Drift Detection and Remediation Project

**Project path:** `network-automation/Configuration Drift Detection and Remediation project/`

This project is a Python-based network automation workflow focused on configuration drift detection, controlled remediation, and post-change verification using NETCONF/YANG.

The project uses YAML files as the source of truth, pulls live running configuration from Cisco IOS XE routers with NETCONF, normalizes both desired and actual state into Python dictionaries, compares them with DeepDiff, and optionally remediates only the configuration section where drift is detected.

### Scenario

The lab simulates a network operations workflow where router configuration is expected to match a documented source of truth. If a device is manually changed outside the intended state, the script detects the mismatch and gives the operator the option to remediate the drift.

The workflow covers three configuration domains:

| Configuration Area | Purpose |
|---|---|
| Interfaces | Validates interface IP addressing against YAML intent |
| Static Routing | Validates static route prefixes and next-hop values |
| BGP | Validates ASN, router ID, neighbors, update source, multihop, and advertised networks |

### Key Features

- YAML-based source of truth
- NETCONF/YANG live configuration collection
- Cisco IOS XE native YANG model usage
- Jinja2-rendered NETCONF XML templates
- XML parsing with `lxml`
- Desired-state and actual-state normalization into Python dictionaries
- DeepDiff comparison for drift detection
- Section-based drift checks for interfaces, static routes, and BGP
- Operator confirmation before remediation
- Targeted remediation using only the drifted configuration template
- Post-remediation verification by pulling live config again
- Rendered XML examples saved for review and troubleshooting
- Local inventory file excluded from GitHub with a sanitized example inventory included

### Automation Workflow

```text
Load YAML Source of Truth
  -> Pull Running Config with NETCONF
  -> Parse YANG XML
  -> Normalize Desired and Actual State
  -> Compare with DeepDiff
  -> Prompt for Remediation
  -> Push Drifted Section Only
  -> Pull Running Config Again
  -> Verify Compliance
```

### Example Drift

A common test case is changing `Loopback0` on a router so that the live device no longer matches the YAML source of truth.

| Source | Loopback0 IP |
|---|---|
| YAML desired state | `1.1.1.1/32` |
| Router actual state | `11.11.11.11/32` |

The script detects the mismatch, shows the exact DeepDiff output, asks whether to remediate the interface configuration, pushes the interface template, and verifies the router again.

### Skills Demonstrated

| Area | Skills |
|---|---|
| Python | Scripting, functions, dictionaries, control flow, data normalization |
| NETCONF/YANG | Running config collection, subtree filters, Cisco IOS XE native model usage |
| XML Parsing | `lxml`, namespaces, extracting structured configuration data |
| Jinja2 | NETCONF XML template rendering for targeted configuration pushes |
| YAML | Source-of-truth data modeling for router intent |
| Drift Detection | DeepDiff comparison of desired state vs actual running state |
| Remediation | Section-based correction, operator approval, post-check verification |
| Network Automation Design | Closed-loop workflow, safe inventory handling, reusable remediation function |

---

# Palo Alto Firewall Automation Project

**Project path:** `firewall-automation/`

This project focuses on automating standalone Palo Alto NGFW operations using **Python** and **Ansible**.

The lab uses two standalone Palo Alto firewalls representing an **HQ and Branch** environment. The project started with a Python-based configuration backup script and was later extended into an Ansible-based **policy-as-code** workflow for address objects, security policies, source NAT rules, and site-to-site IPsec VPN automation.

The goal of this project is to demonstrate a production-style firewall automation workflow where firewall configuration intent is stored as structured YAML data and deployed consistently through a reusable Ansible role.

---

## Scenario

The lab simulates a small enterprise firewall environment with separate HQ and Branch Palo Alto NGFWs.

Each firewall has its own policy file, while a single reusable Ansible role handles the deployment logic. The playbook dynamically loads the correct policy file based on the inventory hostname.

| Inventory Host | Policy File |
|---|---|
| `hq` | `vars/hq_policy.yml` |
| `branch` | `vars/branch_policy.yml` |

This allows the same playbook and role to deploy firewall configuration to different standalone firewalls without duplicating playbook logic.

Current lab design:

```text
HQ users:         10.10.10.0/24
Branch users:     10.20.20.0/24
HQ untrust IP:    57.57.57.57
Branch untrust:   58.58.58.58
VPN tunnel:       tunnel.1
Tunnel subnet:    172.16.1.0/30
HQ tunnel IP:     172.16.1.1/30
Branch tunnel IP: 172.16.1.2/30
```

---

## Key Features

- Standalone Palo Alto NGFW automation
- Python-based running configuration backup
- Ansible inventory for multiple firewalls
- Per-firewall YAML policy files
- Reusable Ansible role for policy deployment
- Dynamic variable loading based on inventory hostname
- Address object creation
- Security policy creation
- Source NAT rule creation
- Tunnel interface creation
- VPN zone assignment
- IKE crypto profile creation
- IPsec crypto profile creation
- IKE gateway creation
- IPsec tunnel creation
- Static routes over the VPN tunnel
- User-to-user VPN security policies
- Conditional commit only when changes occur
- Optional forced commit using an extra variable
- Idempotent Ansible execution
- Use of `--limit` to target specific firewalls
- Git-safe credential handling with ignored credential files
- Example credential file for safe repository sharing
- Basic validation tasks before deployment
- Role-based Ansible structure using separate task files
- Palo Alto CLI troubleshooting workflow for IKE/IPsec

---

## Automation Workflow

The project follows this workflow:

```text
Backup
  -> Load Variables
  -> Validate YAML Policy Data
  -> Deploy Address Objects
  -> Deploy Tunnel Interface
  -> Deploy IKE Crypto Profile
  -> Deploy IPsec Crypto Profile
  -> Deploy IKE Gateway
  -> Deploy IPsec Tunnel
  -> Deploy Static Routes
  -> Deploy Security Rules
  -> Deploy NAT Rules
  -> Commit if Changed
```

---

## Project Structure

```text
firewall-automation/
├── ansible/
│   ├── ansible.cfg
│   ├── group_vars/
│   │   ├── firewalls.example.yml
│   │   └── firewalls.yml
│   ├── inventory.yml
│   ├── playbooks/
│   │   └── deploy_policy.yml
│   ├── requirements.yml
│   ├── roles/
│   │   └── panos_policy/
│   │       ├── defaults/
│   │       │   └── main.yml
│   │       └── tasks/
│   │           ├── main.yml
│   │           ├── load_vars.yml
│   │           ├── validate.yml
│   │           ├── objects.yml
│   │           ├── create_tunnel_interface.yml
│   │           ├── ike_profile.yml
│   │           ├── ipsec_profile.yml
│   │           ├── ike_gateway.yml
│   │           ├── ipsec_to_ike.yml
│   │           ├── static_routes.yml
│   │           ├── security.yml
│   │           ├── nat.yml
│   │           └── commit.yml
│   └── vars/
│       ├── hq_policy.yml
│       └── branch_policy.yml
├── docs/
├── inventory/
├── python/
├── validation/
└── README.md
```

---

## Example Capabilities

| Capability | Description |
|---|---|
| Config Backup | Python script connects to Palo Alto firewalls and saves running configuration backups |
| Address Objects | Ansible creates reusable address objects from YAML |
| Security Rules | Ansible deploys firewall security rules from per-firewall policy files |
| Source NAT | Ansible creates outbound source NAT policies for HQ and Branch |
| Tunnel Interface | Ansible creates `tunnel.1` and assigns it to the virtual router and VPN zone |
| IKE Crypto Profile | Ansible deploys IKE crypto settings such as DH group, authentication, encryption, and lifetime |
| IPsec Crypto Profile | Ansible deploys ESP authentication, encryption, PFS group, and lifetime settings |
| IKE Gateway | Ansible creates the IKE gateway between HQ and Branch public IPs |
| IPsec Tunnel | Ansible binds the IPsec tunnel to the tunnel interface, IKE gateway, and IPsec crypto profile |
| Static Routes | Ansible installs routes to remote user subnets through `tunnel.1` |
| VPN Policies | Ansible creates User-to-VPN and VPN-to-User rules for inter-site user traffic |
| Conditional Commit | Firewall commit runs only if registered tasks report changes |
| Force Commit | Optional `force_commit=true` allows manual commit when needed |
| Idempotency | Re-running the playbook does not create duplicate objects, policies, or VPN components |
| Targeting | `--limit hq` or `--limit branch` controls which firewall is changed |
| Credential Safety | Real credentials are ignored by Git and replaced with a safe example file |

---

## IPsec VPN Automation

The project includes automation for a route-based site-to-site IPsec VPN between HQ and Branch.

The VPN deployment includes:

```text
Tunnel interface creation
VPN zone attachment
IKE crypto profile
IPsec crypto profile
IKE gateway
IPsec tunnel object
Static routes over tunnel.1
Security policies for user-to-user VPN traffic
```

Logical VPN design:

```text
HQ firewall:
  Untrust IP: 57.57.57.57
  User subnet: 10.10.10.0/24
  Tunnel IP: 172.16.1.1/30
  Route to Branch users: 10.20.20.0/24 via tunnel.1

Branch firewall:
  Untrust IP: 58.58.58.58
  User subnet: 10.20.20.0/24
  Tunnel IP: 172.16.1.2/30
  Route to HQ users: 10.10.10.0/24 via tunnel.1
```

VPN verification was performed using Palo Alto CLI commands:

```bash
show vpn ike-sa
show vpn ipsec-sa
test vpn ike-sa gateway Ike_gateway
test routing fib-lookup virtual-router default ip 10.20.20.1
test routing fib-lookup virtual-router default ip 10.10.10.1
test security-policy-match source 10.10.10.1 destination 10.20.20.1 protocol 1 from User to VPN
tail follow yes mp-log ikemgr.log
```

The VPN was successfully brought up, with logs confirming:

```text
IKEv2 IKE SA NEGOTIATION SUCCEEDED
IKEv2 CHILD SA NEGOTIATION SUCCEEDED
IPSEC KEY INSTALLATION SUCCEEDED
```

---

## Example Ansible Usage

Run the playbook against all firewalls:

```bash
ansible-playbook -i inventory.yml playbooks/deploy_policy.yml
```

Run only against HQ:

```bash
ansible-playbook -i inventory.yml playbooks/deploy_policy.yml --limit hq
```

Run only against Branch:

```bash
ansible-playbook -i inventory.yml playbooks/deploy_policy.yml --limit branch
```

Force a commit when required:

```bash
ansible-playbook -i inventory.yml playbooks/deploy_policy.yml -e force_commit=true
```

Syntax check:

```bash
ansible-playbook -i inventory.yml playbooks/deploy_policy.yml --syntax-check
```

---

## Skills Demonstrated

| Area | Skills |
|---|---|
| Palo Alto NGFW | Address objects, zones, security rules, NAT, tunnel interfaces, IKE gateways, IPsec tunnels, static routes, commit workflow |
| VPN | Route-based IPsec VPN, IKE crypto, IPsec crypto, tunnel interfaces, VPN routing, IKE/IPsec troubleshooting |
| Ansible | Inventory, variables, roles, tasks, loops, registers, conditionals, tags, idempotency, `--limit`, forced commits |
| Python | Configuration backup automation and YAML inventory usage |
| Automation Design | Policy-as-code, reusable role structure, per-device policy files, structured configuration intent |
| Security Operations | Safe credential handling, controlled deployment, validation before change, firewall troubleshooting |
| Git/GitHub | `.gitignore`, example secrets file, repository structure, portfolio-ready documentation |

---

## Notes

This project is designed as a hands-on lab and portfolio project for learning firewall automation. The same role structure can be extended further to include:

- NAT exemption for VPN traffic
- Dynamic address groups
- Security profile groups
- Decryption policies
- Panorama support
- Post-deployment validation scripts
- CI/CD pipeline integration
- Automated firewall compliance checks

# Protocol Independent Multicast Labs

**Project path:** `multicast/`

This project area focuses on multicast routing concepts and Protocol Independent Multicast behavior.

The labs implement and validate different multicast models.

## Implemented Multicast Modes

| Mode | Description |
|---|---|
| PIM Sparse Mode | RP-based multicast forwarding model |
| Bidirectional PIM | Shared-tree multicast model for many-to-many communication |
| Source-Specific Multicast | Source-aware multicast forwarding model |

## Skills Demonstrated

| Area | Skills |
|---|---|
| Multicast Routing | PIM behavior, multicast forwarding, receiver/source validation |
| PIM Sparse Mode | RP-based shared tree operation |
| Bidirectional PIM | Many-to-many multicast communication model |
| SSM | Source-specific multicast behavior |
| Troubleshooting | PIM neighbors, multicast routing table, traffic validation |

---

# Repository Structure

```text
NetworkingProjects/
├── firewall-automation/
│   ├── ansible/
│   ├── docs/
│   ├── inventory/
│   ├── python/
│   ├── validation/
│   └── README.md
├── sd-wan/
│   └── versa-sdwan/
├── network-security/
│   └── palo-alto-enterprise-security-lab/
├── network-automation/
├── multicast/
└── README.md
```

Folder names may evolve as projects are improved and reorganized.

---

# Skills Demonstrated Across This Repository

| Category | Technologies / Concepts |
|---|---|
| SD-WAN | Versa SD-WAN, Director, Controller, Analytics, VOS, SLA-based forwarding, internet breakout |
| Network Security | Palo Alto NGFW, User-ID, GlobalProtect, IPsec VPN, NAT, DMZ, identity-based policy |
| Firewall Automation | Palo Alto NGFW, Ansible roles, policy-as-code, source NAT, conditional commits, idempotent deployment |
| Automation | Ansible, Python, Netmiko, Jinja2, YAML, CSV |
| Multicast | PIM Sparse Mode, Bidirectional PIM, Source-Specific Multicast |
| Switching | VLANs, trunks, SVIs, campus LAN design |
| VPN | Site-to-site IPsec, remote access VPN |
| Services | RADIUS, NTP, centralized services |
| Validation | Traffic logs, traceroute, ping, policy testing, SLA failover testing |
| Lab Platforms | EVE-NG, virtual routers, virtual firewalls, virtual SD-WAN appliances |

---

# Why This Repository Matters

This repository is meant to show how I approach network engineering projects from design to validation.

My general workflow is:

1. Define a realistic scenario.
2. Build the lab topology.
3. Configure the required network/security/automation components.
4. Validate the expected behavior.
5. Document the design, results, and lessons learned.

The focus is not only on configuration, but also on proving that the configuration works.

Examples include:

- Showing traffic path behavior with traceroute
- Validating SD-WAN transport failover after SLA violations
- Proving internet breakout behavior per tenant
- Confirming User-ID based access control with firewall logs
- Using automation to generate backups, inventory reports, and configuration snippets
- Deploying Palo Alto firewall policy through reusable Ansible roles
- Using idempotent automation to avoid duplicate firewall objects and rules

---

# Notes

Some projects are more mature than others.

Newer projects include better documentation, diagrams, screenshots, validation matrices, and evidence folders. Older projects may be improved over time as I rebuild or expand them.

Where full configuration exports are not available, the documentation focuses on architecture, implementation approach, and available validation evidence.

---

# Current Focus

My current focus areas are:

- Network security engineering
- Palo Alto NGFW design and operations
- SD-WAN architecture
- Network automation
- Realistic lab documentation for portfolio projects
