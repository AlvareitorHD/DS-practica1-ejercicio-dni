package com.example;

/**
 * Utilidades para el cálculo y la validación del DNI español.
 *
 * <p>El DNI consta de 8 dígitos y una letra de control. La letra se obtiene
 * como la posición {@code numero % 23} en la tabla
 * {@code TRWAGMYFPDXBNJZSQVHLCKE}.</p>
 *
 * <p>Clase de utilidades: solo contiene métodos estáticos y no se puede
 * instanciar.</p>
 */
public final class DniUtils {

    /** Tabla de letras de control, indexada por {@code numero % LETRAS.length()}. */
    private static final String LETRAS = "TRWAGMYFPDXBNJZSQVHLCKE";

    /** Número de dígitos de la parte numérica de un DNI. */
    private static final int NUM_DIGITOS = 8;

    /** Longitud total de un DNI completo (dígitos + letra). */
    private static final int LONGITUD_DNI = NUM_DIGITOS + 1;

    /** Valor mínimo de la parte numérica de un DNI. */
    public static final int NUMERO_MIN = 0;

    /** Valor máximo de la parte numérica de un DNI (8 dígitos). */
    public static final int NUMERO_MAX = 99_999_999;

    /** Constructor privado: esta clase no debe instanciarse. */
    private DniUtils() {
        throw new AssertionError("DniUtils no se puede instanciar");
    }

    /**
     * Calcula la letra de control correspondiente a un número de DNI.
     *
     * @param numero parte numérica del DNI (entre {@value #NUMERO_MIN} y
     *               {@value #NUMERO_MAX})
     * @return la letra de control, en mayúscula
     * @throws IllegalArgumentException si {@code numero} está fuera de rango
     */
    public static char calcularLetra(int numero) {
        if (numero < NUMERO_MIN || numero > NUMERO_MAX) {
            throw new IllegalArgumentException(
                    "Número de DNI fuera de rango (" + NUMERO_MIN + "-" + NUMERO_MAX + "): " + numero);
        }
        return LETRAS.charAt(numero % LETRAS.length());
    }

    /**
     * Indica si un DNI completo (8 dígitos + letra) es válido.
     *
     * <p>Nunca lanza excepciones: cualquier entrada mal formada (nula,
     * longitud incorrecta, caracteres no numéricos, signos, dígitos no
     * ASCII o letra que no coincide) devuelve {@code false}. La letra puede
     * ir en mayúscula o minúscula.</p>
     *
     * @param dni cadena con el DNI completo, por ejemplo {@code "12345678Z"}
     * @return {@code true} si el DNI es válido; {@code false} en caso contrario
     */
    public static boolean validarDni(String dni) {
        if (dni == null || dni.length() != LONGITUD_DNI) {
            return false;
        }

        // Solo dígitos ASCII 0-9 (Integer.parseInt también aceptaría signos
        // y dígitos Unicode, por eso se comprueba carácter a carácter).
        for (int i = 0; i < NUM_DIGITOS; i++) {
            char c = dni.charAt(i);
            if (c < '0' || c > '9') {
                return false;
            }
        }

        // Los 8 primeros caracteres son dígitos: la conversión no puede fallar
        // y el resultado siempre está dentro del rango válido.
        int numero = Integer.parseInt(dni.substring(0, NUM_DIGITOS));
        char letra = Character.toUpperCase(dni.charAt(NUM_DIGITOS));

        return letra == calcularLetra(numero);
    }
}