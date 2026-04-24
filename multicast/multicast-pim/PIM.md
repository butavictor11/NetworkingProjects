# Multicast Application Design and Validation

This lab demonstrates three multicast models used for different application requirements:

Topology:
<img width="791" height="344" alt="image" src="https://github.com/user-attachments/assets/e6dd8f45-c356-4fd5-a34f-efc3cf669808" />


1. **PIM Sparse Mode** for one-to-many application traffic
2. **Bidirectional PIM** for many-to-many / conferencing-style multicast traffic
3. **Source-Specific Multicast** for source-restricted multicast traffic

The lab uses BSR to advertise RP information for the ASM multicast groups.

---

## Application Requirements

| Application | Multicast Group | Requirement | Multicast Model |
|---|---:|---|---|
| One-to-many application | `239.1.1.1` | Traffic is sent from a source to multiple receivers | PIM Sparse Mode |
| Video conferencing application | `239.2.2.2` | Hosts may send and receive multicast traffic in a conferencing-style model | Bidirectional PIM |
| Secure source-specific application | `232.1.1.1` | Receivers should only accept traffic from source `10.0.0.10` | Source-Specific Multicast |

---

## RP Design

BSR is used to advertise RP information for the ASM groups.

### RP Assignment

| Router | Interface | RP Role | Group | Priority |
|---|---|---|---:|---:|
| R3 | Loopback0 | Main RP | `239.1.1.1` | `130` |
| R2 | Loopback0 | Redundant RP | `239.1.1.1` | `100` |
| R2 | Loopback1 | Main RP | `239.2.2.2` | `130` |
| R3 | Loopback1 | Redundant RP | `239.2.2.2` | `100` |

### Design Summary

- `239.1.1.1` uses **PIM Sparse Mode**.
- `239.2.2.2` uses **Bidirectional PIM**.
- `232.1.1.1` uses **SSM**, so it does not require an RP.
- BSR advertises RP candidates for the ASM groups.
- RP priority is used to prefer the main RP and keep a redundant RP available.

---

# Validation Output

## Bidirectional PIM Validation

**Application:** Video conferencing  
**Multicast group:** `239.2.2.2`  
**Expected behavior:** Bidirectional PIM tree is built toward the RP.

```text
(*,239.2.2.2), 00:48:07/-, RP 33.33.33.33, flags: BC
  Bidir-Upstream: GigabitEthernet0/2, RPF nbr: 10.0.4.2

Incoming interface:
  GigabitEthernet0/1, Accepting/Sparse
  GigabitEthernet0/0, Accepting/Sparse
  Loopback0, Accepting/Sparse
  GigabitEthernet0/2, Accepting/Sparse

Outgoing interface list:
  GigabitEthernet0/1, Forward/Sparse, 00:45:21/00:03:25, p
  GigabitEthernet0/0, Forward/Sparse, 00:45:43/00:02:31
  GigabitEthernet0/2, Bidir-Upstream/Sparse, 00:45:43/stopped
```

### What This Proves

- The multicast group `239.2.2.2` is using a shared bidirectional tree.
- The RP for the group is `33.33.33.33`.
- The `Bidir-Upstream` interface is `GigabitEthernet0/2`.
- The router has multiple accepting interfaces for bidirectional multicast traffic.
- Traffic can be forwarded both toward and away from the RP, which matches the video-conferencing use case.

---

## PIM Sparse Mode Validation

**Application:** One-to-many multicast application  
**Multicast group:** `239.1.1.1`  
**Source:** `10.0.0.10`  
**Expected behavior:** Receivers join the shared tree and traffic can move to a source tree.

### Shared Tree Entry

```text
(*,239.1.1.1), 00:48:24/00:03:03, RP 2.2.2.2, flags: SF
  Incoming interface: GigabitEthernet0/1, RPF nbr 10.0.1.2

Outgoing interface list:
  GigabitEthernet0/2, Forward/Sparse, 00:48:24/00:03:03
```

### Source Tree Entry

```text
(10.0.0.10,239.1.1.1), 00:02:04/00:00:54, flags: FT
  Incoming interface: GigabitEthernet0/0, RPF nbr 0.0.0.0, Registering

Outgoing interface list:
  GigabitEthernet0/1, Forward/Sparse, 00:02:04/00:03:22
  GigabitEthernet0/2, Forward/Sparse, 00:02:04/00:03:22
```

### What This Proves

- The group `239.1.1.1` is using PIM Sparse Mode.
- The shared tree entry `(*,239.1.1.1)` exists.
- The RP for the group is `2.2.2.2`.
- The source-specific entry `(10.0.0.10,239.1.1.1)` exists.
- Traffic from source `10.0.0.10` is being forwarded toward multicast receivers.
- The router is registering source traffic toward the RP.

---

## Source-Specific Multicast Validation

**Application:** Secure source-specific application  
**Multicast group:** `232.1.1.1`  
**Allowed source:** `10.0.0.10`  
**Expected behavior:** Receivers join `(S,G)` directly and only receive traffic from `10.0.0.10`.

```text
(10.0.0.10,232.1.1.1), 00:10:43/00:02:44, flags: sT
  Incoming interface: GigabitEthernet0/0, RPF nbr 0.0.0.0

Outgoing interface list:
  GigabitEthernet0/2, Forward/Sparse, 00:06:40/00:02:44
  GigabitEthernet0/1, Forward/Sparse, 00:10:43/00:02:35
```

### What This Proves

- The SSM group `232.1.1.1` is active.
- The multicast tree is source-specific: `(10.0.0.10,232.1.1.1)`.
- Receivers are joining the source directly instead of relying on an RP.
- Only traffic sourced from `10.0.0.10` is expected for this multicast application.
- This matches the security requirement for the application.

---

# Summary

| Multicast Model | Group | Source | RP Required | Validation |
|---|---:|---:|---|---|
| PIM Sparse Mode | `239.1.1.1` | `10.0.0.10` | Yes | `(*,G)` and `(S,G)` entries present |
| Bidirectional PIM | `239.2.2.2` | Multiple possible sources | Yes | `Bidir-Upstream` interface present |
| SSM | `232.1.1.1` | `10.0.0.10` only | No | Source-specific `(S,G)` entry present |

---

## Conclusion

This lab validates three different multicast designs for three different application requirements:

- **PIM Sparse Mode** was used for a traditional one-to-many multicast application.
- **Bidirectional PIM** was used for a video-conferencing-style multicast application.
- **SSM** was used for a source-restricted multicast application where receivers should only accept traffic from `10.0.0.10`.

The output confirms that each multicast model builds the expected multicast state and forwards traffic according to the intended design.


