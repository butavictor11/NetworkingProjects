
Here I will store various networking automations project as I develop my skills in this area.

Projects done so far:

                                                Python

1.Configuration Backup Script 
    -> this is my first networking automation project
    -> connects into multiple devices and pulls Running config
    -> generates running config files for every device, mentioning date&time of configuration pull
    -> multiple runs of the script do not override the file but rather append it,thus the file aggregating chronologic running configs

2.Script for creating a looback interface on multiple devices
    -> in this script my goal was to create loopback interfaces on 3 different routers
    -> script is first checking wether the loopback interface exists
    -> if loopback interface already exists "show ip interface brief" is printed for the specific interface
    -> if loopback does not exist script creates the interface and then prints "show ip interface brief" for the interface

3.Script that pulls inventory info and stores it into a CSV file
    -> in this script I used 2 different functions, one to parse output of "show version" command and one to loop though devices and build a list,list is then used to build the CSV file
    -> for this lab, as observed in CSV file, I used 1 Cisco CSR router, 1 Cisco NEXUS and 3 IOSv routers, which added a lot of complexity to the parsing process

4.Created multiple scripts in order to practice jinja2 templates. Examples:
    -> jinja2_loopbacks ->> creates one or more  loopback interfaces on multiple devices using variables defined in a YAML file
    -> bgp_practice ->> establishes neighbour relationships & advertises networks in bgp using a jinja2 template
    -> jinja_bgp_template ->> builds on the previous example ; if statement is used to only advertise next-hop-self to iBGP neighbors
    

                                                Ansible

Project 1
    -> this is an introductive Ansible lab; goal is to get acustomed with Ansbile commands and directories structure & build confidence
    -> topology consists of 2 routers and 2 switches
    -> playbooks:
        i.   version.yml prints output of show version & show inventory 
        ii.  loopbacks.yml creates loopbacks interfaces and sets ip addresses based on varibles file
        iii. backup.yml saves back-up of running config and timestamps it

Project 2
    -> in this project my goal was to fully configure Campus Lan using ansible. To ensure all configuration is done via ansible I connected all swtiches to a management LAN together with my Ubuntu VM. 
    -> ansible folders structure adds roles for better scalability; 
    -> switches are segregated as per roles : access , distribution , core
    -> switch configuration is generated using jinja2 templates
    -> main challenge encountered with this lab was ensuring idempotency. I have used IOSv switches which do not show VLAN definition in "show run" output. As core switches are L3 switches achieving idempotency for those was much easier. Workaround for Access and Distribution layer was to segregate vlan definition and rest of config between 2 different tasks. While true idempotency could not be achieved due to the image limitation the workaround ensure as much as possible of the configuration was idempotent. I plan to play around with idempotency more in Project 3.