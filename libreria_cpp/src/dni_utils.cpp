#include "dni_utils.h"

#include <cstring>
#include <cctype>

namespace {
    constexpr const char* LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE";
    constexpr int NUMERO_MAXIMO = 99999999;
}

char calcular_letra(int numero){
    if(numero < 0 || numero > NUMERO_MAXIMO){
        return '\0';
    }
    return LETRAS_DNI[numero % 23];
}


bool validar_dni(const char* dni){
    if(dni == nullptr || std::strlen(dni) != 9){
        return false;
    }

    int numero = 0;
    for(int i = 0; i < 8; i++){
        if(dni[i] < '0' || dni[i] > '9'){
            return false;
        }
        numero = numero * 10 + (dni[i] - '0');
    }

    char letra = static_cast<char>(
        std::toupper(static_cast<unsigned char>(dni[8]))
    );

    return calcular_letra(numero) == letra;
}
