from netmiko import ConnectHandler
import csv
import re
import time
import os
devices=[]


def parse_device_info(show_version_output):
    OS=version=uptime="N/A"                                                 ### here i found regex by trail and error; i allowed -; A-z; a-z and " ";; this
                                                                            ### means that with some devices it breaks at () and with some it breaks at ,     
    OS_match=re.search(r"[Cc]isco\s([-A-Za-z ]+)",show_version_output)      ### either way it worked out            
    if OS_match:
        OS=OS_match.group(1)
                          

    version_match=re.search(r"[Vv]ersion\s+([0-9][0-9A-Za-z().]+)",show_version_output)      ###here I used 2 regex groups to force starting with a decimal
    if version_match:                                                                        ###in second group I allow 0-9 a-z A-Z () and . 
        version=version_match.group(1)
         
        
    uptime_match=re.search(r"[Uu]ptime is (.*)",show_version_output)             ### (.*) matches to the end of the the line
    if uptime_match:
        uptime=uptime_match.group(1)
         
   
    return OS,version,uptime                ### main goal of this function to extract OS, version and uptime 


def inventory(devices):
    results=[]
    for dev in devices:                                         ###looping through devices
        try:
            net_connect=ConnectHandler(**dev)
            if dev['device_type'] not in ['cisco_nxos']:        ####net_connect.enable() breaks script if sent to a nexus device so I had to bypass that
                net_connect.enable()
            hostname_to_be_parsed=net_connect.send_command("sh run | include hostname")     ##pulling hostname
            hostname=hostname_to_be_parsed.replace("hostname","").strip()                   ##removing extra 


            sh_version=net_connect.send_command("show version")
            os,version,uptime=parse_device_info(sh_version)         ####calling function 
            net_connect.disconnect()

            results.append({                            ##appending to build the list of dictionaries
                'host':dev['host'],
                'hostname':hostname,
                'os':os,
                'version':version,
                'uptime':uptime
            })
        except Exception as e:
            print(f"{devices['host']} is unreachable")

            result.append({                             ##appending to build the list of dictionaries
                'host':devices['host'],
                'os':"N/a",
                'version':"N/A",
                'uptime':"N/A"
            })
    return results


    
                                            
with open("/home/viviboss123/Netmiko/Devices/devices.csv") as f:
    reader=csv.DictReader(f)
    for row in reader:
        devices.append({                                ####reading csv file 
        'device_type':row['device_type'],
        'host':row['host'],
        'username':row['username'],
        'password':row['password'],
        'secret':row['secret']
        })

    sanky=inventory(devices)
    print(f"\n{sanky}")
    
with open("inventory.csv", "w",newline="") as f:                                        ####generating a CSV file 
    writer=csv.DictWriter(f,fieldnames=["host","hostname","os","version","uptime"])     ####fields to be included in CSV file 
    writer.writeheader()
    writer.writerows(sanky)

