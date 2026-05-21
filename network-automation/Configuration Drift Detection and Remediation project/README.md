# Configuration Drift Detection and Remediation

A Python network automation project that detects configuration drift on Cisco IOS XE routers using NETCONF/YANG, compares live router state against a YAML source of truth, and optionally remediates only the section that drifted.

This project started as a basic day-0 configuration push script and evolved into a closed-loop compliance workflow:

```text
Source of Truth -> Pull Actual State -> Detect Drift -> Remediate -> Verify
```

## What This Project Does

The script audits three configuration domains:

- Interfaces
- Static routes
- BGP

For each router, it:

1. Loads intended configuration from YAML host variable files.
2. Pulls live running configuration from the router using NETCONF.
3. Parses YANG XML into normalized Python dictionaries.
4. Compares desired state vs actual state with DeepDiff.
5. Shows the exact drift found.
6. Prompts before making changes.
7. Pushes only the drifted configuration section.
8. Pulls live config again and verifies whether the drift was fixed.

## Why It Matters

A lot of automation demos stop at "push config to device." This project goes further by validating intent before and after changes.

That makes the workflow closer to real operations:

- Detect configuration drift
- Avoid blind full-config pushes
- Remediate only affected sections
- Verify after remediation
- Keep YAML as the source of truth

## Architecture

```text
+--------------------------+
| YAML Source of Truth     |
| hosts.vars/*.yml         |
+------------+-------------+
             |
             v
+--------------------------+
| Python Automation        |
| config_drift_remediation |
+------------+-------------+
             |
             v
+--------------------------+
| NETCONF/YANG Pull        |
| running config sections  |
+------------+-------------+
             |
             v
+--------------------------+
| Normalize Data           |
| XML -> Python dicts      |
+------------+-------------+
             |
             v
+--------------------------+
| Drift Detection          |
| DeepDiff                 |
+------------+-------------+
             |
             v
+--------------------------+
| Optional Remediation     |
| Jinja2 NETCONF XML       |
+------------+-------------+
             |
             v
+--------------------------+
| Verification             |
| Pull and compare again   |
+--------------------------+
```

## Repository Layout

```text
.
├── config_drift_remediation.py   # Main drift detection/remediation script
├── hosts.vars/                   # Desired state per router
├── templates/                    # Jinja2 NETCONF XML templates
├── rendered/                     # Rendered XML examples
├── inventory.example.yml         # Sanitized inventory example
└── requirements.txt              # Python dependencies
```

`inventory.yml` is intentionally ignored because it contains local lab endpoints and credentials.

## Technologies Used

- Python
- NETCONF
- YANG
- Cisco IOS XE native models
- Jinja2
- YAML
- lxml
- ncclient
- DeepDiff

## Example Drift

If YAML says Loopback0 should be:

```text
1.1.1.1/32
```

but the router has:

```text
11.11.11.11/32
```

DeepDiff reports the mismatch, the script asks whether to remediate, pushes only `interfaces.j2`, then verifies the router again.

Example output:

```text
Interfaces drift found on r1
Value of root['Loopback0']['ip'] changed from "1.1.1.1" to "11.11.11.11".

Remediate Interfaces config on r1? yes/no: yes
Pushing interfaces.j2 to r1...
Interfaces remediated on r1
```

## Design Notes

The script intentionally normalizes both desired and actual state into Python dictionaries before comparing them. This keeps drift detection independent from XML formatting and focuses on actual configuration intent.

The remediation logic is section-based. If only BGP drifts, only the BGP template is pushed. If only interfaces drift, only the interface template is pushed.

## Future Improvements

- Replace YAML with NetBox as the source of truth
- Add an audit-only CLI flag
- Add a non-interactive remediation mode
- Save drift reports to timestamped files
- Add structured JSON output
- Add unit tests for parser functions
- Add CI linting for templates and Python syntax
