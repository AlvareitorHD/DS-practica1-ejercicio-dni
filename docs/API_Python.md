# API Python: microservicio REST de DNI

Microservicio REST construido con **FastAPI** que calcula la letra de control de un DNI español y valida DNIs completos (8 dígitos + letra).

## Requisitos

- Python 3.10 o superior
- Dependencias de `microservicio_python/requirements.txt` (FastAPI, uvicorn, requests, pyyaml)

## Instalación

Desde la carpeta `microservicio_python/`:

```bash
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Linux / macOS / Git Bash:  source .venv/bin/activate   (en Git Bash: source .venv/Scripts/activate)
pip install -r requirements.txt
```

## Ejecución

Desde `microservicio_python/` (la carpeta que contiene `app/`):

```bash
uvicorn app.main:app --reload
```

El servicio queda disponible en `http://127.0.0.1:8000`.

| Recurso | URL |
|---|---|
| Documentación interactiva (Swagger UI) | `http://127.0.0.1:8000/docs` |
| Documentación alternativa (ReDoc) | `http://127.0.0.1:8000/redoc` |
| Contrato OpenAPI (JSON) | `http://127.0.0.1:8000/openapi.json` |
| Contrato OpenAPI (YAML, en el repositorio) | `microservicio_python/docs/openapi.yaml` |

## Endpoints

### `POST /dni/{numero}`: calcula la letra

Calcula la letra de control a partir de la parte numérica del DNI.

| Parámetro | Ubicación | Tipo | Descripción |
|---|---|---|---|
| `numero` | ruta | entero | Número entre 0 y 99999999 |

**Respuesta 200**

```json
{ "numero": 12345678, "letra": "Z" }
```

**Respuesta 422**: `numero` no es un entero o está fuera del rango 0-99999999.

### `GET /dni/validar`: valida un DNI completo

| Parámetro | Ubicación | Tipo | Descripción |
|---|---|---|---|
| `dni` | consulta (query) | cadena | DNI completo, p. ej. `12345678Z`. La letra puede ir en mayúscula o minúscula |

**Respuesta 200**

```json
{ "dni": "12345678Z", "valido": true }
```

Un DNI mal formado (longitud incorrecta, caracteres no numéricos o letra que no coincide) **no es un error**: se responde 200 con `"valido": false`.

**Respuesta 422**: falta el parámetro `dni`.

## Cómo consumir el servicio

El servidor debe estar arrancado en otra terminal.

### Con curl

```bash
curl -X POST http://127.0.0.1:8000/dni/12345678
curl -G http://127.0.0.1:8000/dni/validar --data-urlencode "dni=12345678Z"
```

En PowerShell usa `curl.exe` en lugar de `curl`.

### Con el script `client/client.sh`

```bash
./client/client.sh letra 12345678
./client/client.sh validar 12345678Z
```

Requiere `chmod +x client/client.sh` y una terminal Bash (Git Bash o WSL con el servidor accesible). La URL base se cambia con la variable `DNI_API_URL`.

### Con el cliente Python `client/client.py`

```bash
python client/client.py letra 12345678
python client/client.py validar 12345678Z
python client/client.py --url http://otro-host:8000 letra 12345678
```

### Desde código Python (con `requests`)

```python
import requests

BASE = "http://127.0.0.1:8000"

letra = requests.post(f"{BASE}/dni/12345678", timeout=5).json()["letra"]
valido = requests.get(f"{BASE}/dni/validar", params={"dni": "12345678Z"}, timeout=5).json()["valido"]
```

## Reutilización de la lógica sin HTTP

La lógica está separada de la capa web en `app/dni_utils.py`, de modo que puede reutilizarse sin levantar el servidor:

```python
from app.dni_utils import calcular_letra, validar_dni

calcular_letra(12345678)    # "Z"
validar_dni("12345678Z")    # True
```

| Función | Comportamiento |
|---|---|
| `calcular_letra(numero)` | Devuelve la letra. Lanza `TypeError` si no es un `int` (se excluye `bool`) y `ValueError` si está fuera de 0-99999999 |
| `validar_dni(dni)` | Devuelve `True`/`False`. Nunca lanza excepciones |

## Cálculo de la letra

La letra es la posición `numero % 23` en la tabla `TRWAGMYFPDXBNJZSQVHLCKE`.

## Estructura del componente

```
microservicio_python/
├── app/
│   ├── __init__.py
│   ├── main.py          # endpoints FastAPI y modelos de respuesta
│   └── dni_utils.py     # lógica del DNI
├── docs/
│   └── openapi.yaml     # contrato de la API
├── client/
│   ├── client.py
│   └── client.sh
└── requirements.txt
```

## Regenerar el contrato OpenAPI

Si se modifica `main.py`, hay que regenerar `docs/openapi.yaml` y volver a validarlo (por ejemplo, con `openapi-spec-validator`).