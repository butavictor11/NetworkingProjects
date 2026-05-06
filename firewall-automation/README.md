# Palo Alto Firewall Automation

This project automates common Palo Alto NGFW operations using Python and Ansible.

The goal is to demonstrate a production-style firewall automation workflow for standalone Palo Alto firewalls, including configuration backup, policy-as-code deployment, idempotent changes, and safe credential handling.

## Features

- Python-based firewall configuration backups
- Ansible-based address object deployment
- Ansible-based security policy deployment
- Ansible-based source NAT deployment
- Per-firewall policy files
- Reusable Ansible role for Palo Alto policy deployment
- Idempotent execution
- Conditional commit only when changes occur
- Git-safe credential handling using ignored credential files
- Support for targeting specific firewalls with `--limit`

## Repository Structure

```text
firewall-automation/
├── ansible/
│   ├── ansible.cfg
│   ├── group_vars/
│   │   ├── firewalls.example.yml
│   │   └── firewalls.yml              # ignored by Git
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
├── inventory/
├── python/
├── validation/
├── docs/
├── .gitignore
└── README.md

CI trigger Wed May  6 09:15:15 AM UTC 2026
CI trigger Wed May  6 09:20:11 AM UTC 2026
