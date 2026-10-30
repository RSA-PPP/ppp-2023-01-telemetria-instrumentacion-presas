# Memoria Técnica de Prácticas Preprofesionales: Sistema de Adquisición, Monitoreo IoT y Procesamiento de Sensores Estructurales

**Autor:** Henry Castro  
**Tutor Institucional:** Ing. Milton Muñoz (Red Sísmica del Austro - RSA)  
**Institución:** Universidad de Cuenca  
**Proyecto:** Monitoreo y Telemetría de Instrumentación Estructural en Presas  
**Código:** RSA-PPP-2023-01  

---

## 1. Detección de Bordes para Coordinómetros

### 1.1. Descripción
Se realizaron optimizaciones sobre el software preexistente diseñado para la detección de bordes en coordinómetros ópticos de péndulo, con el objetivo de elevar la precisión y eficacia en la medición métrica de desplazamientos estructurales. Las modificaciones comprenden dos etapas:

1. **Preprocesamiento de Imagen:**
   - **Filtro Gaussiano:** Implementado para reducir el ruido visual de alta frecuencia presente en el entorno de túneles y galerías.
   - **Ecualizador de Histograma:** Aplicado para ajustar el contraste global relativo de la imagen, resaltando el hilo del péndulo frente al fondo metálico o de concreto del coordinómetro.
2. **Procesamiento de Bordes (Algoritmo de Canny):**
   - Se modificó la delimitación espacial del algoritmo. En lugar de aplicarlo sobre la totalidad del encuadre fotográfico (lo cual introducía falsos positivos por texturas irrelevantes), se acotó el análisis a una región de interés (ROI) que corresponde a la mitad crítica de la imagen donde oscila el hilo.

### 1.2. Implementación y Entorno
* **Script Principal:** `python/coordinometros/imageDetected2.py`
* **Dependencias:** OpenCV (`cv2`), NumPy, PiCamera, RPi.GPIO.
* **Control Físico:** Conmutación por modulación por ancho de pulsos (PWM en GPIO 12) para iluminación auxiliar previa al disparo fotográfico.
* **Salida de Resultados:** Registro estructurado de desplazamientos en formato tabular (`IZQ-N1-X.txt` / CSV) conteniendo fecha, hora, coordenadas de bordes en píxeles y desplazamiento métrico calculado en milímetros.

---

## 2. Estudio de Controlador Adaptativo de Ventana Móvil

### 2.1. Concepto y Metodología
Como propuesta para optimizar la carga computacional y resolución en la detección de bordes, se evaluó un algoritmo adaptativo de ventana móvil. El área de análisis se inicializa en la posición más probable donde se encuentra el borde del hilo del péndulo (lado izquierdo o derecho). En cada ciclo o iteración, el recuadro de análisis se desplaza dinámicamente siguiendo la tendencia del borde detectado en la captura precedente.

### 2.2. Resultados y Limitaciones Identificadas
* **Ventajas:** Reducción drástica del área de procesamiento de convolución, aumentando la velocidad de respuesta.
* **Limitación Crítica:** Si ocurre un desplazamiento abrupto o una oscilación mecánica rápida del hilo que sobrepase el ancho del recuadro activo entre dos capturas sucesivas, el algoritmo pierde la traza del péndulo y genera detecciones espurias (falsos positivos).
* **Conclusión Técnica:** Para monitoreo permanente desatendido en presas, la aproximación de ROI fija acotada a la zona de oscilación (mitad de imagen) demostró ser significativamente más robusta y confiable que el controlador dinámico de paso estrecho.

---

## 3. Automatización de Red Ad-Hoc Multihop

### 3.1. Arquitectura y Enrutamiento
Para permitir la interconexión inalámbrica de múltiples Raspberry Pi y concentradores en galerías subterráneas sin infraestructura de red comercial (Access Points), se diseñó un esquema Ad-Hoc 802.11 (IBSS) en canal 5 con ESSID `REDRSAIOT`.

Se estandarizaron dos configuraciones fundamentales a nivel de sistema operativo:
* `/etc/network/interfaces.d/wlan0`: Parámetros de capa física y enlace (IP estática, ESSID, canal, clave).
* `/etc/network/rutasEstaticas.sh`: Rutas de red multihop mediante comandos `route add`, permitiendo a nodos periféricos alcanzar la pasarela principal a través de gateways intermedios con reenvío de paquetes IP (`sysctl net.ipv4.ip_forward=1`).

### 3.2. Herramienta `automated_configuration.py`
Se diseñó un programa en Python que toma los parámetros de red definidos en `Configuracion_ad-hoc.json` y genera de manera autónoma los archivos de configuración del sistema a partir de las plantillas base, facilitando el comisionamiento de nuevos nodos sensores en campo.

---

## 4. Telemetría Desatendida, MQTT y Respaldo Cloud

### 4.1. Emisión Telemática Periódica (MQTT)
Para la transmisión en tiempo real de los desplazamientos calculados en los coordinómetros y niveles de vertederos:
* Se integró un cliente MQTT (Paho-MQTT) que emite tramas estructuradas en JSON cada 2 horas hacia el tópico `coordinometro/status`.
* Se implementó el módulo de acelerógrafos (`PublicarEventoMQTT.py`) que formatea alertas de disparos sísmicos hacia `registrocontinuo/eventos` recibiendo fecha, segundo del día y duración.

### 4.2. Persistencia y Respaldo en Google Drive
Para garantizar la integridad y custodia a largo plazo de las capturas fotográficas y mediciones:
* Las imágenes de comprobación y registros se organizan localmente en la tarjeta SD de la Raspberry Pi.
* Al acumular un periodo mensual de registros, una rutina automática comprime los directorios en formato `tar.gz`.
* Mediante la API v3 de Google Drive y flujos OAuth2 (`SubirArchivoDrive.py`, `subirArchivoCoordinometroDrive.py`), los archivos empaquetados se cargan de forma segura a las carpetas institucionales remotas de la RSA.
