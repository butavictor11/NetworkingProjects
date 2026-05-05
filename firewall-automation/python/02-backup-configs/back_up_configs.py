from pathlib import Path
from datetime import datetime
import yaml
from panos.firewall import Firewall
from panos.errors import PanDeviceError


BASE_DIR = Path(__file__).resolve().parents[2]
INVENTORY_FILE = BASE_DIR / "inventory" / "firewalls.yml"
BACKUP_DIR = Path(__file__).resolve().parent / "backups"

def load_inventory():
    with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["firewalls"]
    
def create_backup_directory():
    BACKUP_DIR.mkdir(exist_ok=True)

def backup_firewall_config(name, fw_data):
    print(f"\n Backing up {name.upper()} ({fw_data['hostname']})\n")

    fw=Firewall(
        hostname=fw_data["mgmt_ip"],
        api_username=fw_data["username"],
        api_password=fw_data["password"],
    )

    try:
        fw.refresh_system_info()

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_filename=f"{name}_{fw_data['hostname']}_{timestamp}.xml"
        backup_path=BACKUP_DIR / backup_filename

        config_xml=fw.op("show config running",xml=True)

        with open(backup_path, "wb") as file:
             file.write(config_xml)
        print(f"Status: Backup Created at {backup_path}")
        return True
    except PanDeviceError as error:
        print(f"Backup failed; error code: {error}")
        return False
    except Exception as error:
        print("Status: FAILED")
        print(f"Unexpected error: {error}")
        return False
    
def main():
    create_backup_directory()
    result={}
    firewalls= load_inventory()
    # print(firewalls)
    for name,fw_data in firewalls.items():
        result[name]= backup_firewall_config(name, fw_data)

    
if __name__ == "__main__":
    main()