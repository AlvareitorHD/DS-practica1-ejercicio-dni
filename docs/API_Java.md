# API Java: librería DniUtils

Librería de utilidades en Java que calcula la letra de control de un DNI español y valida DNIs completos (8 dígitos + letra). Se distribuye como `dni-utils.jar`.

## Requisitos

- JDK 17 o superior (probado con JDK 21). Se necesita el JDK, no solo el JRE.
- No requiere Maven ni Gradle: basta con `javac`, `jar` y `javadoc`.

## Estructura del componente

```
libreria_java/
├── lib/
│   ├── dni-utils.jar
│   └── src/main/java/com/example/DniUtils.java
├── client/
│   └── Main.java
└── docs/
    └── javadoc/          # documentación generada (abrir index.html)
```

## Compilación y empaquetado

Desde `libreria_java/`:

```bash
mkdir -p build/classes
javac -encoding UTF-8 -d build/classes lib/src/main/java/com/example/DniUtils.java
jar cf lib/dni-utils.jar -C build/classes .
```

## API

Clase `com.example.DniUtils`: clase final de utilidades, con solo métodos estáticos y sin instanciación.

| Miembro | Descripción |
|---|---|
| `public static char calcularLetra(int numero)` | Devuelve la letra de control de un número entre 0 y 99999999. Lanza `IllegalArgumentException` si está fuera de rango |
| `public static boolean validarDni(String dni)` | Devuelve `true` si el DNI completo es válido. Nunca lanza excepciones |
| `public static final int NUMERO_MIN` | Valor mínimo (0) |
| `public static final int NUMERO_MAX` | Valor máximo (99999999) |

### Comportamiento de `validarDni`

Devuelve `false` para: `null`, longitud distinta de 9, caracteres no numéricos en los 8 primeros, signos (`+`, `-`), dígitos no ASCII y letra que no coincide. La letra puede ir en mayúscula o minúscula.

### Cálculo de la letra

La letra es la posición `numero % 23` en la tabla `TRWAGMYFPDXBNJZSQVHLCKE`.

## Uso desde código Java

Con el jar en el classpath:

```java
import com.example.DniUtils;

char letra = DniUtils.calcularLetra(12345678);   // 'Z'
boolean ok = DniUtils.validarDni("12345678Z");   // true

try {
    DniUtils.calcularLetra(100_000_000);
} catch (IllegalArgumentException e) {
    System.out.println(e.getMessage());          // número fuera de rango
}
```

## Cliente de ejemplo (`client/Main.java`)

El cliente consume la librería a través del jar (no del código fuente) y ofrece cuatro modos de uso.

### Compilación

Desde `libreria_java/`:

```bash
mkdir -p build/client
javac -encoding UTF-8 -cp lib/dni-utils.jar -d build/client client/Main.java
```

### Ejecución

El separador del classpath es `;` en Windows y `:` en Linux/macOS/WSL. Ejemplos para Windows:

| Modo | Comando |
|---|---|
| Batería de pruebas (sin argumentos) | `java -cp "build/client;lib/dni-utils.jar" Main` |
| Calcular la letra | `java -cp "build/client;lib/dni-utils.jar" Main letra 12345678` |
| Validar un DNI | `java -cp "build/client;lib/dni-utils.jar" Main validar 12345678Z` |
| Menú interactivo | `java -cp "build/client;lib/dni-utils.jar" Main interactivo` |

En Linux/macOS/WSL, sustituye `;` por `:` y las comillas son opcionales.

- **Batería de pruebas**: cada caso se muestra como `[OK]` o `[FALLO]`, e incluye casos límite (0, 99999999), minúsculas, longitudes incorrectas, signos, dígitos no ASCII, cadena vacía y `null`. El programa termina con código 1 si alguno falla.
- **`letra` y `validar`**: resultado por consola. Si el número no es un entero o está fuera de rango, se muestra un mensaje de error por `stderr` y el código de salida es 1.
- **`interactivo`**: menú por consola con opciones para calcular la letra, validar un DNI o salir.

Si en la consola de Windows se ven mal las tildes, ejecutar antes `chcp 65001`.

## Documentación Javadoc

Desde `libreria_java/`:

```bash
javadoc -encoding UTF-8 -charset UTF-8 -docencoding UTF-8 -d docs/javadoc -windowtitle "DniUtils API" lib/src/main/java/com/example/DniUtils.java
```

Abrir `docs/javadoc/index.html` en el navegador. Hay que regenerarla si se modifica `DniUtils.java`.

## Coherencia con los otros componentes

Mismo contrato que el microservicio Python y la librería C++: rango 0 a 99999999, misma tabla de letras, y validación que devuelve `false` ante cualquier entrada mal formada. Las diferencias son de lenguaje: en Java `calcularLetra` lanza `IllegalArgumentException` (en Python, `ValueError`).