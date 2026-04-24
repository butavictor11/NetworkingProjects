# Zero Trust Enterprise Access Lab with Palo Alto NGFW

## Overview

This project is a hands-on enterprise security lab built with Palo Alto Networks Next-Generation Firewalls in EVE-NG.

The lab simulates a realistic enterprise environment with an HQ site, Branch connectivity, DMZ application segment, Active Directory integration, GlobalProtect remote access, NAT, IPsec VPN, User-ID, LDAP group mapping, and identity-based firewall policies.

The main goal of this project was to move beyond basic zone-based firewalling and build a more realistic access control model where users are allowed or denied based on identity, Active Directory group membership, source zone, destination zone, application requirements, and least-privilege security policies.

This lab focuses on a practical enterprise security problem:

> How do you securely provide access to internal applications for local users, branch users, internet users, and remote VPN users without giving everyone broad network access?

To solve this, the lab combines:

- Network segmentation
- Site-to-site IPsec VPN
- Remote access VPN
- Active Directory integration
- User-ID
- LDAP group mapping
- Source NAT
- Destination NAT
- DMZ publishing
- Least-privilege security policies
- Log-based validation
- Negative access testing

---

## Business and Security Problem

In many enterprise environments, users require access to different applications depending on their role, location, and authentication status.

A traditional flat network model can create unnecessary risk because users may be able to reach systems they do not need. This becomes especially important when supporting remote users, branch offices, published DMZ applications, and internal enterprise applications.

This project was designed to answer the following security questions:

- How can internal users be restricted to only the applications they need?
- How can branch users access approved HQ resources without gaining broad internal access?
- How can remote VPN users be authenticated and authorized before accessing internal applications?
- How can internet users reach a published DMZ application without exposing internal networks?
- How can Active Directory groups be used to enforce identity-aware firewall policies?
- How can firewall logs be used to prove that access is allowed or denied correctly?

---

## High-Level Topology

![Lab Topology](diagrams/topology.png)

The topology includes:

- HQ Palo Alto NGFW
- Branch connectivity
- DMZ application segment
- Internal application segments
- Windows Server Active Directory
- GlobalProtect remote user
- Simulated internet/WAN
- IPsec site-to-site VPN
- Source NAT and Destination NAT
- Identity-based firewall policies

---

## Architecture Summary

| Area | Description |
|---|---|
| HQ Security Gateway | Main Palo Alto firewall enforcing traffic between internal users, DMZ services, GlobalProtect users, Branch traffic, and external networks |
| Branch Connectivity | Branch users access approved HQ resources through the site-to-site IPsec VPN and firewall security policies |
| Remote Access | GlobalProtect provides VPN access for remote users, with access restricted by User-ID and security policies |
| Identity Source | Active Directory provides users and groups for authentication, LDAP group mapping, and identity-based policy enforcement |
| DMZ Publishing | A DMZ application is exposed through Destination NAT while remaining segmented from internal networks |
| Internet Access | Internal networks use Source NAT for outbound connectivity through the firewall |
| Access Control | Security policies enforce least-privilege access using zones, users, AD groups, destinations, and services |
| Logging and Validation | Firewall logs, User-ID mappings, VPN status, and policy hit counts are used to confirm expected behavior |

---

## Network Segmentation Design

The lab is divided into separate security zones to avoid flat network access and to enforce policy at the firewall.

| Segment | Firewall Zone | Purpose |
|---|---|---|
| HQ User Segment | HQ-USER | Represents local enterprise users at the HQ site |
| Internal Application Segment | APP | Hosts internal applications that require controlled access |
| DMZ Segment | DMZ | Hosts externally published services |
| Branch Segment | BRANCH | Represents users and systems at a remote branch location |
| GlobalProtect VPN Segment | GP-VPN | Represents remote users connected through GlobalProtect |
| Internet/WAN Segment | UNTRUST | Represents the simulated internet and external networks |
| IPsec Tunnel Segment | VPN | Represents encrypted site-to-site VPN connectivity |

The purpose of this segmentation model is to ensure that users are not trusted simply because they are connected to the network. Access is controlled through explicit firewall policies.

---

## Traffic Flow Design

The lab validates several common enterprise traffic flows.

| Traffic Flow | Description |
|---|---|
| Internal user to internal application | HQ users access approved internal applications based on AD group membership |
| Internal user to internet | Internal users access external resources through Source NAT |
| Branch user to HQ application | Branch users access approved HQ resources through an IPsec VPN |
| Remote user to internal application | GlobalProtect users access internal applications based on identity and AD group membership |
| Internet user to DMZ application | External users access a published DMZ application through Destination NAT |
| Unauthorized user to restricted application | Users without the required group membership are denied |
| Unknown user to protected resource | Unmapped or unidentified users are denied access to restricted resources |

---

## Features Implemented

| Feature | Implementation Detail | Validation |
|---|---|---|
| Palo Alto NGFW deployment | Palo Alto firewall deployed in EVE-NG as the main enterprise security gateway | Firewall interfaces, zones, routing, policies, and logs validated |
| HQ and Branch connectivity | HQ and Branch environments connected using routed firewall segments and VPN connectivity | Branch-to-HQ traffic tested through firewall logs |
| Site-to-site IPsec VPN | IPsec tunnel configured between HQ and Branch | Tunnel status and encrypted traffic flow validated |
| Source NAT | Internal outbound traffic translated through the firewall | Verified through traffic logs and internet access testing |
| Destination NAT | DMZ application published for external access | Verified with DNAT policy and inbound traffic logs |
| DMZ segmentation | Public-facing application placed in a dedicated DMZ zone | Confirmed that DMZ access is limited by security policy |
| Active Directory integration | Windows Server AD integrated with Palo Alto NGFW | LDAP connectivity and user/group visibility validated |
| LDAP group mapping | AD security groups mapped to the firewall for policy enforcement | Group membership confirmed on the firewall |
| User-ID | User-to-IP mapping used for identity-aware policies | User mappings validated in firewall logs |
| GlobalProtect VPN | Remote access VPN configured for external users | Remote user connection and policy enforcement tested |
| AD group-based policies | Security policies reference AD groups for access control | Authorized and unauthorized users tested |
| Log-based validation | Traffic logs used to confirm policy matches and allow/deny behavior | Logs confirmed correct source user, zone, policy, and action |
| Negative testing | Unauthorized access attempts tested intentionally | Deny logs confirmed enforcement of least privilege |

---

## Identity and Access Control Model

The lab follows a least-privilege access model.

Users are not trusted automatically because they are inside the network, connected through VPN, or coming from a specific segment. Access is evaluated using firewall policy logic based on:

- Source zone
- Destination zone
- Source user
- AD group membership
- Destination application or service
- NAT policy
- Security policy
- Logging result

Example access model:

| User / Source | Destination | Expected Result |
|---|---|---|
| Internal authorized user | Assigned internal application | Allowed |
| Internal unauthorized user | Restricted internal application | Denied |
| Branch user | Approved HQ resource | Allowed |
| Branch user | Non-approved internal resource | Denied |
| External internet user | Published DMZ application | Allowed through DNAT |
| External internet user | Internal application segment | Denied |
| GlobalProtect authorized user | Assigned internal application | Allowed |
| GlobalProtect unauthorized user | Restricted internal application | Denied |
| Unknown user | Restricted resources | Denied |

---

## Security Policy Design

The security policy model is based on explicit allow rules and logged deny behavior.

| Policy Purpose | Source Zone | Source Identity | Destination Zone | Destination Type | Application / Service | Action |
|---|---|---|---|---|---|---|
| Allow authorized internal users to assigned app | HQ-USER | Authorized AD group | APP | Internal application | Required application/service only | Allow |
| Deny unauthorized internal users to restricted app | HQ-USER | Any other user | APP | Restricted application | Any | Deny |
| Allow Branch users to approved HQ resource | VPN / BRANCH | Approved branch users or group | APP | Approved HQ resource | Required application/service only | Allow |
| Deny Branch users to non-approved resources | VPN / BRANCH | Any | APP / Internal | Non-approved resources | Any | Deny |
| Allow GlobalProtect users to assigned app | GP-VPN | Authorized AD group | APP | Internal application | Required application/service only | Allow |
| Deny unauthorized GlobalProtect users | GP-VPN | Any other user | APP / Internal | Restricted resources | Any | Deny |
| Allow internet users to published DMZ app | UNTRUST | Any | DMZ | Published DMZ application | Required public service only | Allow |
| Deny DMZ initiated access to internal networks | DMZ | Any | APP / HQ-USER | Internal resources | Any | Deny |
| Allow internal users outbound internet access | HQ-USER | Allowed users/groups | UNTRUST | Internet | Approved applications/services | Allow |
| Deny unknown or unapproved access | Any | Unknown or unauthorized | Protected zones | Restricted resources | Any | Deny |

The policy design avoids broad access such as:

- Any internal user to any server
- Any VPN user to internal networks
- Any Branch user to all HQ resources
- DMZ to internal access
- Unrestricted application access

---

## NAT Design

Both Source NAT and Destination NAT were implemented to simulate common enterprise firewall use cases.

### Source NAT

Source NAT is used for outbound access from internal networks toward the simulated internet.

| NAT Type | Source | Destination | Purpose |
|---|---|---|---|
| Source NAT | Internal user segments | Internet/WAN | Allows internal users to access external resources |
| Source NAT | Branch or VPN users, where required | Internet/WAN | Allows controlled outbound access through the firewall |

### Destination NAT

Destination NAT is used to publish a DMZ application to external users.

| NAT Type | Source | Destination | Purpose |
|---|---|---|---|
| Destination NAT | Internet/WAN | Published public-facing address | Translates inbound traffic to the DMZ application |

The DMZ application is published without allowing direct access to internal application or user segments.

---

## VPN Design

### Site-to-Site IPsec VPN

A site-to-site IPsec VPN was configured to connect the Branch environment to the HQ firewall.

The VPN design includes:

- IKE Gateway
- IPsec tunnel
- Tunnel interface
- Security zones
- Routing
- Security policies
- Log validation

The VPN was not treated as automatically trusted. Branch traffic still had to match explicit firewall security policies before reaching HQ resources.

### GlobalProtect Remote Access VPN

GlobalProtect was configured to provide remote access for external users.

The GlobalProtect design includes:

- GlobalProtect Portal
- GlobalProtect Gateway
- Authentication profile
- LDAP integration
- User-ID mapping
- VPN user zone
- Security policies based on AD group membership

Remote VPN users were restricted to only the internal applications they were authorized to access.

---

## Active Directory and User-ID Integration

Active Directory was integrated with the Palo Alto firewall to support identity-aware security policies.

The identity integration includes:

- LDAP Server Profile
- Authentication Profile
- Group Mapping
- User-ID
- AD security groups
- User-to-IP mapping
- Group-based security policy enforcement

This allows the firewall to make access decisions based on user identity instead of relying only on source IP addresses.

---

## Zero Trust-Inspired Concepts Demonstrated

This lab demonstrates practical Zero Trust-style access principles using Palo Alto NGFW features.

| Concept | How It Was Demonstrated |
|---|---|
| Verify explicitly | User-ID and LDAP group mapping identify users before access is allowed |
| Least privilege | Users only access applications required for their role |
| Assume breach | DMZ, Branch, Remote Access, Internal, and VPN zones are segmented |
| Identity-aware access | Firewall policies reference users and AD groups |
| Controlled remote access | GlobalProtect users are authenticated and still restricted by firewall policies |
| Explicit enforcement | Access is allowed only through specific security policies |
| Deny by default | Unauthorized and unknown users are denied access to protected resources |
| Validation through logs | Firewall logs are used to confirm allow and deny behavior |

This project is described as Zero Trust-inspired because it demonstrates several practical Zero Trust principles using Palo Alto NGFW features, including identity-aware access, segmentation, least-privilege policy enforcement, and explicit allow/deny validation.

A full production-grade Zero Trust architecture would require additional licensed capabilities and enterprise integrations, such as MFA, endpoint posture checks, continuous device compliance validation, advanced threat prevention, centralized logging/SIEM integration, and broader identity provider integration. This lab focuses on the core access-control and firewall enforcement components that can be realistically simulated in EVE-NG.

---

## Threat Model

| Risk | Control Implemented |
|---|---|
| Remote VPN user gains broad internal access | GlobalProtect users are restricted using AD groups and security policies |
| Branch compromise leads to lateral movement | Branch traffic is limited to approved HQ resources only |
| Internet exposure reaches internal networks | Destination NAT only publishes the DMZ application |
| DMZ system attempts internal access | DMZ-to-internal traffic is denied unless explicitly allowed |
| Unauthorized user accesses restricted app | AD group-based policies deny users without required membership |
| Unknown user bypasses identity policy | Unknown users are denied access to restricted resources |
| Misconfigured access policy allows too much traffic | Logs and policy hit counts are used to validate rule behavior |
| Browser/session caching causes misleading test results | Incognito/private sessions and firewall logs are used for accurate validation |

---

## Validation

The lab was validated through firewall logs, VPN status, User-ID mappings, policy hit counts, and end-user access tests.

| Test Case | Expected Result | Status |
|---|---|---|
| Branch user reaches approved HQ resource | Traffic allowed through VPN and security policy | Passed |
| Branch user attempts unapproved internal access | Traffic denied by security policy | Passed |
| External user reaches DMZ application | Destination NAT and security policy allow access | Passed |
| External user attempts internal application access | Traffic denied | Passed |
| Internal user accesses internet | Source NAT works correctly | Passed |
| GlobalProtect user connects remotely | VPN connection succeeds | Passed |
| Authorized AD group accesses assigned app | Access allowed | Passed |
| Unauthorized AD group accesses restricted app | Access denied | Passed |
| Unknown user attempts restricted access | Access denied | Passed |
| DMZ attempts internal access | Access denied unless explicitly allowed | Passed |
| Traffic logs match expected policy behavior | Correct allow/deny logs observed | Passed |
| Policy hit counts increase during testing | Correct policy match confirmed | Passed |

---

## Negative Testing

Negative testing was included to confirm that the firewall was not only allowing valid traffic, but also denying unauthorized access.

| Negative Test | Expected Result | Validation Method |
|---|---|---|
| Unauthorized internal user attempts restricted app access | Denied | Traffic log shows deny action |
| Unauthorized GlobalProtect user attempts restricted app access | Denied | Traffic log shows deny action and source user |
| Branch user attempts access to non-approved HQ resource | Denied | Security policy deny log |
| Internet user attempts access to internal application segment | Denied | No matching DNAT/security policy |
| Unknown user attempts access to protected application | Denied | User appears as unknown or unmapped in logs |
| DMZ host attempts internal access | Denied | DMZ-to-internal deny policy/log |
| User outside required AD group attempts assigned app | Denied | Group-based policy does not match |

---

## Log Analysis

Validation was performed using multiple Palo Alto log and monitoring views.

The following were checked during testing:

- Traffic logs
- System logs
- GlobalProtect logs
- User-ID mappings
- IPsec tunnel status
- NAT rule matches
- Security policy matches
- Policy hit counts
- Source zone and destination zone
- Source user
- Application identification
- Allow and deny actions

For each test, I verified:

1. The expected source zone
2. The expected destination zone
3. The correct source user or group
4. The correct application or service
5. The correct NAT rule, where applicable
6. The correct security policy match
7. The expected allow or deny action

---

## Key Palo Alto Features Used

- Security Policies
- NAT Policies
- Source NAT
- Destination NAT
- IPsec VPN
- IKE Gateway
- Tunnel Interfaces
- GlobalProtect Portal
- GlobalProtect Gateway
- LDAP Server Profile
- Authentication Profile
- Group Mapping
- User-ID
- Traffic Logs
- System Logs
- GlobalProtect Logs
- Policy Hit Counts

---

## Troubleshooting Highlights

This project included several realistic troubleshooting scenarios.

### User-ID and LDAP Group Mapping Mismatch

During testing, group-based firewall policies did not initially match as expected.

The firewall learned users in one format, while LDAP group mapping displayed users in another format. This prevented the firewall from correctly matching the user to the expected AD group.

The issue was resolved by correcting the identity and group mapping configuration so User-ID and LDAP group membership were represented consistently.

### Browser Session Causing Misleading Test Results

During application access testing, traffic appeared denied in the firewall logs while the application still appeared reachable.

Testing from a new private/incognito browser session confirmed that the firewall policy was working correctly and that the original result was caused by browser session or cache behavior.

### Palo Alto VM Resource Limitation

The IPsec tunnel initially showed stability issues in the virtual lab environment.

After increasing the Palo Alto VM memory allocation, the tunnel became stable and traffic forwarding worked as expected.

### Policy Matching Verification

Some access tests required checking policy order, source zone, destination zone, source user, application, and service fields.

This reinforced the importance of validating firewall behavior through logs instead of assuming a rule is matching correctly.

---

## Key Lessons Learned

- VPN connectivity alone does not mean users should have broad internal access.
- GlobalProtect users should still be restricted with security policies after authentication.
- User-ID and LDAP group mapping must be consistent for group-based policies to work correctly.
- Firewall logs are essential for validating both allowed and denied traffic.
- Destination NAT should publish only the required DMZ service, not expose internal networks.
- Branch connectivity should be treated as semi-trusted and restricted to approved resources.
- Browser caching and existing sessions can create misleading test results.
- Virtual firewall resource limitations can cause symptoms that look like configuration problems.
- Explicit deny rules with logging are useful for validating least-privilege access models.
- A realistic firewall lab should include both positive and negative testing.

---

## Evidence

Screenshots and supporting outputs should be stored using the following structure:

```text
screenshots/
├── security-policies/
├── nat/
├── ipsec/
├── user-id/
├── globalprotect/
├── logs/
├── traffic-tests/
└── troubleshooting/