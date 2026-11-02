# API C++: biblioteca dni_utils

Biblioteca reutilizable en C++17 que calcula la letra de control de un DNI español y valida DNIs completos (8 dígitos + letra). Se construye como biblioteca estática mediante CMake y puede enlazarse con otros programas C++.

## Requisitos

- Compilador compatible con C++17 (por ejemplo, MSVC, g++ o Clang).
- CMake 3.16 o superior.
- Doxygen para regenerar la documentación HTML (no es necesario para compilar ni ejecutar la biblioteca).
- No requiere bibliotecas externas: utiliza únicamente la biblioteca estándar de C++.

## Estructura del componente

```
libreria_cpp/
├── src/
│   ├── dni_utils.h            # Interfaz pública documentada
│   └── dni_utils.cpp          # Implementación de la biblioteca
├── client/
│   └── prueba.cpp             # Cliente y batería de pruebas
├── docs/
│   ├── Doxyfile               # Configuración de Doxygen
│   └── generada/              # Documentación HTML generada
└── CMakeLists.txt             # Construcción y pruebas con CMake
```

La cabecera `dni_utils.h` declara la API que pueden utilizar otros programas. Su implementación está en `dni_utils.cpp`; el cliente `prueba.cpp` utiliza las funciones públicas sin duplicar el algoritmo.

## Compilación y enlace

Desde `libreria_cpp/`:

```bash
cmake -S . -B build
cmake --build build --config Release
```

La compilación genera una biblioteca estática dni_utils y un ejecutable prueba que utiliza dicha biblioteca.

## API

Las funciones públicas se declaran en `src/dni_utils.h` y **no requieren crear objetos**.

| Función | Entrada | Resultado | Error |
|---|---|---|---|
| `char calcular_letra(int numero)` | Entero entre 0 y 99999999 | Letra de control en mayúscula | Devuelve `'\0'` si el número está fuera de rango |
| `bool validar_dni(const char* dni)` | Cadena C terminada en `'\0'`, con ocho dígitos ASCII y una letra mayúscula | `true` si el DNI es válido | Devuelve `false` si está mal formado, la letra no coincide o el puntero es `nullptr` |

### Comportamiento de `calcular_letra`

- Admite valores desde `0` hasta `99999999`, ambos incluidos.
- Devuelve la letra correspondiente en mayúscula, por ejemplo `calcular_letra(12345678)` devuelve `'Z'`.
- Si recibe `-1` o `100000000`, devuelve el **carácter nulo** `'\0'` como indicador de error; no lanza una excepción.
- El número se recibe como `int`: si se necesita mostrar el DNI completo, los ceros a la izquierda deben añadirse al presentarlo como texto.

### Comportamiento de `validar_dni`

Devuelve `false` si recibe:

- `nullptr` o una cadena cuya longitud no sea exactamente 9.
- Caracteres diferentes de los dígitos ASCII `0`–`9` en las primeras ocho posiciones.
- Una letra incorrecta, una letra minúscula, espacios, signos o separadores.

La entrada debe ser una **cadena C válida terminada en `\0`**; `nullptr` está contemplado, pero la función no está diseñada para recibir punteros no válidos. No se admiten NIE ni CIF.

### Cálculo de la letra

La letra se obtiene usando el índice `numero % 23` sobre la cadena `TRWAGMYFPDXBNJZSQVHLCKE`.

## Uso desde código C++

Incluyendo la cabecera pública y enlazando la biblioteca:

```cpp
#include "dni_utils.h"
#include <iostream>

int main() {
    char letra = calcular_letra(12345678);  // 'Z'
    bool valido = validar_dni("12345678Z"); // true

    if (letra == '\0') {
        std::cerr << "Número fuera de rango\n";
        return 1;
    }

    std::cout << "Letra: " << letra << '\n';
    std::cout << std::boolalpha << "DNI válido: " << valido << '\n';
    return 0;
}
```

`std::boolalpha` muestra los booleanos como `true` y `false` en lugar de `1` y `0`.

## Cliente de ejemplo (`client/prueba.cpp`)

El cliente llama a las dos funciones públicas, muestra ejemplos y ejecuta una batería de 14 comprobaciones: resultados conocidos, límites numéricos, números fuera de rango, formato, mayúsculas, rechazo de minúsculas, espacios, caracteres incorrectos y `nullptr`.

### Compilación y ejecución

Desde `libreria_cpp/`, una vez compilado el proyecto:

Windows en Visual Studio:

```powershell
.\build\Release\prueba.exe
```

Linux/macOS o generadores de configuración única:

```bash
./build/prueba
```

La ruta exacta depende del generador elegido por CMake.

Salida esperada:

```text
Letra de 12345678: Z
Validar 12345678Z: true
Validar 12345678A: false
Todas las pruebas han pasado.
```

El programa termina con código 0 si todas las comprobaciones son correctas y con código 1 si alguna falla.

### Pruebas automáticas con CTest

`CMakeLists.txt` registra el cliente como prueba `dni_pruebas`. Para ejecutarla:

```bash
ctest --test-dir build -C Release --output-on-failure
```

El resultado esperado es `100% tests passed`. CTest verifica que el ejecutable termine con código de salida 0; las comprobaciones concretas se realizan dentro de `prueba.cpp`.

## Documentación Doxygen

La cabecera `src/dni_utils.h` incluye comentarios con `@brief`, `@param`, `@return` y `@note`, que documentan las funciones públicas.

Desde `libreria_cpp/`, con Doxygen instalado:

```bash
doxygen docs/Doxyfile
```

La configuración genera documentación HTML en `docs/generada/html/`. Para consultarla, abrir:

```text
docs/generada/html/index.html
```

Si se modifica la interfaz pública o sus comentarios, debe regenerarse la documentación antes de entregar.

## Coherencia con los otros componentes

Los tres componentes utilizan el mismo algoritmo de cálculo (`numero % 23` y la misma tabla de letras) y el rango numérico `0`–`99999999`. Sin embargo, hay diferencias de contrato que deben conocerse:

- C++: `calcular_letra` devuelve `'\0'` ante un número fuera de rango; `validar_dni` acepta letras mayúsculas y minúsculas.
- Java: `calcularLetra` lanza `IllegalArgumentException` fuera de rango; `validarDni` admite mayúsculas y minúsculas.
- Python: la función `calcular_letra` lanza `TypeError` o `ValueError`, según el error; la validación admite mayúsculas y minúsculas. El microservicio REST expone sus operaciones mediante HTTP y JSON.
