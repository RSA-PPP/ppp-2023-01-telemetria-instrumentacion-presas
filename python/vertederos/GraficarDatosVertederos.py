################################## ~ LIBRERIAS ~ ##################################
import csv
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
###################################################################################

#################################### ~ RUTAS ~ ####################################
usr = os.environ.get('USER')
path_base = '/home/'+usr+'/resultados/vertederos/'
nameFile = sys.argv[1]
path = path_base + nameFile 
###################################################################################

################################## ~ FUNCIONES ~ ##################################
# FUNCION: Importar CSV
def import_csv():
    date_format = '%Y-%m-%dT%H:%M:%SZ'
    fecha = []                              #Almacena la hora de la medicion
    desf  = []                              #Almacena los desfases [us]
    temp  = []                              #Almacena la temperatura [gC]
    d     = []                              #Almacena la distancia [mm]
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            fecha.append(datetime.strptime(row[0], date_format))
            desf.append(float(row[1]))
            temp.append(float(row[2]))
            d.append(float(row[3])) 
    return [fecha, desf,temp,d]

# FUNCION: Graficar datos
def graficar(x,y,yLabel,titulos):
    total = len(y)
    plt.figure(figsize=(10, 15))
    for k1 in range(1,total+1):
        plt.subplot(3,1,k1)
        plt.plot(x,y[k1-1])
        plt.title(titulos[k1-1])
        plt.xticks(rotation=45, ha='right')
        plt.ylabel(yLabel[k1-1])
    plt.tight_layout()
    #plt.savefig(path_base+'imagenes/resultados.png')
    plt.show()
###################################################################################

##################################### ~ MAIN ~ ####################################
datos = import_csv()
graficar(datos[0],datos[1:],['us','gC','mm'],["DESFASE","TEMPERATURA","DISTANCIA"])
################################################################################### 
