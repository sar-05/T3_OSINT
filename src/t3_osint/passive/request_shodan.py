"""Consulta a Shodan."""

import shodan


def consulta_shodan(api_key, ip):
    """Retorna los resultados obtenidos de consultar el API de Shodan."""

    api = shodan.Shodan(api_key)
    resultados = api.search(f"ip:{ip}")
    total = resultados.get("total", 0)
    results_list = []
    for match in resultados.get("matches", []):
        result = {
            "ip": match.get("ip_str"),
            "organization": match.get("org", "Desconocida"),
            "banner": match.get("data", "").strip(),
            "location": {
                "city": match.get("location", {}).get("city", "Desconocida"),
                "country": match.get("location", {}).get(
                    "country_name",
                    "Desconocido",
                ),
                "latitude": match.get("location", {}).get("latitude", "N/A"),
                "longitude": match.get("location", {}).get("longitude", "N/A"),
            },
            "port": match.get("port", "N/A"),
            "transport": "ssl"
            if match.get("port") == 465
            else "starttls"
            if match.get("port") == 587
            else "none",
            "timestamp": match.get("timestamp", "N/A"),
            "asn": match.get("asn", "N/A"),
            "hostnames": match.get("hostnames", []),
            "domains": match.get("domains", []),
            "os": match.get("os", "Desconocido"),
            "data": match.get("data", "").strip(),
            "vulns": match.get("vulns", []),
        }
        results_list.append(result)
        return {
            "IP": result["ip"],
            "Puerto": result["port"],
            "Pais": result["location"]["country"],
            "Vulnerabilidades": len(result["vulns"]),
        }


if __name__ == "__main__":
    api_key = input("Ingrese la API key: ")
    ip = input("Ingrese la IP a consultar: ")
    print(f"\n Ejecutando búsqueda: {ip}\n")
    print(consulta_shodan(api_key, ip))
