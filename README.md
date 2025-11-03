# T3 OSINT

El script actual es capaz de ejecutar análisis tanto activo como pasivo dado la
IP de un servidor web.

## Funcionamiento

El script puede realizar dos tipos de escaneos:

Activo: Utiliza Ping y Nmap para un análisis profundo del sitio interactuando
directamente con él.

Pasivo: Utiliza herramientas como Shodan y whois para recopilar información de
manera pasiva.

## Argumentos

Por seguridad, el  script lee el argumento `--active` que funciona como un
switch de encendido para el análisis activo.

## Variables de Entorno

Para ejecutarse correctamente, el script requiere que exista un archivo
**.env** en el mismo directorio que en donde se ejecute.

Este archivo deberá contener los valores de las la IP y la llave del API de
Shodan en el siguiente formato:

```bash
IP=<La Ip del sitio web>
SHODAN_KEY=<API Key de Shodan>
```
