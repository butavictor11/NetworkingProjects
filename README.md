# Networking Projects Portfolio

This repository documents a collection of hands-on networking, network security, SD-WAN, multicast, and automation projects built throughout my network engineering journey.

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
| Automation | Ansible, Python, Netmiko, Jinja2, YAML, configuration backups, inventory collection, templated deployments |
| Routing & Multicast | PIM Sparse Mode, Bidirectional PIM, Source-Specific Multicast |
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

## Network Automation Projects

**Project path:** `automation/`

This area contains Ansible and Python/Netmiko projects focused on automating common network engineering tasks such as configuration deployment, compliance auditing, inventory collection, configuration backups, and template-based routing configuration.

The projects are split into two main areas:

1. Ansible automation
2. Python / Netmiko automation

---

### Ansible Projects

The Ansible projects focus on building repeatable automation workflows using playbooks, separated task files, YAML variables, and Jinja2 templates.

| Project | Description |
|---|---|
| Basic Ansible Playbooks | Introductory playbooks for collecting device information, configuring loopbacks, and backing up configurations |
| Three-Tier Campus LAN Automation | Builds a functional three-tier campus design using Ansible, separated task files, YAML variables, and Jinja2 templates |
| Compliance Audit and Remediation | Audits RADIUS, NTP, and login banner configuration across multiple devices; if a device fails the audit, remediation is applied and the audit is run again |

Key Ansible work:

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

Skills demonstrated:

| Area | Skills |
|---|---|
| Ansible | Playbooks, task files, variables, inventory, command execution, configuration deployment |
| Jinja2 | Template-based campus configuration generation |
| YAML | Structured input data for repeatable automation |
| Compliance | Audit, remediation, re-check workflow |
| Reporting | Aggregate and per-device audit reports |
| Campus Design | VLANs, trunks, access ports, SVIs, three-tier campus LAN configuration |

---

### Python / Netmiko Projects

The Python and Netmiko projects focus on SSH-based network automation, data collection, configuration backup, and template-driven routing configuration.

| Script / Project | Description |
|---|---|
| `Inventory/inventory.py` | Collects hostname, operating system, software version, and uptime information from multiple devices and exports the results to a CSV file |
| `ConfigBackup/config_backup.py` | Collects running configurations from multiple devices and saves each configuration into a separate backup file |
| `bgp_practice/bgp_practice.py` | Uses Jinja2 templates and Netmiko to configure BGP neighbor relationships and advertise networks between devices |
| `BGP/bgp_config.py` | Uses YAML variables, Jinja2 templates, and Netmiko to build a more advanced BGP automation workflow, including route reflector configuration and policy-based traffic steering |

Skills demonstrated:

| Area | Skills |
|---|---|
| Python | Scripting, file handling, CSV generation, automation logic |
| Netmiko | SSH connectivity, command execution, configuration deployment |
| Jinja2 | Template-driven configuration generation |
| YAML | Structured variables for routing configuration |
| BGP Automation | Neighbor creation, network advertisement, route reflector configuration, traffic engineering |
| Operations | Inventory collection and configuration backup automation |

---

## Protocol Independent Multicast Labs

**Project path:** `routing/multicast/`

This project area focuses on multicast routing concepts and Protocol Independent Multicast behavior.

The labs implement and validate different multicast models.

### Implemented Multicast Modes

| Mode | Description |
|---|---|
| PIM Sparse Mode | RP-based multicast forwarding model |
| Bidirectional PIM | Shared-tree multicast model for many-to-many communication |
| Source-Specific Multicast | Source-aware multicast forwarding model |

### Skills Demonstrated

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
├── sd-wan/
│   └── versa-sdwan/
├── network-security/
│   └── palo-alto-enterprise-security-lab/
├── automation/
│   ├── ansible/
│   └── python/
├── routing/
│   └── multicast/
└── README.md
