import os
import stat
import base64
import getpass
import shodan
import json

def obtener_api_key():
    ruta = os.path.expanduser("~/.shodan_key")
    if os.path.exists(ruta):
        with open(ruta, "rb") as f:
            encoded = f.read().strip()
        return base64.b64decode(encoded).decode("utf-8")
    else:
        key = getpass.getpass("🔐 Ingresa tu Shodan API Key: ")
        encoded = base64.b64encode(key.encode("utf-8"))
        with open(ruta, "wb") as f:
            f.write(encoded)
        try:
            os.chmod(ruta, stat.S_IREAD | stat.S_IWRITE)
        except Exception:
            pass
        print(f"✅ Clave guardada en: {ruta}")
        return key

def consultar_shodan(api, consulta):
    try:
        resultados = api.search(consulta)
        total = resultados.get("total", 0)
        print(f"🔹 Resultados encontrados: {total}\n")

        results_list = []
        
        for match in resultados.get("matches", []):
            result = {
            "ip": match.get("ip_str"),
            "organization": match.get("org", "Desconocida"),
            "banner": match.get("data", "").strip(),
            "location": {
                "city": match.get("location", {}).get("city", "Desconocida"),
                "country": match.get("location", {}).get("country_name", "Desconocido"),
                "latitude": match.get("location", {}).get("latitude", "N/A"),
                "longitude": match.get("location", {}).get("longitude", "N/A"),
            },
            "port": match.get("port", "N/A"),
            "transport": "ssl" if match.get("port") == 465 else "starttls" if match.get("port") == 587 else "none",
            "timestamp": match.get("timestamp", "N/A"),
            "asn": match.get("asn", "N/A"),
            "hostnames": match.get("hostnames", []),
            "domains": match.get("domains", []),
            "os": match.get("os", "Desconocido"),
            "data": match.get("data", "").strip(),
            "vulns": match.get("vulns", []),
            }
            results_list.append(result)
            print(f" - IP: {result['ip']}, Puerto: {result['port']}, País: {result['location']['country']}, Vulnerabilidades: {len(result['vulns'])}")

        with open("shodan_results.json", "w", encoding="utf-8") as f:
            json.dump(results_list, f, indent=2, ensure_ascii=False)

        print("\n✅ Resultados guardados en shodan_results.json")

    except shodan.APIError as e:
        print(f"❌ Error en la consulta a Shodan: {e}")

def main():
    API_KEY = obtener_api_key()
    api = shodan.Shodan(API_KEY)
    consulta = "ip:146.190.113.171"
    print(f"\n🔍 Ejecutando búsqueda: {consulta}\n")
    consultar_shodan(api, consulta)

if __name__ == "__main__":
    main()
