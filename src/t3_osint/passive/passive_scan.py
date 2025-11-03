"""Función de escaneo pasivo."""

from t3_osint import consulta_builtwith, consulta_shodan, consulta_whois


def passive_scan(ip, shodan_key) -> dict:
    """Retorna un diccionario con los escaneos pasivos individuales."""
    return {
        "passive": {
            "builtwith": consulta_builtwith(ip),
            "consulta_shodan": consulta_shodan(ip=ip, api_key=shodan_key),
            "consulta_whois": consulta_whois(ip),
        },
    }


if __name__ == "__main__":
    ip = input("Ingrese la IP: ")
    shodan_api = input("Ingrese el API de Shodan: ")
    print(passive_scan(ip, shodan_api))
