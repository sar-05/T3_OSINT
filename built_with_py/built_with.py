"""Utility functions and classes for calculating speed."""  # noqa: INP001
import json

import builtwith


def consulta_builtwith(url, archivo_salida=r"built_with_py\builtwith.json"):
    """Dadad."""
    info = builtwith.parse(url)

    with open(archivo_salida, "w", encoding="utf-8") as f:  # noqa: PTH123
        json.dump(info, f, ensure_ascii=False, indent=4)

    return info

if __name__ == "__main__":
    url = "http://146.190.113.171"
    resultado = consulta_builtwith(url)
    print("Tecnologías detectadas guardadas en JSON")

