from netmiko import ConnectHandler
import yaml

devices = yaml.safe_load(open("/home/viviboss123/Netmiko/BGP/devices/devices.yml"))

output_file = "configs.txt"



for name, dev in devices.items():

    print(f"\n>>> Trying {name} ({dev['host']})")

    try:
        conn = ConnectHandler(**dev)
        print("Connected!")
        configs=["do show run | sect bgp","do show run | sect route-map", "do show run | sect prefix-list"]
        conn.send_command("do clear ip bgp * soft ")
        conn.disconnect()

    except Exception as e:
        print(f"ERROR on {name}: {e}")

