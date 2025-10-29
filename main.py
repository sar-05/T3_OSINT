"""Execute host scans."""

from argparse import ArgumentParser
from json import dump
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from active_scan import active_scan


def passive_scan(ip):
    """Execute the passive scan."""
    print(f"Passive scan of {ip} will go here")


def save_scan(scan: dict, path: str):
    """Recives a dict and saves it as JSON to a file."""
    if scan:
        with Path(path).open("w", encoding="utf-8") as f:
            dump(scan, f, indent=4)
        print(f"Scan saved to {path}")


def main():
    """Execute the passive scan. Execute the active scan only if specified."""
    parser = ArgumentParser(description="Enable active execution")
    parser.add_argument(
        "--active",
        action="store_true",
        help="Input IP to process",
    )
    args = parser.parse_args()

    if not Path(".env").exists():
        print("Save IP to scan in .env file")
        return

    load_dotenv()
    ip = getenv("IP")

    if not ip:
        print("IP isn't properly defined in .env")
        return

    if args.active:
        print(f"Starting active scan of {ip}")
        try:
            save_scan(active_scan(ip), "active_scan.json")
        # TODO: Add except logic for active scan
        except:
            print("Unable to save active scan")

    try:
        save_scan(passive_scan(ip), "passive_scan.json")
    # TODO: Add except logic for passive scan
    except:
        print("Unable to save active scan")


if __name__ == "__main__":
    main()
