# Ansible Network Automation Projects

This directory contains multiple Ansible network automation projects focused on configuration backup, variable-driven configuration, campus LAN deployment, and compliance auditing.

The goal of these projects was to build practical experience with Ansible playbook structure, YAML variables, Jinja2 templates, task separation, audit logic, remediation workflows, and reporting.

---

## Projects Overview

| Project | Focus | Summary |
|---|---|---|
| Project 1 | Ansible fundamentals | Introductory playbooks for backups, loopback provisioning, and device information collection |
| Project 2 | Campus LAN automation | Three-tier campus LAN configuration using separated task files, YAML variables, and Jinja2 templates |
| Project 3 | Compliance audit and remediation | Audits RADIUS, NTP, and banner configuration, applies remediation when needed, and generates reports |

---

## Project 1 - Ansible Fundamentals

This project was created to get familiar with Ansible playbook structure and basic network automation workflows.

The goal was to automate common operational tasks across multiple network devices.

### Playbooks

| Playbook | Purpose |
|---|---|
| Backup playbook | Pulls the running configuration from devices and saves timestamped backup files |
| Loopback playbook | Creates loopback interfaces on multiple devices using YAML variables |
| Version and inventory playbook | Collects software version and inventory information from network devices |

### Skills Practiced

- Creating basic Ansible playbooks
- Working with network device inventories
- Running commands on multiple devices
- Using YAML variables
- Saving command output to files
- Creating timestamped configuration backups
- Applying simple configuration changes across multiple devices

---

## Project 2 - Three-Tier Campus LAN Automation

This project focused on building a more structured Ansible workflow.

The main goal was to learn how to separate playbooks into reusable task files and use Jinja2 templates to generate a functional three-tier campus LAN design.

### What This Project Automates

| Area | Description |
|---|---|
| VLANs | Creates VLANs based on structured variables |
| SVIs | Configures switched virtual interfaces for gateway functionality |
| Access Ports | Applies access VLAN configuration to endpoint-facing ports |
| Trunk Ports | Configures trunk links between campus layers |
| Interface Descriptions | Adds consistent interface descriptions |
| Campus Design | Builds a functional three-tier campus network using templates |

### Design Approach

This project uses:

- Ansible playbooks
- Separated task files
- YAML variable files
- Jinja2 templates
- Structured campus LAN data

Instead of writing static configurations manually, the campus configuration is generated from variables and templates.

### Skills Practiced

- Separating Ansible logic into task files
- Using Jinja2 templates for network configuration generation
- Building reusable configuration workflows
- Separating data from configuration logic
- Automating a structured campus LAN design
- Creating cleaner and more scalable playbooks

---

## Project 3 - Compliance Audit and Remediation

This project focuses on using Ansible for network compliance validation.

The goal was to audit multiple devices for required RADIUS, NTP, and login banner configuration. If a device fails an audit check, Ansible applies remediation and then runs the audit again to confirm the issue was fixed.

### Audit Scope

| Configuration Area | Purpose |
|---|---|
| RADIUS | Validates centralized authentication configuration |
| NTP | Validates time synchronization configuration |
| Login Banner | Validates required device login banner configuration |

### Workflow

```text
1. Run audit against multiple devices
2. Check RADIUS, NTP, and banner configuration
3. Identify passed and failed checks
4. Apply remediation if a device fails
5. Run the audit again
6. Generate aggregate and per-device reports
