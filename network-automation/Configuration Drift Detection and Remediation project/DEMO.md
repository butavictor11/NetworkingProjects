# Demo Walkthrough

This is the suggested demo flow for presenting the project on GitHub, LinkedIn, or in an interview.

## Demo Goal

Show a closed-loop network automation workflow:

```text
Detect drift -> Show diff -> Ask for approval -> Remediate -> Verify
```

## Scenario

The source of truth says `r1` Loopback0 should be:

```text
1.1.1.1/32
```

A manual change on the router changes it to:

```text
11.11.11.11/32
```

The script should detect that the router no longer matches the YAML source of truth.

## Demo Steps

1. Show the desired state in `hosts.vars/r1.yml`.
2. Manually introduce drift on the router.
3. Run the script:

```bash
python3 config_drift_remediation.py
```

4. Show DeepDiff detecting the mismatch.
5. Answer `yes` to remediate the interface section.
6. Show the script pushing `interfaces.j2` only.
7. Show post-remediation verification.

## Expected Output

```text
r1

Interfaces drift found on r1
Value of root['Loopback0']['ip'] changed from "1.1.1.1" to "11.11.11.11".

Remediate Interfaces config on r1? yes/no: yes
Pushing interfaces.j2 to r1...
Rendered XML saved to rendered/r1_interfaces.xml
Interfaces remediated on r1
```

## Presentation Talking Points

- YAML is used as the source of truth.
- NETCONF pulls actual running config from the routers.
- XML is normalized into Python dictionaries.
- DeepDiff compares desired and actual state.
- Remediation is interactive and section-based.
- The script verifies after remediation instead of assuming success.

## Strong One-Liner

This project turns a basic day-0 push script into a closed-loop configuration compliance workflow.
