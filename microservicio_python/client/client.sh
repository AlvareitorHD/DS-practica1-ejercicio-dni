#!/usr/bin/env bash
# Cliente curl para el microservicio REST de DNI.
#
# Uso:
#   ./client.sh letra 12345678
#   ./client.sh validar 12345678Z
# La URL base se puede cambiar con: DNI_API_URL=http://host:8000 ./client.sh ...

BASE_URL="${DNI_API_URL:-http://127.0.0.1:8000}"

uso() {
    echo "Uso: $0 letra <numero> | validar <dni_completo>" >&2
    exit 1
}

[ $# -eq 2 ] || uso

case "$1" in
    letra)
        curl -s --max-time 5 -w "\nHTTP %{http_code}\n" \
            -X POST "$BASE_URL/dni/$2"
        ;;
    validar)
        curl -s --max-time 5 -w "\nHTTP %{http_code}\n" \
            -G "$BASE_URL/dni/validar" --data-urlencode "dni=$2"
        ;;
    *)
        uso
        ;;
esac