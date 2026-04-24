from netmiko import ConnectHandler
import yaml
from jinja2 import Environment, FileSystemLoader

def load_yaml(path):                            #### argument is path to yaml.file
    with open(path) as f:                       #### goes through file 
        return yaml.safe_load(f)                ####returns a dictionary

def generate_config(template_file,loopbacks):           ####argument is jinja template and loopbacks which is part 
    env=Environment(loader=FileSystemLoader('.'))       ####of jinja template: {% for lo in loopbacks %}
    template=env.get_template(template_file)            ####
    return template.render(loopbacks=loopbacks)         #### puts python variable loopbacks into jinja2
                                                        #### variable loopbacks

def deploy(devices,config_text):                         #### arguments are device->>dictionary containing ssh
    connect=ConnectHandler(**devices)                    #### credentials
    connect.enable()
    output=connect.send_config_set(config_text.splitlines())    #####config has a structure that needs .splitlines()
    connect.disconnect()
    return output 

if __name__ == "__main__":
    devices=load_yaml("/home/viviboss123/Netmiko/Devices/devices.yml")
    # print(f"\n\n\n\n\ndevices: {devices}")
    configs=load_yaml("data.yml")
    
    for name,device in devices.items():             ###name=dictionary key device=dictionary value 
        print(f"generating config for {name}\n")
        config_text=generate_config("template.j2",configs[name]["loopbacks"])
        print(config_text)
        result=deploy(device,config_text)
        print(result)
        