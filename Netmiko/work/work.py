
import argparse
import getpass
import os
import re
from datetime import datetime
from typing import List, Dict, Optional

import pandas as pd
from netmiko import ConnectHandler


# -------------------------
# 1) Parsing logic
# -------------------------

def parse_show_int_desc(output: str) -> List[Dict[str, str]]:
    """
    Parse Cisco-style `show interfaces description` output into structured rows.

    Typical Cisco IOS output looks like:

        Interface              Status         Protocol Description
        Gi0/0                  up             up       Uplink to ISP
        Gi0/1                  administratively down down   --
        Gi0/0.120              up             up       --- Airportnet airportnet_icn

    We want to convert each data line into a dict like:
        {
          "interface": "Gi0/0",
          "state": "up/up",
          "description": "Uplink to ISP"
        }

    Why parse?
    - CLI output is "human-readable text"
    - CSV needs "structured data" (rows + columns)
    """

    rows: List[Dict[str, str]] = []

    # This regex matches ONE interface line.
    #
    # Explanation:
    # - (?P<intf>\S+)   : capture the first "word" (non-space) as interface name
    # - \s+             : one or more spaces
    # - (?P<status>\S+) : capture the next word as status
    # - \s+             : spaces
    # - (?P<proto>\S+)  : capture the next word as protocol
    # - \s*             : optional spaces
    # - (?P<desc>.*)    : capture the rest of the line as description (can be empty)
    #
    # NOTE: This is a "best effort" parser for common IOS formatting.
    line_re = re.compile(
        r"^(?P<intf>\S+)\s+(?P<status>\S+)\s+(?P<proto>\S+)\s*(?P<desc>.*)$"
    )

    # We loop line-by-line through the CLI output
    for line in output.splitlines():
        line = line.rstrip()

        # Skip empty lines
        if not line:
            continue

        # Some outputs include a header like:
        # "Interface Status Protocol Description"
        # We detect it and skip it.
        low = line.lower()
        if low.startswith("interface") and "protocol" in low:
            continue

        # In labs, sometimes prompt lines accidentally get captured, like:
        # "R1# show interfaces description"
        # This is a simple guard for common patterns.
        if line.startswith(("R1(", "R2(", "R3(")):
            continue

        # Try matching the line with our regex.
        m = line_re.match(line)

        # If the line doesn't match the expected pattern, skip it.
        # (Better than crashing.)
        if not m:
            continue

        # Extract the named capture groups from regex
        intf = m.group("intf")
        status = m.group("status")
        proto = m.group("proto")
        desc = (m.group("desc") or "").strip()

        # Clean up description if it’s just placeholders
        if desc in {"--", "---"}:
            desc = ""

        # Some outputs may put a separator like "--- " before the description
        # Example: "--- Airportnet airportnet_icn"
        # This removes that leading "--- " if present.
        desc = re.sub(r"^---\s*", "", desc).strip()

        # Build a dict (one row)
        rows.append(
            {
                "interface": intf,
                # Combine status/proto into a single column for simplicity
                "state": f"{status}/{proto}",
                "description": desc,
            }
        )

    return rows


# -------------------------
# 2) SSH connection helper
# -------------------------

def ssh_connect(
    host: str,
    username: str,
    password: str,
    secret: Optional[str] = None,
    device_type: str = "cisco_ios",
):
    """
    Create a Netmiko SSH session to the device.

    - device_type "cisco_ios" is correct for most IOS / IOS-XE CLIs.
    - secret is optional (enable password). If provided, we enter enable mode.
    """
    device = {
        "device_type": device_type,
        "host": host,
        "username": username,
        "password": password,
    }

    if secret:
        device["secret"] = secret

    conn = ConnectHandler(**device)

    # If enable secret was provided, enter privileged exec mode
    if secret:
        conn.enable()

    return conn


# -------------------------
# 3) Output filename helper
# -------------------------

def build_base_out(host: str, base_out: Optional[str]) -> str:
    """
    Decide the base filename for exports.

    If user passes --base-out:
        use it (without extension)
    Else:
        create something like:
          <host>_show_int_desc_YYYYMMDD_HHMMSS
    """
    if base_out:
        # If user passes "output.csv", remove .csv so we can add extensions ourselves.
        return os.path.splitext(base_out)[0]

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_host = host.replace(":", "_")  # avoid weird filenames on IPv6
    return f"{safe_host}_show_int_desc_{ts}"


# -------------------------
# 4) Turn rows into DataFrame
# -------------------------

def rows_to_df(rows: List[Dict[str, str]]) -> pd.DataFrame:
    """
    Convert list-of-dicts into a pandas DataFrame.

    If parsing returns zero rows, we return a DataFrame with one "warning" row
    to make it obvious something went wrong (instead of exporting an empty file).
    """
    df = pd.DataFrame(rows, columns=["interface", "state", "description"])

    if df.empty:
        df = pd.DataFrame(
            [{
                "interface": "",
                "state": "",
                "description": "No rows parsed. Check device output or parser regex.",
            }]
        )

    return df


# -------------------------
# 5) Export
# -------------------------

def export_csv(df: pd.DataFrame, csv_path: str) -> None:
    """
    Export DataFrame to CSV.

    encoding="utf-8-sig" helps Excel open UTF-8 CSVs correctly (adds BOM).
    """
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")


def export_xlsx(df: pd.DataFrame, xlsx_path: str, sheet_name: str = "interfaces") -> None:
    """
    Optional: export to Excel as well.
    You can remove this function if you want CSV only.
    """
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheet_name[:31], index=False)


# -------------------------
# 6) Main CLI program
# -------------------------

def main():
    """
    This is the entry point when you run the script like:

      python script.py --host 10.0.0.1 --username admin

    It:
    - reads CLI args
    - prompts password if needed
    - connects
    - runs command
    - parses output
    - exports to CSV (+ optional XLSX)
    """
    parser = argparse.ArgumentParser(
        description="Export `show interfaces description` to CSV (simple learning version)."
    )

    # Required connection info
    parser.add_argument("--host", required=True, help="Router IP/hostname")
    parser.add_argument("--username", required=True, help="SSH username")

    # Optional password: if not provided, we prompt securely
    parser.add_argument("--password", help="SSH password (if omitted, you will be prompted)")

    # Optional enable secret
    parser.add_argument("--secret", help="Enable secret (enable password), if needed")

    # Command to run (kept flexible so you can experiment)
    parser.add_argument(
        "--command",
        default="show interfaces description",
        help="Command to run for interface list",
    )

    # Output file naming
    parser.add_argument(
        "--base-out",
        help="Base output name (no extension). Creates .csv (and .xlsx if enabled)",
    )

    # Optional: save the raw command output to a text file for debugging
    parser.add_argument(
        "--save-raw",
        help="Optional: save raw command output to this .txt path",
    )

    # Optional: Excel settings
    parser.add_argument("--sheet", default="interfaces", help="Excel sheet name")

    # If you want CSV only, you can delete Excel entirely OR keep it and ignore it.
    parser.add_argument(
        "--no-xlsx",
        action="store_true",
        help="If set, do NOT export XLSX (CSV only).",
    )

    args = parser.parse_args()

    # If password wasn't provided as an argument, prompt for it (hidden input)
    password = args.password or getpass.getpass("SSH Password: ")

    conn = ssh_connect(
        host=args.host,
        username=args.username,
        password=password,
        secret=args.secret,
        device_type="cisco_ios",
    )

    try:
        # 1) Run the show command
        raw_desc = conn.send_command(args.command)

        # 2) Optionally save raw output (useful while learning parsing)
        if args.save_raw:
            with open(args.save_raw, "w", encoding="utf-8") as f:
                f.write(raw_desc)

        # 3) Parse raw output into structured rows
        rows = parse_show_int_desc(raw_desc)

        # 4) Convert rows into a DataFrame
        df = rows_to_df(rows)

        # 5) Build output filenames and export
        base = build_base_out(args.host, args.base_out)
        csv_file = base + ".csv"
        export_csv(df, csv_file)

        print(f"Parsed rows: {len(rows)}")
        print(f"Saved CSV : {csv_file}")

        # Optional XLSX export
        if not args.no_xlsx:
            xlsx_file = base + ".xlsx"
            export_xlsx(df, xlsx_file, sheet_name=args.sheet)
            print(f"Saved XLSX: {xlsx_file}")

    finally:
        # Always close SSH session, even if an exception happens
        conn.disconnect()


if __name__ == "__main__":
    main()