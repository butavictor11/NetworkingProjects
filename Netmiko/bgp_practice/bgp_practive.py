from netmiko import ConnectHandler
import yaml
from jinja2 import Environment,FileSystemLoader


def generate_config(configs,routers):  ## this functions creates the config to send to the devices
    env=Environment(loader=FileSystemLoader("."))
    template=env.get_template(configs)
    return template.render(**routers)

def deploy(routers,config_set):         ###this function only send config set to routers
    connect=ConnectHandler(** routers)
    connect.enable()
    output=connect.send_config_set(config_set.splitlines())
    show=connect.send_command("\n  sh ip route bgp ")
    print(show)
    connect.disconnect()
    return output



devices=yaml.safe_load(open("/home/viviboss123/Netmiko/Devices/devices.yml")) ##connection info
variables=yaml.safe_load(open("variables.yml")) ### yaml info to be put into j2 template


for dev,name in devices.items():
    config=generate_config("template.j2",variables[dev])   ##### variables[dev]= variables for every device; dev=R1 then R2 then R3 
    result=deploy(name,config)                              #### name=connection params for netmiko; config= real config for every device 
    print(result)
 