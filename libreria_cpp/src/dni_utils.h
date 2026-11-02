#ifndef DNI_UTILS_H
#define DNI_UTILS_H

/**
 * @file dni_utils.h
 * @brief API pública de una biblioteca C++ para DNI españoles.
 *
 * Se permiten DNI con ocho dígitos ASCII y letra mayúscula o minúscula.
 * No se contemplan NIE, CIF, espacios ni separadores.
 */

/**
 * @brief Calcula la letra de un número de DNI español.
 * @param numero Número entre 0 y 99999999, ambos incluidos.
 * @return Letra mayúscula correspondiente al módulo 23, o '\0' si el número
 *         es negativo o mayor que 99999999.
 * @note Si se requiere mostrar el DNI completo, añadir ceros a la izquierda
 *       hasta formar exactamente ocho dígitos.
 */
char calcular_letra(int numero);

/**
 * @brief Comprueba que el DNI cumple el formato y que su letra es correcta.
 * @param dni Cadena C terminada en '\0', con ocho dígitos y una letra.
 *            Puede ser nullptr, en cuyo caso devuelve false.
 * @return true si es un DNI válido, false si está mal formado o su letra
 *         no se corresponde con el número.
 * @note Se aceptan letras mayúsculas y minúsculas; no se eliminan espacios.
 */
bool validar_dni(const char* dni);

#endif  // DNI_UTILS_H