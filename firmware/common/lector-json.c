// Compilar: gcc -o lector lector-json.c -ljansson

/* Ejecutar: 
    1. gcc -c lector-json1.c -o lector-json.o
    2. ar rcs lector-json.a lector-json.o 
*/ 

#include <stdio.h>
#include <stdlib.h>
#include <jansson.h>
#include "lector-json.h"

int compilar_json() {
    FILE *file;
    json_t *root;
    json_error_t error;
    // Abrir el archivo JSON
    file = fopen("/home/pasante1/configuracion/DatosConfiguracion.json", "r");
    if (!file) {
        fprintf(stderr, "No se puede abrir el archivo\n");
        return 1;
    }

    // Cargar el contenido del JSON en una estructura de datos
    
    root = json_loadf(file, 0, &error);

    fclose(file);

    if (!root) {
        fprintf(stderr, "Error al leer el archivo JSON: %s\n", error.text);
        return 1;
    }

    // Verifica que el contenido es un objeto
    if (!json_is_object(root)) {
        fprintf(stderr, "El JSON no es un objeto\n");
        json_decref(root);
        return 1;
    }

    // Acceder a los datos
    json_t *dispositivo = json_object_get(root, "dispositivo");
    json_t *directorios = json_object_get(root, "directorios");
    json_t *drive = json_object_get(root, "drive");

    // Ejemplo de cómo acceder a una propiedad específica
    const char *id = json_string_value(json_object_get(dispositivo, "id"));

    printf("ID del dispositivo: %s\n", id);

    // No olvides liberar la memoria
    json_decref(root);

    return 0;
}