"""Execute host scans."""

from argparse import ArgumentParser
from json import dump
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from t3_osint import active_scan, passive_scan


def save_scan(scan: dict, path: str):
    """Receives a dict and saves it as JSON to a file."""
    if scan:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
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
    shodan_key = getenv("SHODAN_KEY")

    if not ip:
        print("IP isn't properly defined in .env")
        return

    if not shodan_key:
        print("Shodan API key isn't properly defined in .env")
        return

    if args.active:
        print(f"Starting active scan of {ip}")
        try:
            save_scan(active_scan(ip), "out/active_scan.json")
        # TODO: Add except logic for active scan
        except:
            print("Unable to save active scan")

    try:
        save_scan(
            passive_scan(ip=ip, shodan_key=shodan_key),
            "out/passive_scan.json",
        )
    # TODO: Add except logic for passive scan
    except:
        print("Unable to save passive scan")


if __name__ == "__main__":
    main()
