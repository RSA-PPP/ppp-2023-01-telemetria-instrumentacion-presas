########################################## ~ LIBRERIAS ~ ###############################################
import paho.mqtt.client as mqtt
import json
import os
import datetime
import subprocess
########################################################################################################

########################################## ~ FUNCIONES ~ ###############################################

# Función para extraer la fecha, hora y duración del payload JSON
def procesar_mensaje(mensaje):
    payload = json.loads(mensaje.payload)
    sensor_id = payload["sensor_id"]
    tipo_medicion = payload["tipo_medicion"]
    accion = payload["accion"]
    timestamp = payload["timestamp"]
    print(f"Id: {sensor_id}, Tipo de medicion: {tipo_medicion}, Tiempo: {timestamp}")

    # Ejecuta el programa solicitado
    cmd = ["python3", f"/home/rsa/ejecutables/MedirVertedero.py", sensor_id ]
    subprocess.run(cmd)


# Funcion para definir los callbacks para los eventos de conexión
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código de resultado: " + str(rc))
    # Suscribirse al topic al conectarse
    client.subscribe(topicSuscription)

# Funcion para publicar mensajes
def publicar_mensaje(client, topic, mensaje):
    client.publish(topic, mensaje)

# Funciona para recibir mensajes
def on_message(client, userdata, msg):
    print("Mensaje recibido en el topic " + msg.topic + " con el contenido: ")
    payload_str = msg.payload.decode('utf-8')
    print(payload_str)
    # Procesa la solicitud
    procesar_mensaje(msg)
    # Publicar en el topic que ya se cumplio la tarea
    #publicar_mensaje(client, topicPublish, "completado")

########################################################################################################

############################################# ~ MAIN ~ #################################################

if __name__ == "__main__":

    # Lee el archivo de configuracion de parametros MQTT
    with open("/home/rsa/configuracion/mqtt-configuracion.json", "r") as config_file:
        config = json.load(config_file)
    server_address = config["server_address"]
    username = config["username"]
    password = config["password"]
    topicSuscription = config["topic_solicitud"]
    topicPublish = config["topic_respuesta"]

    # Crea una instancia del cliente MQTTc
    client = mqtt.Client()

    # Asigna los callbacks de conexión y de recepción de mensajes
    client.on_connect = on_connect
    client.on_message = on_message

    # Conexion al broker MQTT
    client.username_pw_set(username, password)
    client.connect(server_address, 1883, 60)

    # Inicia el loop para mantener la conexión y recibir mensajes
    client.loop_forever()

########################################################################################################