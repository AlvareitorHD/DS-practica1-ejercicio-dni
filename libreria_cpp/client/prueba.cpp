#include "dni_utils.h"

#include <iostream>
#include <string>

using namespace std;

int main(){
    cout << "Letra de 12345678: " << calcular_letra(12345678) << "\n";
    cout << boolalpha;
    cout << "Validar 12345678Z: " << validar_dni("12345678Z") << "\n";
    cout << "Validar 12345678A: " << validar_dni("12345678A") << "\n";

    const bool correcto =
        calcular_letra(12345678) == 'Z' &&
        calcular_letra(0) == 'T' &&
        calcular_letra(1) == 'R' &&
        calcular_letra(-1) == '\0' &&
        calcular_letra(100000000) == '\0' &&
        validar_dni("12345678Z") &&
        validar_dni("00000000T") &&
        validar_dni("00000001R") &&
        !validar_dni("12345678A") &&
        !validar_dni("1234567Z") &&
        validar_dni("12345678z") &&
        !validar_dni(" 12345678Z") &&
        !validar_dni("X1234567L") &&
        !validar_dni(nullptr);

    if(!correcto){
        cout << "ERROR: Alguna prueba ha fallado. \n";
        return 1;
    }

    cout << "Todas las pruebas han pasado. \n";
    return 0;
}