"""Cliente de línea de comandos para el microservicio REST de DNI.

Uso:
    python client.py letra 12345678
    python client.py validar 12345678Z
    python client.py --url http://otro-host:8000 letra 12345678

La URL base también puede fijarse con la variable de entorno DNI_API_URL.
"""

import argparse
import os
import sys

import requests

DEFAULT_URL = "http://127.0.0.1:8000"
TIMEOUT = 5  # segundos


class ApiError(Exception):
    """Error al consumir la API (red o respuesta no exitosa)."""


def _request(method: str, url: str, **kwargs) -> dict:
    """Realiza la petición y devuelve el JSON, o lanza ApiError."""
    try:
        response = requests.request(method, url, timeout=TIMEOUT, **kwargs)
    except requests.exceptions.ConnectionError:
        raise ApiError(f"No se pudo conectar con el servidor en {url}.")
    except requests.exceptions.Timeout:
        raise ApiError("El servidor no respondió a tiempo.")

    if response.status_code == 422:
        raise ApiError("Petición rechazada (422): parámetro ausente o fuera de rango.")
    if not response.ok:
        raise ApiError(f"Error HTTP {response.status_code}.")
    return response.json()


def calcular_letra(base_url: str, numero: int) -> str:
    """POST /dni/{numero} -> letra de control."""
    return _request("POST", f"{base_url}/dni/{numero}")["letra"]


def validar_dni(base_url: str, dni: str) -> bool:
    """GET /dni/validar?dni=... -> True si es válido."""
    return _request("GET", f"{base_url}/dni/validar", params={"dni": dni})["valido"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Cliente de la API de DNI español.")
    parser.add_argument(
        "--url",
        default=os.environ.get("DNI_API_URL", DEFAULT_URL),
        help=f"URL base del servicio (por defecto {DEFAULT_URL}).",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p_letra = sub.add_parser("letra", help="Calcula la letra de un número de DNI.")
    p_letra.add_argument("numero", type=int, help="Parte numérica (0-99999999).")

    p_val = sub.add_parser("validar", help="Valida un DNI completo.")
    p_val.add_argument("dni", help="DNI completo, ej. 12345678Z.")

    args = parser.parse_args()
    base_url = args.url.rstrip("/")

    try:
        if args.comando == "letra":
            letra = calcular_letra(base_url, args.numero)
            print(f"La letra del DNI {args.numero} es {letra}")
        else:
            valido = validar_dni(base_url, args.dni)
            print(f"El DNI {args.dni} es {'válido' if valido else 'inválido'}")
    except ApiError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())