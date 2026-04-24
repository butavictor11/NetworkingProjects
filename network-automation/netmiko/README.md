# Python / Netmiko Network Automation

This directory contains multiple Python automation scripts built with Netmiko.

The goal of these scripts is to automate common network engineering tasks such as inventory collection, configuration backups, and BGP configuration deployment using SSH-based automation.

---

## Scripts Overview

| Script | Purpose |
|---|---|
| `Inventory/inventory.py` | Connects to multiple devices, collects hostname, OS, software version, and uptime information, then exports the data to a CSV file |
| `ConfigBackup/config_backup.py` | Connects to multiple devices, collects the running configuration, and stores each device configuration in a separate backup file |
| `bgp_practice/bgp_practice.py` | Uses Jinja2 templates and Netmiko to configure BGP neighbor relationships and advertise networks between devices |
| `BGP/bgp_config.py` | Uses YAML variables, Jinja2 templates, and Netmiko to automate a more advanced BGP design, including route reflectors and policy-based traffic steering |

---

## Project Goals

The main goals of these scripts are to:

- Automate repetitive network operations tasks
- Collect device information in a structured format
- Generate configuration backups from multiple devices
- Use templates to create repeatable BGP configurations
- Separate device data from configuration logic using YAML variables
- Practice SSH-based automation with Netmiko

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core scripting language |
| Netmiko | SSH connectivity to network devices |
| Jinja2 | Configuration template rendering |
| YAML | Structured variables for BGP configuration |
| CSV | Inventory reporting output |
| Cisco IOS / IOSv | Network device platform used in the lab |

---

## Skills Demonstrated

| Area | Skills |
|---|---|
| Network Automation | Automating device access, command execution, and configuration deployment |
| Inventory Collection | Extracting hostname, OS, version, and uptime information |
| Configuration Backup | Saving running configurations from multiple devices |
| BGP Automation | Creating neighbors, advertising networks, configuring route reflectors |
| Traffic Engineering | Influencing BGP path selection using variable-driven policy logic |
| Templating | Using Jinja2 to generate reusable network configurations |
| Structured Data | Using YAML and CSV for input and output data |

---

## Summary

These scripts demonstrate practical Python and Netmiko automation for network operations and routing configuration tasks. They cover both operational workflows, such as inventory and backups, and configuration workflows, such as BGP neighbor creation, network advertisement, route reflector configuration, and traffic steering.
