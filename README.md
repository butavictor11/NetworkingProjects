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

## Palo Alto Firewall Automation Project

**Project path:** `firewall-automation/`

This project focuses on automating standalone Palo Alto NGFW operations using Python and Ansible.

The lab uses two standalone Palo Alto firewalls representing an HQ and Branch environment. The project started with a Python-based configuration backup script and was later extended into an Ansible-based policy-as-code workflow for address objects, security policies, and source NAT rules.

The goal of this project is to demonstrate a production-style firewall automation workflow where firewall policy is stored as structured YAML data and deployed consistently through a reusable Ansible role.

### Scenario

The lab simulates a small enterprise firewall environment with separate HQ and Branch Palo Alto NGFWs.

Each firewall has its own policy file, while a single reusable Ansible role handles the deployment logic. The playbook dynamically loads the correct policy file based on the inventory hostname.

Example:

| Inventory Host | Policy File |
|---|---|
| `hq` | `vars/hq_policy.yml` |
| `branch` | `vars/branch_policy.yml` |

This allows the same playbook and role to deploy firewall policy to different standalone firewalls without duplicating playbook logic.

### Key Features

- Standalone Palo Alto NGFW automation
- Python-based running configuration backup
- Ansible inventory for multiple firewalls
- Per-firewall YAML policy files
- Reusable Ansible role for policy deployment
- Address object creation
- Security policy creation
- Source NAT rule creation
- Conditional commit only when changes occur
- Idempotent Ansible execution
- Use of Ansible `--limit` to target specific firewalls
- Git-safe credential handling with ignored credential files
- Example credential file for safe repository sharing
- Basic validation tasks before deployment
- Role-based Ansible structure using separate task files

### Automation Workflow

The project follows this workflow:

```text
Backup -> Load Variables -> Validate -> Deploy Objects -> Deploy Security Rules -> Deploy NAT -> Commit if Changed
```

### Project Structure

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

### Example Capabilities

| Capability | Description |
|---|---|
| Config Backup | Python script connects to Palo Alto firewalls and saves running configuration backups |
| Address Objects | Ansible creates reusable address objects from YAML |
| Security Rules | Ansible deploys firewall security rules from per-firewall policy files |
| Source NAT | Ansible creates outbound source NAT policies for HQ and Branch |
| Conditional Commit | Firewall commit runs only if objects, rules, or NAT policies changed |
| Idempotency | Re-running the playbook does not create duplicate objects or rules |
| Targeting | `--limit hq` or `--limit branch` controls which firewall is changed |
| Credential Safety | Real credentials are ignored by Git and replaced with a safe example file |

### Skills Demonstrated

| Area | Skills |
|---|---|
| Palo Alto NGFW | Address objects, security rules, NAT, zones, commit workflow |
| Ansible | Inventory, variables, roles, tasks, tags, conditionals, idempotency |
| Python | Configuration backup automation, YAML inventory usage |
| Automation Design | Policy-as-code, reusable role structure, per-device policy files |
| Security Operations | Safe credential handling, controlled deployment, validation before change |
| Git/GitHub | `.gitignore`, example secrets file, portfolio-ready repository structure |

---

# Network Automation Projects

**Project path:** `network-automation/`

This area contains Ansible and Python/Netmiko projects focused on automating common network engineering tasks such as configuration deployment, compliance auditing, inventory collection, configuration backups, and template-based routing configuration.

The network automation projects are split into two main areas:

- Ansible automation
- Python / Netmiko automation

The Palo Alto firewall automation project is maintained separately under `firewall-automation/` because it combines firewall security operations, Python backups, and Ansible policy-as-code.

---

## Ansible Projects

The Ansible projects focus on building repeatable automation workflows using playbooks, separated task files, YAML variables, and Jinja2 templates.

| Project | Description |
|---|---|
| Basic Ansible Playbooks | Introductory playbooks for collecting device information, configuring loopbacks, and backing up configurations |
| Three-Tier Campus LAN Automation | Builds a functional three-tier campus design using Ansible, separated task files, YAML variables, and Jinja2 templates |
| Compliance Audit and Remediation | Audits RADIUS, NTP, and login banner configuration across multiple devices; if a device fails the audit, remediation is applied and the audit is run again |

### Key Ansible Work

- `version.yml` collects `show version` and `show inventory` from multiple devices.
- `loopbacks.yml` creates loopback interfaces and assigns IP addresses using variable files.
- `backup.yml` saves timestamped running configuration backups.
- Campus LAN automation uses separated task files for cleaner playbook structure.
- Jinja2 templates generate a functional three-tier campus LAN configuration.
- Campus automation includes VLANs, SVIs, trunks, access ports, interface descriptions, and variable-driven configuration.
- Compliance automation validates RADIUS, NTP, and login banner configuration across multiple devices.
- Failed audit checks trigger remediation.
- The audit is run again after remediation to confirm compliance.
- Aggregate and per-device reports are generated after every audit run.

### Skills Demonstrated

| Area | Skills |
|---|---|
| Ansible | Playbooks, task files, variables, inventory, command execution, configuration deployment |
| Jinja2 | Template-based campus configuration generation |
| YAML | Structured input data for repeatable automation |
| Compliance | Audit, remediation, re-check workflow |
| Reporting | Aggregate and per-device audit reports |
| Campus Design | VLANs, trunks, access ports, SVIs, three-tier campus LAN configuration |

---

## Python / Netmiko Projects

The Python and Netmiko projects focus on SSH-based network automation, data collection, configuration backup, and template-driven routing configuration.

| Script / Project | Description |
|---|---|
| `Inventory/inventory.py` | Collects hostname, operating system, software version, and uptime information from multiple devices and exports the results to a CSV file |
| `ConfigBackup/config_backup.py` | Collects running configurations from multiple devices and saves each configuration into a separate backup file |
| `bgp_practice/bgp_practice.py` | Uses Jinja2 templates and Netmiko to configure BGP neighbor relationships and advertise networks between devices |
| `BGP/bgp_config.py` | Uses YAML variables, Jinja2 templates, and Netmiko to build a more advanced BGP automation workflow, including route reflector configuration and policy-based traffic steering |

### Skills Demonstrated

| Area | Skills |
|---|---|
| Python | Scripting, file handling, CSV generation, automation logic |
| Netmiko | SSH connectivity, command execution, configuration deployment |
| Jinja2 | Template-driven configuration generation |
| YAML | Structured variables for routing configuration |
| BGP Automation | Neighbor creation, network advertisement, route reflector configuration, traffic engineering |
| Operations | Inventory collection and configuration backup automation |

---

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
