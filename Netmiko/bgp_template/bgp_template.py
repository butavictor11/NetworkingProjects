from netmiko import ConnectHandler
from jinja2 import Environment,FileSystemLoader
import yaml



def generate_config(template_file,router):
    env=Environment(loader=FileSystemLoader("."))   ### this load jinja2 "engine"
    template=env.get_template(template_file)
    return template.render(**router)

def deploy(devices,config_text):                         #### arguments are device->>dictionary containing ssh
    connect=ConnectHandler(**devices)                    #### credentials
    connect.enable()
    output=connect.send_config_set(config_text.splitlines())    #####config has a structure that needs .splitlines() to send lines 1 by 1
    connect.disconnect()
    return output 

if __name__ == "__main__":

    devices=yaml.safe_load(open("/home/viviboss123/Netmiko/Devices/devices.yml"))       #### dictionary on connection details from every router
    template=yaml.safe_load(open("data.yml"))
    for name,dev in devices.items():
        
        config=generate_config("jinja_bgp_template.j2",template[name])
      
        result=deploy(dev,config)
        print(result)
        

    

    
   
    

    