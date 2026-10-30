########################################## ~ LIBRERIAS ~ ###############################################
import numpy as np
from scipy import signal
from scipy.signal import correlate
from scipy.signal import butter,bessel,filtfilt, lfilter
import math
import sys
import os
import csv 
import json
from MQTTResponsePublisher import publicar_mensaje
########################################################################################################

######################################### ~ CONSTANTES ~ ###############################################
#Constantes:
sizeTramaShort = 702
sizeTramaInt = 350
periodoMuestreo = 5
#Variables:
factorResample = 10
periodoResample = periodoMuestreo/factorResample
dix = 25*factorResample
senal1 = []
senal2 = []
########################################################################################################

########################################## ~ FUNCIONES ~ ###############################################

def RemuestrearOffset(arrayMuestras, offset):
    #Convierte el array a formato np:
    npMuestras = np.array(arrayMuestras)
    resampleMuestras = signal.resample(npMuestras, len(npMuestras) * factorResample)
    resampleMuestras = resampleMuestras - offset
    return resampleMuestras

def texto(nameFile):
    pos1 = nameFile.find('_')
    nombre = nameFile[0:pos1]
    nameFile = nameFile[(nameFile.find('-')+1):]
    pos1 = nameFile.find('_')
    pos2 = nameFile.find('-')

    txt1 = nameFile[(pos1+1):pos2]
    txt1 = '20'+txt1[0:2]+'-'+txt1[2:4]+'-'+txt1[4:]
    
    txt2 = nameFile[(pos2+1):(pos2+7)]
    txt2 = txt2[0:2]+':'+txt2[2:4]+':'+txt2[4:]

    return nombre,txt1+'T'+txt2+'Z'

def extraer(datos,nombreCSV):
    name = '/home/rsa/resultados/vertederos/'+nombreCSV+'.csv'
    with open(name, mode='a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor_csv.writerow(datos)

########################################################################################################	
    
############################################# ~ MAIN ~ #################################################

if __name__ == "__main__":
   
    #*****************************************************************************
    #usr = os.environ.get('USER')                        #Obtencion del usuario
    usr = 'rsa'
    path_base = '/home/'+usr+'/' 
    rutaArchivoReferencia = path_base+"configuracion/"
    nombreArchivoReferencia = "Referencia_Btt-39-41-3.npy"
    pathArchivoReferencia = rutaArchivoReferencia + nombreArchivoReferencia
    referencia = np.load(pathArchivoReferencia)
    #*****************************************************************************

    #*****************************************************************************
    ##Abre el archivo binario::
    nombreArchivo2 = sys.argv[1]
    rutaCarpeta = path_base+"mediciones/vertederos/"
    path2 = rutaCarpeta + nombreArchivo2 + '.dat'
    #Abre y convierte el segundo archivo:
    f = open(path2, "rb")
    tramaDatosShort = np.fromfile(f, np.int8, sizeTramaShort)
    f.close()
    #Convierte el vector de datos tipo short en un vector de tipo int
    for i in range(0, sizeTramaInt - 1):
        datoIntLSB = tramaDatosShort[i * 2] 
        datoIntMSB = tramaDatosShort[(i * 2)+1]
        datoInt = ((datoIntMSB << 8) & 0xFF00) + ((datoIntLSB) & 0xFF)
        senal2.append(datoInt)
    #*****************************************************************************

    #*****************************************************************************
    #Obtiene los bytes de temperatura de la trama:
    temperaturaLSB = tramaDatosShort[sizeTramaShort - 2]
    temperaturaMSB = tramaDatosShort[sizeTramaShort - 1]
    temperaturaRaw = ((temperaturaMSB << 8) & 0xFF00) + ((temperaturaLSB) & 0xFF)
    #Verifica si la temperatura es negativa:
    if (temperaturaRaw & 0x8000):
        signoTemp = -1
        temperaturaRaw = ~temperaturaRaw + 1
    else:
        signoTemp = 1
    #Calcula la parte entera de la temperatura:
    temperaturaInt = (temperaturaRaw >> 4) * signoTemp
    #Calcula la parte decimal de la temperatura:
    temperaturaFloat = ((temperaturaRaw & 0x000F) * 625) / 10000.0
    #Calcula la temperatura:
    dTemp = -0.5
    temperaturaSensor = temperaturaInt + temperaturaFloat + dTemp
    Vsonido = 331.45 * math.sqrt(1 + (temperaturaSensor / 273))
    #*****************************************************************************

    #******************************************************************************        
    #Normaliza las senales:
    senal1 = RemuestrearOffset(referencia, 0)
    #senal2 = RemuestrearOffset(senal2, 508)
    senal2 = RemuestrearOffset(senal2, 517)
    nsamples = np.size(senal1)
        
    #Calcula la correlacion cruzada de la senal ultrasonica con la senal de referencia:
    xcorr = correlate(senal1, senal2)
    dt = np.arange(1-nsamples, nsamples)
    recovered_time_shift = dt[xcorr.argmax()]
    
    #Calculo del desfase en us:
    desfaseTiempo = recovered_time_shift*-1*periodoResample
    dA = -80.5
    TOF = 1375 + desfaseTiempo + dA
    Distancia = 0.5*(TOF/1e6)*Vsonido*1000

    # Texto
    nameCSV,fecha = texto(nombreArchivo2)

    # Salida 
    datos = [fecha,np.round(desfaseTiempo,2), np.round(temperaturaSensor,2),np.round(Distancia,2)]
    extraer(datos,nameCSV)
    print("Desfase [us]: %f" % desfaseTiempo) 
    print("Temperatura [gC]: %f" % temperaturaSensor)
    print("Distancia [mm]: %f" % Distancia) 
    '''
    print("Desfase [num muestras]: %d" % recovered_time_shift) 
    print("Periodo muestreo [us]: %f" % (periodoResample)) 
    print("Temperatura [gC]: %f" % temperaturaSensor) 
    print("Vsonido [m/seg]: %f" % Vsonido)
    print("TOF [us]: %f" % TOF) 
    print("Distancia [mm]: %f" % Distancia) 
    '''

    # Publica el resultado a traves de MQTT
    # Lee el archivo de configuracion de parametros MQTT
    nombre_sensor = "veterderos"
    with open("/home/rsa/configuracion/mqtt-configuracion.json", "r") as config_file:
        config = json.load(config_file)
    server_address = config["server_address"]
    username = config["username"]
    password = config["password"]
    topicSuscription = config["topic_solicitud"].replace("sensor", nombre_sensor)
    topicPublish = config["topic_respuesta"].replace("sensor", nombre_sensor)

    mensaje = {
    "sensor_id": "03",
    "desfase": desfaseTiempo,
    "temperatura": temperaturaSensor,
    "distancia": Distancia,
    }

    # Convierte el diccionario en una cadena JSON
    mensaje_json = json.dumps(mensaje)

    # Llama a la función para publicar el mensaje
    publicar_mensaje(server_address, username, password, topicPublish, mensaje_json)

    
#******************************************************************************