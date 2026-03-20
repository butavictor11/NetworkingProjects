This project documents a hands-on Versa SD-WAN lab built in EVE-NG to simulate a regional airport-style hub-and-spoke deployment.

The lab was designed to demonstrate how centralized infrastructure services, customer segmentation, and resilient SD-WAN architecture can be combined in a realistic multi-tenant environment. It includes redundant hub design, centralized authentication, centralized NTP, dual transport underlays, and validation of failover behavior.

A key part of the design is the use of three suborganisations at each site, with each suborganisation representing a different customer tenant. This allowed the lab to model shared SD-WAN infrastructure delivered by a service provider while maintaining logical separation between customers.

The main focus of the lab was to build and validate:

- a hub-and-spoke SD-WAN topology
- multi-tenant segmentation using suborganisations
- centralized RADIUS authentication
- centralized NTP services
- MPLS-preferred forwarding with Internet backup
- hub-side high availability concepts
- VRRP-based gateway resiliency on the hub services LAN

- The objectives of this lab were:

- build a Versa SD-WAN hub-and-spoke topology in EVE-NG
- simulate multiple branch sites connected to a regional hub
- model **three separate customer environments** using suborganisations
- provide centralized infrastructure services from the hub site
- validate administrator authentication through a centralized FreeRADIUS server
- validate reachability to centralized NTP services
- test transport behavior across MPLS and Internet links
- design and test a redundant hub model with active/standby behavior
- understand how VRRP supports gateway resiliency on a shared L2 service LAN
- document configuration decisions, issues encountered, and lessons learned
- study scalability and ease of deployement of Versa SD-WAN using templates


Topology diagram:
<img width="981" height="683" alt="image" src="https://github.com/user-attachments/assets/74475cc1-5324-4fff-af0e-f0402e764367" />

My topology is separated into:
1. Versa Headend
2. 2 WAN underlays (MPLS and INTERNET transport)
3. One hub site where I've deployed 2 VOS devices for a redundant hub model with active/standby behavior. HUB1 acts as active while HUB2 is the standby device. The hub site also hosts centralized RADIUS and NTP servers. I've chosed the geographical location of this site to be in Brussels,Belgium
4. 2 spoke sites(Schiphol Airport and Frankfurt Airport)

Using Versa suborganisation I've created 3 fictional airline companies that operate in both airports.I will refer to them as clients in future references. 

Client Dutch Airways has opted for a standard Spoke-to-Hub-only connection and chose to have it's internet breakout centralized at Hub site in Brussels.
Client German Airways has opted for a Spoke-to-Spoke-via-Hub connection, as it has a operational requirement that offices in various airports can communicate between themselves.As for internet breakout customer has also opted for centralized interner brekout at Brussels site.
Client French Airways has opted for a Spoke-to-Hub-only connection, where each site has DIA(direct internet access).



