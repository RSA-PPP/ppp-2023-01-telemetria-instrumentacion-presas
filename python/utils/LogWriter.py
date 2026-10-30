'''
########################################## ~ LIBRERIAS ~ ###############################################
from __future__ import print_function
from googleapiclient import errors
import os
from datetime import datetime
import time
import sys 
import subprocess
import json
########################################################################################################

############################# ~ DIRECTORIOS Y ARCHIVOS PARA EL DRIVE~ ##################################
usr = os.environ.get('USER')                                                      #Obtencion del usuario
path_base = '/home/'+usr+'/'
path_logFile = path_base + 'log-files/'
path_jsonFile = path_base + 'configuracion/'
########################################################################################################

########################################## ~ FUNCIONES ~ ############################################### 
# Funcion: Extraer datos de un archivo .json
def importar_json(param1,param2):
    # Abre y lee el archivo JSON de configuración
    with open(path_jsonFile+'DatosConfiguracion.json', 'r') as config_file:
        configuracion = json.load(config_file)
    return configuracion[param1][param2]

# Funcion: Construir el nombre del archivo .log 
def nameFileLog():
    today = datetime.now()
    fecha = today.strftime('%Y-%m-%d')    
    hora = today.strftime("%H:%M:%S")
    return 'Log_'+importar_json("dispositivo","id")+fecha+'.log',hora  

# Funcion: Creacion del archivo .log 
def FileLog(msgLog,name_file,Hora):
    file_log = open(name_file,"a+")
    file_log.write(Hora+"\t"+msgLog+"\n")

########################################################################################################
msgLog = sys.argv[1]
name_file , Hora = nameFileLog()
name_file = path_logFile+name_file
FileLog(msgLog,name_file,Hora)

'''

# Importa las librerías necesarias
from __future__ import print_function
from datetime import datetime
import os
import json
import sys

# Variables globales
usr = os.environ.get('USER')
path_base = '/home/' + usr + '/'
path_logFile = path_base + 'log-files/'
path_jsonFile = path_base + 'configuracion/'

# Función: Extraer datos de un archivo .json
def importar_json(param1, param2):
    with open(path_jsonFile + 'DatosConfiguracion.json', 'r') as config_file:
        configuracion = json.load(config_file)
    return configuracion[param1][param2]

# Función: Construir el nombre del archivo .log
def nameFileLog():
    today = datetime.now()
    fecha = today.strftime('%Y-%m-%d')
    hora = today.strftime("%H:%M:%S")
    return 'Log_' + importar_json("dispositivo", "id") + fecha + '.log', hora

# Función: Creación del archivo .log
def FileLog(msgLog):
    name_file, Hora = nameFileLog()
    name_file = path_logFile + name_file
    file_log = open(name_file, "a+")
    file_log.write(Hora + "\t" + msgLog + "\n")

# Si se ejecuta como un script independiente, se puede usar para registrar mensajes de registro
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Proporcione un argumento para el mensaje de registro.")
    else:
        msgLog = sys.argv[1]
        FileLog(msgLog)
