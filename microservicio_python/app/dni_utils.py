"""Utilidades para el cálculo y la validación del DNI español."""

LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"
NUMERO_MIN = 0
NUMERO_MAX = 99_999_999

def calcular_letra(numero: int) -> str:
    """Devuelve la letra de control correspondiente al número de DNI.

    Args:
        numero: parte numérica del DNI.

    Returns:
        Letra de control en mayúscula.

    Raises:
        TypeError: si el argumento no es un número entero.
        ValueError: si el número no está en el rango válido.
    """
    # 1. Control de tipo (Evita strings, floats, booleanos, etc.)
    # Nota: isinstance(True, int) es True en Python, por eso excluimos bool explícitamente
    if not isinstance(numero, int) or isinstance(numero, bool):
        raise TypeError("El número de DNI debe ser estrictamente un número entero (int).")

    # 2. Control de rango
    if not (NUMERO_MIN <= numero <= NUMERO_MAX):
        raise ValueError("El número de DNI debe estar entre 00000000 y 99999999.")

    resto = numero % 23
    
    return LETRAS_DNI[resto]

def validar_dni(dni: str) -> bool:
    """Indica si un DNI completo (8 dígitos + letra) es válido.

    No lanza excepciones: cualquier entrada que no sea un DNI bien
    formado y con letra correcta devuelve False.

    Args:
        dni: cadena con el DNI completo (ej. "12345678Z"). La letra
            puede ir en mayúscula o minúscula.

    Returns:
        True si el DNI es válido, False en caso contrario.
    """
    # 1. Tipo y longitud
    if not isinstance(dni, str) or len(dni) != 9:
        return False

    parte_numerica = dni[:-1]
    letra = dni[-1].upper()

    # 2. Solo dígitos ASCII 0-9 (isdigit() solo aceptaría también "²", "٣", etc.)
    if not (parte_numerica.isascii() and parte_numerica.isdigit()):
        return False

    # 3. La letra proporcionada debe coincidir con la calculada
    return letra == calcular_letra(int(parte_numerica))