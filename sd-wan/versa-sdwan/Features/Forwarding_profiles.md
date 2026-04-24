For customer German_Airways I've created multiple forwarding profiles. 

Traffic is separated into the following 5 FW profiles:
<img width="1725" height="289" alt="image" src="https://github.com/user-attachments/assets/d365425f-12ef-4092-ac24-9bdb6ced8ed7" />
Deny_risky_traffic ->> blocks access to risky URL's(gambling, bots_net etc)
Real_time ->> used for real time apps such as ZOOM or MS TEAMS. This forwarding profile has the strictest SLA profile
Business_Critical ->> DNS RDP 
Bulk_traffic ->> FTP,Windows_update etc; I've also added Youtube for easier lab validation
Standard_traffic ->> all internet browsing goes here(HTTP HTTPS)


I have also created the followig SLA profiles to ensure customer application choose the best WAN. Each SLA is continuosly evaluated.

<img width="1830" height="192" alt="image" src="https://github.com/user-attachments/assets/64b11af0-75d5-4e1b-9669-7cfd2ad09762" />

Each FW profile works as expected:
<img width="2206" height="328" alt="image" src="https://github.com/user-attachments/assets/bdaa7f96-70e6-42da-a4f2-1a6061f16949" />

Using a LINUX VM I'm simulating bad path conditions on MPLS link. 

sudo tc qdisc replace dev ens4 root netem delay 90ms loss 1.5%  ->> this commands violates SLA of Real_time Forwarding profile so traffic is shifted to Internet link.
No other FW profile is affected.

<img width="1837" height="495" alt="image" src="https://github.com/user-attachments/assets/67c2d308-d761-44e9-a5f6-a6b8824431e2" />

<img width="1828" height="267" alt="image" src="https://github.com/user-attachments/assets/5d6c2f18-a979-48bb-b4eb-ae284cb1cc40" />

The following screeshot is taken from Versa Analytics and proves all SLA profiles are continously evaluated and logged.

<img width="2053" height="615" alt="image" src="https://github.com/user-attachments/assets/8e5a9647-2160-4ccb-8c5d-8d9e4f8094fe" />








