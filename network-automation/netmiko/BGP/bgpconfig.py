from netmiko import ConnectHandler
from jinja2 import Environment,FileSystemLoader
import yaml


def build_config(name,jinja,variable_conn,variable_steer):
    variables={
        **variable_conn.get(name,{}),
        **variable_steer.get(name,{})
    }

    env=Environment(loader=FileSystemLoader("/home/viviboss123/Netmiko/BGP/templates"))
    template=env.get_template(jinja)
    return template.render(**variables)


def deploy_function(routers,configs):
    conn=ConnectHandler(**routers)
    conn.enable()

    result=conn.send_config_set(configs.splitlines())
    conn.send_command(" clear ip bgp * soft ")
    conn.disconnect()
    return result







devices=yaml.safe_load(open("/home/viviboss123/Netmiko/BGP/devices/devices.yml"))
variables_connectivity=yaml.safe_load(open("/home/viviboss123/Netmiko/BGP/variables/variables_connectivity.yml"))
variables_steering=yaml.safe_load(open("/home/viviboss123/Netmiko/BGP/variables/variables_steering.yml"))

for name,dev in devices.items():
    configs=build_config(name,"master_template.j2",variables_connectivity,variables_steering)
    output=deploy_function(dev,configs)
    print(output)
    # print(configs)