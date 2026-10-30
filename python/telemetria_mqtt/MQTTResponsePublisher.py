########################################## ~ LIBRERIAS ~ ###############################################
import paho.mqtt.client as mqtt
import json
import os
import datetime
import subprocess
########################################################################################################

########################################## ~ FUNCIONES ~ ###############################################

# Funcion para definir los callbacks para los eventos de conexión
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código de resultado: " + str(rc))
    # Suscribirse al topic al conectarse
    client.subscribe(topicSuscription)

def publicar_mensaje(server_address, username, password, topic, mensaje):
    # Crea una instancia del cliente MQTT
    client = mqtt.Client()
    
    # Configura el usuario y contraseña si es necesario
    if username and password:
        client.username_pw_set(username, password)
    
    # Conéctate al broker MQTT
    client.connect(server_address, 1883, 60)
    
    # Publica el mensaje en el topic
    client.publish(topic, mensaje)
    
    # Cierra la conexión
    client.disconnect()

########################################################################################################

