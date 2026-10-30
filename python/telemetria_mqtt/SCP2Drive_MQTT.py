########################################## ~ LIBRERIAS ~ ###############################################
import paho.mqtt.client as mqtt
import json
import os
import datetime
import subprocess
import time
import sys
########################################################################################################

####################################### ~ PARAMETROS_MQTT ~ ############################################
server_address = "www.domoqu.com"
username = "rsa"
password = "RSAiotace2023"
topic = "parametros"
########################################################################################################

###################################### ~ VARIABLES GLOBALES ~ ##########################################
payload_str = ""
########################################################################################################

############################# ~ DIRECTORIOS Y ARCHIVOS PARA EL DRIVE~ ##################################
usr = os.environ.get('USER')                                                      #Obtencion del usuario
path_base = '/home/'+usr+'/'                                                      #Ruta Base 
path_SubirArchivoRemotoDrive = path_base+'programas/subirArchivos/subirArchivoRemotoDrive.py'
########################################################################################################

########################################## ~ FUNCIONES ~ ###############################################
# Definir los callbacks para los eventos de conexión
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código de resultado: " + str(rc))
    # Suscribirse al topic al conectarse
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print("Mensaje recibido en el topic " + msg.topic + " con el contenido: " + str(msg.payload))
    payload_str = msg.payload.decode('utf-8')
    consola(payload_str)
    publicar_mensaje(client, "status", "completado")
    client.loop_stop()
    client.disconnect()
    sys.exit(0)

def publicar_mensaje(client, topic, mensaje):
    client.publish(topic, mensaje)

def consola(pay): 
    returned_output = subprocess.call('python3 '+path_SubirArchivoRemotoDrive+" "+pay,shell = True)
########################################################################################################


########################################### ~ MAIN ~ ###################################################
# Configuracion de MQTT
# Crear una instancia del cliente MQTTc
client = mqtt.Client()

# Asignar los callbacks de conexión y de recepción de mensajes
client.on_connect = on_connect
client.on_message = on_message

# Conectarse al broker MQTT
client.username_pw_set(username, password)
client.connect(server_address, 1883, 60)
client.loop_forever()


########################################################################################################

