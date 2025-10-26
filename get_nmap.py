from os import getenv
from json import dump
from dotenv import load_dotenv
from nmapthon2 import NmapScanner
from nmapthon2.elements import Host, MissingScript
from nmapthon2.utils import valid_ip


def nmap_scan(ip):

    if not valid_ip(ip):
        raise TypeError(f"{ip} isn't a valid ip")

    scanner = NmapScanner()
    result = scanner.scan(ip, arguments='--privileged -A --osscan-guess')
    host = result[ip]

    if not isinstance(host, Host):
        raise TypeError(f"{host} isn't a valid Host")

    nmap_scan = {}
    os_info = {}
    ports = {}

    host_info = {
            'host': host.ipv4,
            'state': host.state,
            'reason': host.reason,
            'start_time': f"{host.start_time}",
            'end_time': f"{host.end_time}"
            }

    most_accurate = host.most_accurate_os()

    if most_accurate:
        os_info = {
                'most_accurate_os': most_accurate.name,
                'accuracy': most_accurate.accuracy
                }

    for port_obj in host:
        port = {
                'protocol': port_obj.protocol,
                'state': port_obj.state,
                'reason': port_obj.reason
                }

        service_obj = port_obj.service
        if service_obj:
            service = {
                'name': service_obj.name,
                'product': service_obj.product,
                'version': service_obj.version,
                'confidence': service_obj.conf,
            }
            port.update({'service': service})
            try:
                headers = service_obj.get_script('http-server-header')
                service.update({'headers': headers})
            except MissingScript:
                continue
            finally:
                ports.update({port_obj.number: port})

    nmap_scan = {
            'host_info': host_info,
            'os_info': os_info,
            'ports': ports
            }

    return nmap_scan


if __name__ == '__main__':

    load_dotenv()
    ip = getenv('IP')

    with open('active_results.json', 'w', encoding='utf-8') as f:
        dump(nmap_scan(ip), f, indent=4)
