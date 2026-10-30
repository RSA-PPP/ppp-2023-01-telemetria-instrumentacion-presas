import numpy as np
import cv2
from datetime import date
from datetime import datetime
import os
from picamera import PiCamera
from time import sleep
import os
import time
import RPi.GPIO as GPIO
from time import sleep

camera = PiCamera()
bandera=False

print(str(time.strftime("%H"))+":"+str(time.strftime("%M"))+":"+str(time.strftime("%S")))

def TomarFotografia(direccionCarpeta):

       now = datetime.now()

       GPIO.setmode(GPIO.BCM)
       GPIO.setwarnings(False)
       GPIO.setup(12, GPIO.OUT)
#GPIO.output(12, GPIO.HIGH)
       pwm = GPIO.PWM(12, 100)
       pwm.start(100)
       sleep(1)
       try:

       ##########################-Captura de Imagen-###########################
       ########################################################################
              camera.resolution= (600,300)
              #camera.rotation = 180
              camera.start_preview()
              #camera.capture(direccionCarpeta+'imagenSinZoom.jpeg')
              sleep(1)
              camera.zoom = (0.3, 0.5, 0.4, 0.4)
              sleep(1)
              imagenZoomx2 = direccionCarpeta +str(now)+'.jpg'
              camera.capture(imagenZoomx2)
              camera.stop_preview()
              sleep(1)
              pwm.stop()
       except:
              print("No se puede capturar la imagen")
              pwm.stop()

       return imagenZoomx2,now

def ProcesarImagen(imagen, direccionCarpeta, horaFecha):

       mat_datos_x=[]
       puntoMenor=0

       try:
       ####################-Procesamiento de Imagen-##########################
       #######################################################################

              img = cv2.imread(imagen)
              height, width = img.shape[:2]

              gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
              #gauss = cv2.medianBlur(gris,13)
              gauss = cv2.GaussianBlur(gris, (5,5), 0)
              cv2.imwrite(direccionCarpeta+'filtroblur.jpg',gauss)
              #canny = cv2.Canny(gauss, 100, 150)
              canny = cv2.Canny(gauss, 10, 50)

              lines = cv2.HoughLinesP(image=canny,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=180,maxLineGap=100)

              a,b,c = lines.shape

              f = open(direccionCarpeta+"IZQ-N1-X.txt","a")

              for i in range(a):
                     cv2.line(gauss, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
                     print(lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3])
                     mat_datos_x.append(lines[i][0][0])
                     cv2.imwrite(direccionCarpeta+'lineasMarcadas.jpg',gauss)

              puntoMayor=max(mat_datos_x)
              puntoMenor=min(mat_datos_x)
              #anchoCable=215
              anchoCable = puntoMayor - puntoMenor
              relacionPixel=2/anchoCable
              print(anchoCable)
              print(str(puntoMenor*relacionPixel)+' mm')

              mat_datos_x.clear()

              f.write(str(horaFecha)+"\t"+str(puntoMenor)+"\t"+ str(puntoMayor)+"\t"+str(puntoMenor*relacionPixel)+"\n")
              f.close

              puntoMenor=0
              puntoMayor=0
       except:
              print("Imagen Mala para realizar el calculo")


now = datetime.now()

fecha=time.strftime("%d-%m-%y")
hora=time.strftime("%H:%M:%S")
direccionCarpeta='/home/pi/resultados/'

imagenTomada,horaFecha=TomarFotografia(direccionCarpeta)
ProcesarImagen(imagenTomada,direccionCarpeta,horaFecha)

# while True:

       # fecha=time.strftime("%d-%m-%y")
       # horas=time.strftime("%H")
       # minutos=time.strftime("%M")
       # segundos=time.strftime("%S")

       # if str(minutos) != "05":
              # bandera=True

       # if (str(minutos) == "05" and str(segundos) == "00" and bandera==True):

              # print(str(time.strftime("%H"))+":"+str(time.strftime("%M"))+":"+str(time.strftime("%S")))

              # now = datetime.now()
              # os.mkdir('/home/pi/ProcesamientoCoordinoscopio/'+str(now)+'/')

              # fecha=time.strftime("%d-%m-%y")
              # hora=time.strftime("%H:%M:%S")
              # direccionCarpeta='/home/pi/ProcesamientoCoordinoscopio/Fotos/'

              # imagenTomada,horaFecha=TomarFotografia(direccionCarpeta)
              # ProcesarImagen(imagenTomada,direccionCarpeta,horaFecha)

              # bandera=False
