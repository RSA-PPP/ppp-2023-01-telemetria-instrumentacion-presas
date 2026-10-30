import json

# Abre y lee el archivo JSON de configuración
with open('/home/pasante1/configuracion/DatosConfiguracion.json', 'r') as config_file:
    configuracion = json.load(config_file)

# Accede a los datos en el archivo de configuración
id_dispositivo = configuracion["dispositivo"]["id"]
dir_archivos_recibidos = configuracion["directorios"]["archivosRecibidos"]
drive_cajas_medicion = configuracion["drive"]["cajasMedicion"]

# Imprime los valores
print("ID del dispositivo:", id_dispositivo)
print("Directorio de archivos recibidos:", dir_archivos_recibidos)
print("ID de Google Drive para cajas de medición:", drive_cajas_medicion)
