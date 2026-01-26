from netmiko import ConnectHandler
import csv
import time
devices=[]

with open("/home/viviboss123/Netmiko/Devices/devices.csv") as f:
    reader=csv.DictReader(f)
    for row in reader:
        devices.append({
            'device_type':row['device_type'],
            'host':row['host'],
            'username':row['username'],
            'password':row['password'],
            'secret':row['secret']
        })


for i, dev in enumerate(devices,start=1):

    try:

        net_connect=ConnectHandler(**dev)
        net_connect.enable()
        print(f"Connected to host {dev['host']}\n")
        loop_ip=f"11.11.11.{i}"
        commands=["int loop98",f"ip address {loop_ip} 255.255.255.255","no shut"]
        
        output=net_connect.send_command("show ip int br | i 98")
        print(f"\n {output}")

        if not output.strip():
            net_connect.send_config_set(commands)
            print("\n Loop interface created ")
            time.sleep(2)
            int_check=net_connect.send_command("show ip int br | i 98")
            print(f"\n Inferface created for host {dev['host']} \n {int_check}")
    
    except Exception as e:
        print(f"Could not connect to host {dev['host']}")
        

