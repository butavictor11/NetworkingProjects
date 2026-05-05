
from pathlib import Path
import yaml
from panos.firewall import Firewall
from panos.errors import PanDeviceError


BASE_DIR = Path(__file__).resolve().parents[2]
INVENTORY_FILE = BASE_DIR / "inventory" / "firewalls.yml"


def load_inventory():
    with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["firewalls"]


def check_firewall(name, fw_data):
    print(f"\n=== Checking {name.upper()} ({fw_data['hostname']}) ===")

    fw = Firewall(
        hostname=fw_data["mgmt_ip"],
        api_username=fw_data["username"],
        api_password=fw_data["password"],
    )

    try:
        system_info = fw.refresh_system_info()
        print("Status: CONNECTED")
        print(f"Hostname: {getattr(system_info, 'hostname', getattr(system_info, 'devicename', 'N/A'))}")
        print(f"Model: {getattr(system_info, 'platform', getattr(system_info, 'model', 'N/A'))}")
        print(f"Serial: {getattr(system_info, 'serial', 'N/A')}")
        print(f"PAN-OS Version: {getattr(system_info, 'version', 'N/A')}")

        return True

    except PanDeviceError as error:
        print("Status: FAILED")
        print(f"PAN-OS error: {error}")
        return False

    except Exception as error:
        print("Status: FAILED")
        print(f"Unexpected error: {error}")
        return False


def main():
    firewalls = load_inventory()
    results = {}
    print(firewalls.items())
    for name, fw_data in firewalls.items():
        results[name] = check_firewall(name, fw_data)

    # print("\n=== SUMMARY ===")
    # for name, status in results.items():
    #     print(f"{name}: {'OK' if status else 'FAILED'}")


if __name__ == "__main__":
    main()
