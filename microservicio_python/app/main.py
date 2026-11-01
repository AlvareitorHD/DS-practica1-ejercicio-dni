"""Microservicio REST para obtener y validar la letra del DNI español."""

from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

from app.dni_utils import NUMERO_MAX, NUMERO_MIN, calcular_letra, validar_dni

tags_metadata = [
    {
        "name": "DNI",
        "description": "Operaciones de cálculo y validación del DNI español.",
    }
]

app = FastAPI(
    title="API de DNI español",
    description=(
        "Microservicio que calcula la letra de control de un DNI a partir de "
        "su número y valida DNIs completos (8 dígitos + letra)."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Desarrollo local"},
    ],
    contact={
        "name": "Grupo A3 DS",
        "email": "alrulu@correo.ugr.es",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)


# ---------- Modelos de respuesta ----------

class LetraResponse(BaseModel):
    """Resultado del cálculo de la letra de control."""

    numero: int = Field(..., description="Parte numérica del DNI.", examples=[12345678])
    letra: str = Field(
        ...,
        min_length=1,
        max_length=1,
        description="Letra de control calculada (mayúscula).",
        examples=["Z"],
    )


class ValidacionResponse(BaseModel):
    """Resultado de la validación de un DNI completo."""

    dni: str = Field(..., description="DNI recibido, tal cual.", examples=["12345678Z"])
    valido: bool = Field(
        ..., description="True si el formato es correcto y la letra coincide."
    )


# ---------- Endpoints ----------

@app.post(
    "/dni/{numero}",
    response_model=LetraResponse,
    tags=["DNI"],
    summary="Calcula la letra de un DNI",
    operation_id="calcularLetra",
    response_description="Número recibido y letra de control correspondiente.",
    responses={
        422: {"description": "El número no es un entero o está fuera del rango 0-99999999."},
    },
)
async def calcular_letra_endpoint(
    numero: Annotated[
        int,
        Path(
            ge=NUMERO_MIN,
            le=NUMERO_MAX,
            description="Parte numérica del DNI (entre 0 y 99999999).",
            examples=[12345678],
        ),
    ],
) -> LetraResponse:
    """Calcula la letra de control a partir de la parte numérica del DNI.

    La letra se obtiene como la posición `numero % 23` en la tabla
    `TRWAGMYFPDXBNJZSQVHLCKE`.

    Si `numero` no es un entero o está fuera del rango permitido, la
    petición se rechaza con **422 Unprocessable Entity**.
    """
    return LetraResponse(numero=numero, letra=calcular_letra(numero))


@app.get(
    "/dni/validar",
    response_model=ValidacionResponse,
    tags=["DNI"],
    summary="Valida un DNI completo",
    operation_id="validarDni",
    response_description="DNI recibido y resultado de la validación.",
    responses={
        422: {"description": "Falta el parámetro de consulta `dni`."},
    },
)
async def validar_dni_endpoint(
    dni: Annotated[
        str,
        Query(
            description="DNI completo: 8 dígitos y una letra. La letra puede ir "
            "en mayúscula o minúscula.",
            examples=["12345678Z"],
        ),
    ],
) -> ValidacionResponse:
    """Comprueba si un DNI completo es válido.

    Un DNI mal formado (longitud incorrecta, caracteres no numéricos, letra
    que no coincide...) **no es un error de la petición**: se responde
    **200 OK** con `valido: false`. Solo se devuelve **422** si falta el
    parámetro `dni`.
    """
    return ValidacionResponse(dni=dni, valido=validar_dni(dni))