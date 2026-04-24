# Versa SD-WAN Multi-Tenant Airline Connectivity Lab

## Overview

This project is a hands-on Versa SD-WAN lab built in EVE-NG to simulate a managed multi-tenant SD-WAN environment for airline connectivity across multiple airports.

The lab models a scenario where several fictional airline tenants operate from different airport locations while sharing a common SD-WAN platform. Each tenant has its own connectivity requirements, internet breakout model, forwarding behavior, and security policy design.

The goal of the project was to build a realistic service-provider-style SD-WAN environment using Versa Director, Versa Controller, Versa Analytics, Versa VOS appliances, dual transport underlays, tenant segmentation, SLA-based forwarding, centralized hub services, hub redundancy, and integrated security profiles.


## Business Scenario

A regional SD-WAN hub in Brussels provides managed SD-WAN connectivity for multiple airline tenants operating across different airport locations.

The lab simulates three fictional airlines:

| Tenant | Description |
|---|---|
| Dutch Airways | Airline tenant operating from Schiphol and Frankfurt with spoke-to-hub connectivity |
| German Airways | Airline tenant operating from Schiphol and Frankfurt with spoke-to-spoke communication through the Brussels hub |
| French Airways | Airline tenant operating from Schiphol and Frankfurt with spoke-to-hub connectivity and local internet breakout |

This design demonstrates how different customers can share the same SD-WAN platform while maintaining separate connectivity models, traffic policies, and internet breakout behavior.

---

## Architecture Summary

| Area | Description |
|---|---|
| SD-WAN Platform | Versa Director, Versa Controller, and Versa Analytics |
| Regional Hub | Brussels hub site providing SD-WAN aggregation, centralized services, and centralized internet breakout |
| Hub Redundancy | Two Versa VOS edge devices deployed at the Brussels regional hub |
| Spoke Sites | Schiphol Airport and Frankfurt Airport |
| Tenants | Dutch Airways, German Airways, and French Airways |
| Multi-Tenancy | Each airline implemented as a Versa suborganization |
| Transport Underlays | MPLS and Internet |
| Forwarding Design | MPLS preferred for private/non-internet traffic, with Internet available as SLA-based failover |
| Internet Breakout | Dutch and German use centralized breakout through Brussels; French uses local DIA at each airport |
| Centralized Services | RADIUS and NTP hosted at the Brussels hub |
| Security Services | Decryption profile, antivirus profile, zone protection, and tenant policies |
| Validation | SLA violations, failover, breakout testing, centralized services, and security profile validation |

---

## Lab Topology

<img width="991" height="721" alt="topology" src="https://github.com/user-attachments/assets/0f4c7f88-2f71-40b9-94a5-937ce558ccef" />


The topology includes:

- Versa Director
- Versa Controller
- Versa Analytics
- Brussels regional hub
- Two Versa VOS edges at the Brussels hub for redundancy
- Schiphol airport spoke site
- Frankfurt airport spoke site
- MPLS underlay
- Internet underlay
- Dutch Airways tenant
- German Airways tenant
- French Airways tenant
- Centralized RADIUS and NTP services
- Tenant-specific internet breakout behavior

---

## SD-WAN Headend

The lab used the full Versa SD-WAN headend stack.

| Component | Role |
|---|---|
| Versa Director | Centralized configuration, templates, tenant management, device management, and policy management |
| Versa Controller | SD-WAN control plane and overlay control |
| Versa Analytics | Logging, monitoring, traffic visibility, and operational validation |
