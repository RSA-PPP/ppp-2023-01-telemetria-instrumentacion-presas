############################################# ~ LIBRERIAS ~ ##################################################
import paho.mqtt.client as mqtt
import json
import os
import subprocess
import time
import sys
import random
from datetime import datetime
import numpy as np
##############################################################################################################

#################################### ~ PARAMETROS DE CONFIGURACION ~ #########################################
# Parametros MQTT
usr = os.environ.get('USER')                                                      #Obtencion del usuario
path_base = '/home/'+usr+'/'                                                      #Ruta Base 

with open(path_base + 'configuracion/mqtt-configuracion.json',"r") as condig_file:
    config = json.load(condig_file)

server_address = config["server_address"]
username = config["username"]
password = config["password"]

# Parametros de Simulacion del sensor
valMin = 10                                                     # Valor Minimo
valMax = 15                                                     # Valor Maximo

# Caracteristicas del sensor
ID = '01'
tipo_medicion = "temperatura"
unidad = "grados Celcius"

# Topics MQTT
topicSuscription = config["topicSuscription"]   # Topic para suscribirse a la solicitud 
topicPublish = config["topicPublish"]    # Topic para publicar la respuesta

##############################################################################################################

############################################# ~ FUNCIONES ~ ##################################################
# Definir los callbacks para los eventos de conexión
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código de resultado: " + str(rc))
    # Suscribirse al topic al conectarse
    client.subscribe(topicSuscription)

# Acciones a ejecutar una vez que se recibio un mensaje 
def on_message(client, userdata, msg):
    print("Mensaje recibido en el topic " + msg.topic + " con el contenido: " + str(msg.payload))
    payload_str = msg.payload.decode('utf-8')
    print("Payload: ",payload_str)
    if payload_str == "medir":
        medicion = simuMedicion(valMax,valMin)
        hora_actual = horaMedicion()
        publicar_mensaje(client, topicPublish,format_json(medicion,hora_actual))

# Publicar un mensaje en el TOPIC:topicPublish
def publicar_mensaje(client, topic, mensaje):
    client.publish(topic, mensaje)

# Simulacion basica del sensor
def simuMedicion(valMax,valMin):
    return str(np.round(random.uniform(valMin,valMax),2))

# Hora de la medicion en formato ISO 8601 
def horaMedicion():
    hora_actual = datetime.now()
    fecha = hora_actual.strftime("%Y-%m-%dT%H:%M:%SZ")
    return fecha

# Mensaje en formato JSON
def format_json(med,hora):
    id = '"sensor_id": "'+ID+'",'
    medicion = '"tipo_medicion": "'+tipo_medicion+'",'
    valor = '"valor": "' + med+'",'
    unit = '"unidad":  "'+unidad+'",'
    timestamp = '"timestamp": "'+hora+'"'
    return '{\n\t'+id+'\n\t'+medicion+'\n\t'+valor+'\n\t'+unit+'\n\t'+timestamp+'\n}'

##############################################################################################################

############################################## ~ MAIN ~ ######################################################
client = mqtt.Client()

# Asignar los callbacks de conexión y de recepción de mensajes
client.on_connect = on_connect
client.on_message = on_message

# Conectarse al broker MQTT
client.username_pw_set(username, password)
client.connect(server_address, 1883, 60)
client.loop_forever()
##############################################################################################################
