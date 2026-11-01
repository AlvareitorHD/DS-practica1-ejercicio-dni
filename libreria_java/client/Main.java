package client;
import com.example.DniUtils;

import java.util.Scanner;

/**
 * Cliente de la librería {@link DniUtils}.
 *
 * <p>Modos de uso:</p>
 * <ul>
 *   <li>Sin argumentos: ejecuta una batería de pruebas con resultado esperado.</li>
 *   <li>{@code letra <numero>}: calcula la letra de un número.</li>
 *   <li>{@code validar <dni>}: valida un DNI completo.</li>
 *   <li>{@code interactivo}: modo de entrada/salida por consola.</li>
 * </ul>
 */
public class Main {

    private static int fallos = 0;

    public static void main(String[] args) {
        if (args.length == 0) {
            ejecutarPruebas();
            return;
        }

        switch (args[0]) {
            case "letra":
                if (args.length != 2) {
                    uso();
                }
                System.exit(comandoLetra(args[1]));
                break;
            case "validar":
                if (args.length != 2) {
                    uso();
                }
                comandoValidar(args[1]);
                break;
            case "interactivo":
                modoInteractivo();
                break;
            default:
                uso();
        }
    }

    // ---------- Uso ----------

    private static void uso() {
        System.err.println("Uso:");
        System.err.println("  java Main                    (batería de pruebas)");
        System.err.println("  java Main letra <numero>");
        System.err.println("  java Main validar <dni>");
        System.err.println("  java Main interactivo");
        System.exit(1);
    }

    // ---------- Comandos individuales ----------

    /** Devuelve 0 si todo va bien y 1 si la entrada no es válida. */
    private static int comandoLetra(String texto) {
        try {
            int numero = Integer.parseInt(texto.trim());
            char letra = DniUtils.calcularLetra(numero);
            System.out.println("La letra del DNI " + numero + " es " + letra);
            return 0;
        } catch (NumberFormatException e) {
            System.err.println("Error: \"" + texto + "\" no es un número entero.");
        } catch (IllegalArgumentException e) {
            System.err.println("Error: " + e.getMessage());
        }
        return 1;
    }

    private static void comandoValidar(String dni) {
        boolean valido = DniUtils.validarDni(dni);
        System.out.println("El DNI " + dni + " es " + (valido ? "válido" : "inválido"));
    }

    // ---------- Modo interactivo ----------

    private static void modoInteractivo() {
        try (Scanner sc = new Scanner(System.in)) {
            while (true) {
                System.out.println();
                System.out.println("1) Calcular letra");
                System.out.println("2) Validar DNI");
                System.out.println("0) Salir");
                System.out.print("Opción: ");
                if (!sc.hasNextLine()) {
                    return;
                }
                String opcion = sc.nextLine().trim();

                switch (opcion) {
                    case "1":
                        System.out.print("Número (0-99999999): ");
                        if (!sc.hasNextLine()) {
                            return;
                        }
                        comandoLetra(sc.nextLine());
                        break;
                    case "2":
                        System.out.print("DNI completo: ");
                        if (!sc.hasNextLine()) {
                            return;
                        }
                        comandoValidar(sc.nextLine().trim());
                        break;
                    case "0":
                        return;
                    default:
                        System.out.println("Opción no válida.");
                }
            }
        }
    }

    // ---------- Batería de pruebas ----------

    private static void ejecutarPruebas() {
        System.out.println("=== calcularLetra ===");
        probarLetra(12345678, 'Z');
        probarLetra(0, 'T');
        probarLetra(1234567, 'L');
        probarLetra(99_999_999, 'R');
        probarLetraFueraDeRango(-1);
        probarLetraFueraDeRango(100_000_000);

        System.out.println();
        System.out.println("=== validarDni ===");
        probarValidar("12345678Z", true);
        probarValidar("12345678z", true);   // minúscula
        probarValidar("00000000T", true);   // ceros a la izquierda
        probarValidar("99999999R", true);   // límite superior
        probarValidar("12345678A", false);  // letra incorrecta
        probarValidar("1234567Z", false);   // 8 caracteres
        probarValidar("12345678", false);   // sin letra
        probarValidar("123456789Z", false); // demasiado largo
        probarValidar("1234567AZ", false);  // letra en medio
        probarValidar("+1234567L", false);  // signo
        probarValidar("-1234567L", false);  // signo negativo
        probarValidar("\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668Z", false); // dígitos árabes
        probarValidar("", false);
        probarValidar(null, false);

        System.out.println();
        if (fallos == 0) {
            System.out.println("Todas las pruebas han pasado.");
        } else {
            System.out.println("Pruebas fallidas: " + fallos);
            System.exit(1);
        }
    }

    private static void probarLetra(int numero, char esperada) {
        char obtenida = DniUtils.calcularLetra(numero);
        informar("calcularLetra(" + numero + ") = " + obtenida, obtenida == esperada);
    }

    private static void probarLetraFueraDeRango(int numero) {
        try {
            DniUtils.calcularLetra(numero);
            informar("calcularLetra(" + numero + ") debería lanzar excepción", false);
        } catch (IllegalArgumentException e) {
            informar("calcularLetra(" + numero + ") lanza IllegalArgumentException: "
                    + e.getMessage(), true);
        }
    }

    private static void probarValidar(String dni, boolean esperado) {
        boolean obtenido = DniUtils.validarDni(dni);
        String texto = (dni == null) ? "null" : "\"" + dni + "\"";
        informar("validarDni(" + texto + ") = " + obtenido, obtenido == esperado);
    }

    private static void informar(String descripcion, boolean correcto) {
        if (!correcto) {
            fallos++;
        }
        System.out.println((correcto ? "[OK]   " : "[FALLO] ") + descripcion);
    }
}