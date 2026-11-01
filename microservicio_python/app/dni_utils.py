"""Utilidades para el cálculo y la validación del DNI español."""

LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"

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
    if not (0 <= numero <= 99999999):
        raise ValueError("El número de DNI debe estar entre 00000000 y 99999999.")

    resto = numero % 23
    
    return LETRAS_DNI[resto]

def validar_dni(dni: str) -> bool:
    """Indica si un DNI completo (8 dígitos + letra) es válido.
    
    Args:
        dni: cadena de texto con el DNI completo (ej. "12345678Z").
    Returns:
        True si el DNI es válido, False en caso contrario.
    Raises:
        TypeError: si el argumento no es una cadena de texto.
        ValueError: si el formato, la longitud o los caracteres no son válidos.
    """
    # 1. Control de tipo
    if not isinstance(dni, str):
        raise TypeError("El DNI debe ser una cadena de texto (str).")
    
    # 2. Control de longitud
    if len(dni) != 9:
        raise ValueError("La longitud del DNI es incorrecta. Debe tener exactamente 9 caracteres.")
    
    # Separar los números y la letra (asegurando mayúscula)
    parte_numerica = dni[:-1]
    letra_proporcionada = dni[-1].upper()
    
    # 3. Control de caracteres válidos en la letra
    if letra_proporcionada not in LETRAS_DNI:
        raise ValueError("El último carácter no corresponde a una letra de control de DNI válida.")
        
    # 4. Control de formato numérico
    if not parte_numerica.isdigit():
        raise ValueError("Los primeros 8 caracteres deben ser dígitos numéricos.")
        
    # 5. Validación del DNI
    numero = int(parte_numerica)
    letra_correcta = calcular_letra(numero)
    
    return letra_proporcionada == letra_correcta