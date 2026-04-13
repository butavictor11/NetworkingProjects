In this project I'm exploring Protocol Independent Multicast(PIM)

Topology:
<img width="791" height="344" alt="image" src="https://github.com/user-attachments/assets/e6dd8f45-c356-4fd5-a34f-efc3cf669808" />

Let's assume there is an application that multicasts in a one-to-many fashion from Source. Multicast group for this application is 239.1.1.1.

There is another application that the company uses for video-conferencing. Multicast group for this application is 239.2.2.2.

Also,there is another application that requires that hosts only receive traffic from 10.0.0.10 for security. Multicast group for this application is 232.1.1.1.

I will use BSR to advertise RP for both cases.

I will configure R3's loobaack0 as main RP(priority 130) for group 239.1.1.1 and loopback 1 as redundant RP(priority 100) for group 239.2.2.2.

I will configure R2's loopback 0 as redundant RP(priority 100) for group 239.1.1.1 and loopback 1 as main RP(priority 130) for group 239.2.2.2

Bidirectional pim :
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

 SPARSE MODE ->>

(*, 239.1.1.1), 00:48:24/00:03:03, RP 2.2.2.2, flags: SF
Incoming interface: GigabitEthernet0/1, RPF nbr 10.0.1.2
Outgoing interface list:
 GigabitEthernet0/2, Forward/Sparse, 00:48:24/00:03:03

(10.0.0.10, 239.1.1.1), 00:02:04/00:00:54, flags: FT

Incoming interface: GigabitEthernet0/0, RPF nbr 0.0.0.0, Registering

Outgoing interface list:
 GigabitEthernet0/1, Forward/Sparse, 00:02:04/00:03:22
 GigabitEthernet0/2, Forward/Sparse, 00:02:04/00:03:22

 SSM ->
(10.0.0.10, 232.1.1.1), 00:10:43/00:02:44, flags: sT

Incoming interface: GigabitEthernet0/0, RPF nbr 0.0.0.0

Outgoing interface list:
 GigabitEthernet0/2, Forward/Sparse, 00:06:40/00:02:44
 GigabitEthernet0/1, Forward/Sparse, 00:10:43/00:02:35


