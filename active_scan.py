"""Generate nmap as JSON.

Module to generate an nmap scan and save findings as a JSON.
"""

import ipaddress
from json import dump
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from nmapthon2 import NmapScanner
from nmapthon2.elements import Host, MissingScript
from ping3 import ping


def active_scan(ip):
    """Write nmap data to a dict.

    Args:
        ip: A valid IP adress.

    Returns:
        dict: Contains gathered host, OS and port information.

    """
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print(f"{ip} isn't a valid ip")
        return None

    scanner = NmapScanner()
    result = scanner.scan(ip, arguments="--privileged -A --osscan-guess")
    host = result[ip]

    if not isinstance(host, Host):
        msg = f"{host} isn't a valid Host"
        raise TypeError(msg)

    os_info = {}
    ports = {}

    host_info = {
        "host": host.ipv4,
        "state": host.state,
        "reason": host.reason,
        "icp_rtt": ping(ip, timeout=2),
        "start_time": f"{host.start_time}",
        "end_time": f"{host.end_time}",
    }

    most_accurate = host.most_accurate_os()

    if most_accurate:
        os_info = {
            "most_accurate_os": most_accurate.name,
            "accuracy": most_accurate.accuracy,
        }

    for port_obj in host:
        port = {
            "protocol": port_obj.protocol,
            "state": port_obj.state,
            "reason": port_obj.reason,
        }

        service_obj = port_obj.service
        if service_obj:
            service = {
                "name": service_obj.name,
                "product": service_obj.product,
                "version": service_obj.version,
                "confidence": service_obj.conf,
            }
            port.update({"service": service})
            try:
                headers = service_obj.get_script("http-server-header")
                service.update({"headers": headers})
            except MissingScript:
                continue
            finally:
                ports.update({port_obj.number: port})

    return {"host_info": host_info, "os_info": os_info, "ports": ports}


if __name__ == "__main__":
    load_dotenv()
    ip = getenv("IP")

    scan = nmap_scan(ip)
    if scan:
        with Path("active_results.json").open("w", encoding="utf-8") as f:
            dump(scan, f, indent=4)
    else:
        print("Unable to procede with active scan")
