"""Consultas a ipwhois."""

from ipwhois import IPWhois


def consulta_whois(dominio):
    """Retorna propiedades de el servidor que aloja al sitio."""
    objetivo = IPWhois(dominio)
    resultado = objetivo.lookup_rdap()

    return {
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


if __name__ == "__main__":
    dominio = "146.190.113.171"
    resultado = consulta_whois(dominio)
    print(resultado)
