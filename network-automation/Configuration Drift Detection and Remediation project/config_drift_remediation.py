import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from lxml import etree
from ncclient import manager
from ncclient.operations import RPCError
from deepdiff import DeepDiff


PROJECT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = PROJECT_DIR / "templates"
HOST_VARS_DIR = PROJECT_DIR / "hosts.vars"
INVENTORY_FILE = PROJECT_DIR / "inventory.yml"
RENDERED_DIR = PROJECT_DIR / "rendered"
IOS_XE_NATIVE_NS = "http://cisco.com/ns/yang/Cisco-IOS-XE-native"
INTERFACE_FILTER = f"""
<native xmlns="{IOS_XE_NATIVE_NS}">
  <interface/>
</native>
"""
BGP_FILTER = f"""
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"
      xmlns:bgp="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
    <router>
        <bgp:bgp/>
    </router>
</native>
"""
ROUTE_FILTER=f"""
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
 	<ip>
		<route/>
	</ip>
</native>
"""

def load_yaml(filename):
    with open(filename, "r") as f:
        data = yaml.safe_load(f)
    if data is None:
        raise ValueError(f"{filename} is empty")
    return data


def create_config(template_names, variables):
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    rendered_configs = []
    for template_name in template_names:
        template = env.get_template(template_name)
        rendered_configs.append((template_name, template.render(**variables)))
    return rendered_configs

def desired_interfaces_to_python(variables):
    desired = {}

    for interface in variables.get("interfaces", []):
        interface_name = f"{interface['type']}{interface['name']}"

        desired[interface_name] = {
            "ip": str(interface["ip"]),
            "mask": str(interface["mask"]),
        }

    return desired

def desired_routes_to_python(variables):
    desired = {}

    for route in variables.get("routes", []):
        address=f"{route["ip"]}/{route["mask"]}"
        desired[address]= {
            "ip": str(route["ip"]),
            "mask": str(route["mask"]),
            "next_hop":str(route["next_hop"]),
        }

    return desired

def desired_bgp_to_python(variables):
    bgp=variables.get("bgp",{})
    desired={
        "asn": str(bgp["asn"]),
        "router_id":str(bgp["router_id"]),
        "neighbors": {},
        "networks": set(),

    }

    for neighbor in bgp.get("neighbors",[]):
        desired["neighbors"][str(neighbor["nei_rid"])]={
            "remote_as": str(neighbor["remote_as"]),
            "ebgp_hops": str(neighbor["ebgp_hops"]),
            "update_source": f"Loopback{neighbor["nei_loopback"]}" if neighbor["nei_loopback"] is not None else None,}
        
    for network in bgp.get("bgp_networks"):
        ip=network["ip"]
        mask=network["mask"]
        desired["networks"].add((ip,mask))

    return desired


def save_rendered_config(name, template_name, rendered_config):
    RENDERED_DIR.mkdir(exist_ok=True)
    output_name = template_name.replace(".j2", "")
    output_file = RENDERED_DIR / f"{name}_{output_name}.xml"

    with open(output_file, "w") as f:
        f.write(rendered_config)
    print(f"Rendered XML saved to {output_file}")


def push_config(templates,variables, device, name):
    configs = create_config(templates, variables)

    try:
        with manager.connect(
            host=device["host"],
            port=device.get("port", 830),
            username=device["username"],
            password=device["password"],
            hostkey_verify=False,
            allow_agent=False,
            look_for_keys=False,
            timeout=30,
            device_params={"name": "csr"},
        ) as m:
            for template_name, rendered_config in configs:
                print(f"Pushing {template_name} to {name}...")
                save_rendered_config(name, template_name, rendered_config)

                rpc = etree.fromstring(rendered_config.encode())
                operation = rpc[0] if rpc.tag.endswith("rpc") else rpc
                m.dispatch(operation)

    except RPCError as error:
        print(f"NETCONF RPC error on {name}:")
        print(error)

    except Exception as error:
        print(f"Connection or script error on {name}:")
        print(error)

def get_actual_interfaces(device):
    with manager.connect(
        host=device["host"],
        port=device.get("port", 830),
        username=device["username"],
        password=device["password"],
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False,
        timeout=30,
        device_params={"name": "csr"},
    ) as m:
        response = m.get_config(
            source="running",
            filter=("subtree", INTERFACE_FILTER),
        )
    return response.data_xml

def get_actual_bgp(device):
    with manager.connect(
        host=device["host"],
        port=device.get("port", 830),
        username=device["username"],
        password=device["password"],
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False,
        timeout=30,
        device_params={"name": "csr"},
    ) as m:
        response = m.get_config(
            source="running",
            filter=("subtree", BGP_FILTER),
        )
    return response.data_xml


def get_actual_routes(device):
    with manager.connect(
        host=device["host"],
        port=device.get("port", 830),
        username=device["username"],
        password=device["password"],
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False,
        timeout=30,
        device_params={"name": "csr"},
    ) as m:
        response = m.get_config(
            source="running",
            filter=("subtree", ROUTE_FILTER),
        )
    return response.data_xml
def actual_bgp_to_python(xml_data):
    root = etree.fromstring(xml_data.encode()) ##->> converts string in xml tree
    ns = {                                          ## that python can search in
        "ios": IOS_XE_NATIVE_NS,
        "bgp": "http://cisco.com/ns/yang/Cisco-IOS-XE-bgp",
    }
    actual={
        "asn":None,
        "router_id":None,
        "neighbors":{},
        "networks" :set()
    }

    bgp_root= root.find(".//bgp:bgp",namespaces=ns)
    if bgp_root is None:
        return actual
    
    actual["asn"]=bgp_root.findtext("bgp:id",namespaces=ns)
    actual["router_id"]=bgp_root.findtext("bgp:bgp/bgp:router-id/bgp:ip-id",namespaces=ns)
    for neighbor in bgp_root.findall("bgp:neighbor",namespaces=ns):
        neighbor_id= neighbor.findtext("bgp:id",namespaces=ns)
        if neighbor_id == None:
            continue
        loopback=neighbor.findtext("bgp:update-source/bgp:interface/bgp:Loopback",namespaces=ns)
        actual["neighbors"][neighbor_id]={
            "remote_as": neighbor.findtext("bgp:remote-as",namespaces=ns),
            "ebgp_hops": neighbor.findtext("bgp:ebgp-multihop/bgp:max-hop",namespaces=ns),
            "update_source": f"Loopback{loopback}" if loopback else None,
        }
    for network in bgp_root.findall(".//bgp:network/bgp:with-mask",namespaces=ns):
        ip=network.findtext("bgp:number",namespaces=ns)
        mask=network.findtext("bgp:mask",namespaces=ns)
        if ip and mask:
            actual["networks"].add((ip,mask))
    return actual

def actual_interfaces_to_python(xml_data):
    actual = {} ##->> create empty dictionary to sore
    root = etree.fromstring(xml_data.encode()) ##->> converts string in xml tree
    ns = {                                          ## that python can search in
        "ios": IOS_XE_NATIVE_NS,
    }

    interface_root = root.find(".//ios:interface", namespaces=ns)
        ## ^ finds interface section anywhere in xml tree
    if interface_root is None:
        return actual

    for interface in interface_root:        ##loops through every interface
        interface_type = etree.QName(interface).localname

        name = interface.findtext("ios:name", namespaces=ns)

        ip = interface.findtext(
            "ios:ip/ios:address/ios:primary/ios:address",
            namespaces=ns,
        )
        mask = interface.findtext(
            "ios:ip/ios:address/ios:primary/ios:mask",
            namespaces=ns,
        )

        if name is None or ip is None or mask is None:
            continue

        interface_name = f"{interface_type}{name}"

        actual[interface_name] = {
            "ip": ip,
            "mask": mask,
        }

    return actual

def actual_routes_to_python(xml_data):
    actual={}
    root = etree.fromstring(xml_data.encode()) ##->> converts string in xml tree
    ns = {                                          ## that python can search in
        "ios": IOS_XE_NATIVE_NS,
    }
    route_root = root.find(".//ios:route", namespaces=ns)
    if route_root is None:
        return actual

    for route in route_root:
        route_type = etree.QName(route).localname

        if route_type != "ip-route-interface-forwarding-list":
            continue

        prefix=route.findtext("ios:prefix",namespaces=ns)
        mask=route.findtext("ios:mask",namespaces=ns)
        next_hop = route.findtext("ios:fwd-list/ios:fwd", namespaces=ns)

        if prefix is None or mask is None or next_hop is None:
            continue
        
        route_name= f"{prefix}/{mask}"

        actual[route_name]={
            "ip": prefix,
            "mask": mask,
            "next_hop": next_hop
        }
    return actual



def remediate_section(
    name,
    section_name,
    diff,
    template,
    desired_section,
    get_actual_func,
    actual_to_python_func,
    device_vars,
    device,
):
    if not diff:
        return

    print(f"{section_name} drift found on {name}")
    print(diff.pretty())

    answer = input(f"\nRemediate {section_name} config on {name}? yes/no: ").strip().lower()
    if answer != "yes":
        print(f"Skipping {section_name} remediation on {name}")
        return

    push_config([template], device_vars, device, name)

    actual_xml = get_actual_func(device)
    actual_section = actual_to_python_func(actual_xml)
    remedy_diff = DeepDiff(desired_section, actual_section, ignore_order=True)

    if not remedy_diff:
        print(f"{section_name} remediated on {name}")
    else:
        print(f"{section_name} still has drift on {name}")
        print(remedy_diff.pretty())


def main():
    devices = load_yaml(INVENTORY_FILE)

    for name, device in devices.items():
        var_files = HOST_VARS_DIR / f"{name}.yml"
        device_vars = load_yaml(var_files)
        desired={
            "interfaces": desired_interfaces_to_python(device_vars),
            "routes": desired_routes_to_python(device_vars),
            "bgp": desired_bgp_to_python(device_vars)
        }

        actual={
            "interfaces" : actual_interfaces_to_python(get_actual_interfaces(device)),
            "routes": actual_routes_to_python(get_actual_routes(device)),
            "bgp": actual_bgp_to_python(get_actual_bgp(device))
        }
        
        print(f"\n {name} \n")
        diff_interfaces= DeepDiff(desired["interfaces"], actual["interfaces"], ignore_order=True)
        diff_routes= DeepDiff(desired["routes"], actual["routes"], ignore_order=True)
        diff_bgp= DeepDiff(desired["bgp"], actual["bgp"], ignore_order=True)
    
        if not diff_interfaces and not diff_routes and not diff_bgp:
            print(f"No drift on {name}")
            continue

        remediate_section(
            name,
            "Interfaces",
            diff_interfaces,
            "interfaces.j2",
            desired["interfaces"],
            get_actual_interfaces,
            actual_interfaces_to_python,
            device_vars,
            device,
        )

        remediate_section(
            name,
            "Static routing",
            diff_routes,
            "static_routing.j2",
            desired["routes"],
            get_actual_routes,
            actual_routes_to_python,
            device_vars,
            device,
        )

        remediate_section(
            name,
            "BGP",
            diff_bgp,
            "bgp.j2",
            desired["bgp"],
            get_actual_bgp,
            actual_bgp_to_python,
            device_vars,
            device,
        )




if __name__ == "__main__":
    main()
