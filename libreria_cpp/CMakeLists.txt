
cmake_minimum_required(VERSION 3.16)
project(DNIUtils VERSION 1.0 LANGUAGES CXX)

add_library(dni_utils STATIC src/dni_utils.cpp)
target_include_directories(dni_utils PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/src")
target_compile_features(dni_utils PUBLIC cxx_std_17)

add_executable(prueba client/prueba.cpp)
target_link_libraries(prueba PRIVATE dni_utils)

enable_testing()
add_test(NAME dni_pruebas COMMAND prueba)
