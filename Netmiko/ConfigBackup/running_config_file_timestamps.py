from netmiko import ConnectHandler
import time 
devices =[
	{
	'device_type' : 'cisco_ios',
	'host' : '192.168.88.133',
	'username': 'admin',
	'password': 'cisco',
	'secret' : 'cisco'},

	{
	'device_type' : 'cisco_ios',
	'host' : '192.168.88.134',
	'username': 'admin',
	'password': 'cisco',
	'secret' : 'cisco'},

	{
	'device_type' : 'cisco_ios',
	'host' : '192.168.88.135',
	'username': 'admin',
	'password': 'cisco',
	'secret' : 'cisco'}
	]


command="show run"

for device in devices:

    try:
        print(f"\nConnecting to {device['host']}\n")
        net_connect=ConnectHandler(**device)
        net_connect.enable()
        
        print(f"\nConnected to {device['host']}\n")
        
        output=net_connect.send_command(command)
        print(f" \n {output} \n")

        filename=f"running_config_{device['host']}.txt"
        with open(filename,"a") as f:
            f.write("****"*100 + "\n\n\n")
            f.write(f"\nDevice {device['host']} \n")
            f.write(f"Collected on {time.ctime()} \n")
            f.write("****"*100+ "\n\n\n")
            f.write(output)
        print("File created")      

        net_connect.disconnect()
        print(f" \n Disconnected from  {device['host']}\n\n")
        

    except Exception as e:

        print(f" \n Could not connect to {device['host']}:{e}")
