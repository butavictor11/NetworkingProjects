In this directory I have multiple Netmiko automation scripts.

1.Inventory/inventory.py ->>  pulls hostname,os,version,uptime information into a CSV file

2.ConfigBackup/config_backup.py ->> pull running config from multiple devices and stores it in separate files

3.bgp_practice/bgp_practice.py ->> using j2 templates and Netmiko I create bgp neighbourships btwn devices and advertise networks

4.BGP/bgp_config.py ->> works like above script but also I influence traffic steering based and create route-reflectors using variables stored in yml
