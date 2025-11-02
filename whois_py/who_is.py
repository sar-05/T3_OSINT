"""Utility functions and classes for calculating speed."""
import json

from ipwhois import IPWhois  # pyright: ignore[reportMissingImports]


def consulta_whois(dominio, salida=r"whois_py\whois.json"):
    """Consult functions and classes for calculating speed."""
    objetivo = IPWhois(dominio)
    resultado = objetivo.lookup_rdap()

    datos_ipwhois = {
        "asn_registry": resultado["asn_registry"],
        "asn": resultado["asn"],
        "asn_cidr": resultado["asn_cidr"],
        "asn_country_code": resultado["asn_country_code"],
        "asn_description": resultado["asn_description"],
        "query": resultado["query"],
        "start_address": resultado["network"]["start_address"],
        "end_address": resultado["network"]["end_address"],
        "cidr": resultado["network"]["cidr"],
        "ip_version": resultado["network"]["ip_version"],
    }

    with open(salida, "w", encoding="utf-8") as f:  # noqa: PTH123
        json.dump(datos_ipwhois, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    dominio = "146.190.113.171"
    resultado = consulta_whois(dominio)
    print("Información IPWHOIS guardada en JSON")
