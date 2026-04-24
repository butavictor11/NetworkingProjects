from netmiko import ConnectHandler
from jinja2 import Environment,FileSystemLoader
import yaml


def build_full_config(name, connectivity_data, steering_data, config):
    merged_variables={
        **connectivity_data.get(name,{}),
        **steering_data.get(name,{})
        }

    env=Environment(loader=FileSystemLoader("."))
    template=env.get_template(config)
    return template.render(**merged_variables) 
           

def deploy(routers,config_set):         ###this function only send config set to routers
    connect=ConnectHandler(** routers)
    connect.enable()
    connect.send_command("clear ip bgp * soft in")
    
    output=connect.send_config_set(config_set.splitlines())
    connect.disconnect()
    return output


if __name__ == "__main__":


    devices=yaml.safe_load(open("/home/viviboss123/Netmiko/Devices/devices.yml"))
    variables_connectivity=yaml.safe_load(open("variables_connectivity.yml"))
    variables_steering=yaml.safe_load(open("variables_steering.yml"))

    for name,dev in devices.items():
        config=build_full_config(name, variables_connectivity, variables_steering , "master_template.j2")
        result=deploy(dev,config)
        print(result)

    
   
   
        