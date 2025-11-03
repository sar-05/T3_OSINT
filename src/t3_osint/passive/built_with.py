"""Utility functions and classes for calculating speed."""

import builtwith


def consulta_builtwith(url):
    """Devuelve las tecnlogías que usa el sitio web."""
    return builtwith.parse(url)


if __name__ == "__main__":
    url = "http://146.190.113.171"
    resultado = consulta_builtwith(url)
    print(resultado)
