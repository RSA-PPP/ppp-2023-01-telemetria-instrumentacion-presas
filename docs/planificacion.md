---
titulo: "Plan de Trabajo de Prácticas Preprofesionales: Sistema de Adquisición, Monitoreo IoT y Procesamiento de Sensores Estructurales en Presas"
proyecto: "Monitoreo y Telemetría de Instrumentación Estructural - Presas"
codigo_proyecto: "RSA-PPP-2023-01"
area_tematica: "Sistemas Embebidos, Visión por Computador, Redes IoT y Telemetría"
estado: "Culminado"
version: "1.0"
fecha_creacion: "2023-11-22"
fecha_actualizacion: "2024-04-12"

pasante:
  nombre: "Henry Castro"
  cedula: "N/D"
  correo: "henry.castro@ucuenca.edu.ec"
  carrera: "Ingeniería en Electrónica y Telecomunicaciones"
  institucion: "Universidad de Cuenca"

tutoria:
  tutor_institucional: "Ing. Milton Muñoz. (Red Sísmica del Austro - RSA)"
  correo_tutor_institucional: "milton.munozc@ucuenca.edu.ec"

cronograma:
  duracion_total_horas: 120
  dedicacion_semanal_horas: 14
  duracion_semanas: 8.5
  fecha_inicio: "2023-11-22"
  fecha_fin_estimada: "2024-04-10"
  modalidad: "Presencial / Remota"

tecnologias:
  - "Hardware y SBCs: Raspberry Pi 3/4, Estación Concentradora, Nodos Sensores"
  - "Lenguajes de Programación: Python 3, Bash Shell Scripting, C, SQL"
  - "Visión Artificial y Procesamiento de Señales: OpenCV (Filtro Gaussiano, Ecualización de Histograma, Algoritmo Canny, ROI dinámico, Correlación Acústica)"
  - "Redes y Protocolos IoT: Red Ad-Hoc 802.11 (IBSS wlan0, enrutamiento estático multihop), MQTT (Paho-MQTT, JSON), SSH, RealVNC"
  - "Almacenamiento y Cloud: Google Drive API, compresión TAR.GZ, CSV estructurado"

repositorio:
  url: "https://github.com/RSA-PPP/ppp-2023-01-telemetria-instrumentacion-presas"
  rama_base: "main"
---

---

## 1. Antecedentes y Justificación Técnica

1. **Contexto del Sistema y Estado Inicial:** 
   La Red Sísmica del Austro (RSA) gestiona la auscultación y monitoreo de la salud estructural de presas a través de instrumental especializado que incluye coordinómetros ópticos (medición de desplazamientos del péndulo inverso y directo), vertederos de aforo y una red de acelerógrafos para registro sísmico continuo. Al inicio de la pasantía, los coordinómetros operaban con un software preliminar en Raspberry Pi (`imageDetected2.py`) que capturaba imágenes del hilo del péndulo pero presentaba vulnerabilidad al ruido visual y cambios lumínicos dentro de los túneles de la presa. En cuanto a la red de acelerógrafos, la difusión de eventos sísmicos mediante MQTT requería estandarización de formatos de disparo. Además, existía la necesidad de interconectar los nodos de la presa en un esquema de red inalámbrica Ad-Hoc sin depender de puntos de acceso comerciales.

2. **Limitaciones Críticas Identificadas:** 
   * **Inestabilidad en la Detección de Bordes del Péndulo:** El algoritmo Canny se ejecutaba sobre el encuadre completo de la imagen sin preprocesamiento de contraste, provocando falsos positivos en el cálculo de posición del hilo debido al fondo ruidoso.
   * **Falsa Clasificación de Eventos Sísmicos en MQTT:** En el servidor concentrador, se requería una correcta catalogación de eventos aislados y locales/sísmicos.
   * **Inexistencia de Enrutamiento Automatizado en Túneles:** La topología de galerías subterráneas exigía comunicación inalámbrica Ad-Hoc entre nodos y gateways intermedios; la configuración manual de interfaces de red (`wlan0`) y tablas de ruteo estático (`rutasEstaticas.sh`) resultaba propensa a errores.
   * **Persistencia y Respaldo Incompletos:** Las mediciones generadas requerían un pipeline automático de respaldo en la nube (Google Drive) y sincronización periódica hacia brokers MQTT remotos.

3. **Propuesta de Solución Implementada:** 
   * Estandarización del flujo de eventos MQTT en acelerógrafos (`PublicarEventoMQTT.py`).
   * Perfeccionamiento del pipeline de visión por computador en OpenCV (filtro gaussiano, ecualizador de histograma y reducción del área de Canny a ROI de interés).
   * Automatización integral de la configuración de red Ad-Hoc y ruteo multihop en Linux mediante scripts parametrizados por JSON.
   * Implementación de la persistencia en CSV, publicación periódica MQTT cada 2 horas y respaldo comprimido en Google Drive.
   * Procesamiento de correlación acústica en vertederos de aforo.

---

## 2. Objetivos del Plan de Trabajo

### 2.1. Objetivo General
Desarrollar, optimizar e integrar un sistema integral de adquisición de datos, procesamiento por visión por computador, correlación acústica, enrutamiento en red Ad-Hoc y telemetría automatizada (MQTT y Google Drive) para los sensores estructurales de presas (coordinómetros, vertederos y acelerógrafos).

### 2.2. Objetivos Específicos
1. Desarrollar e implementar los scripts en Python para la publicación estandarizada (`PublicarEventoMQTT.py`) bajo el protocolo MQTT, formateando la carga útil en JSON hacia tópicos institucionales.
2. Optimizar el algoritmo de visión artificial para la medición de posición en coordinómetros (`imageDetected2.py`), aplicando filtro gaussiano para reducción de ruido, ecualización de histograma y delimitación del área de Canny a la región de interés (ROI).
3. Investigar y evaluar experimentalmente el concepto de un controlador adaptativo de ventana móvil para el seguimiento dinámico del hilo del péndulo ante oscilaciones mecánicas.
4. Diseñar la arquitectura para autoconfiguración de nodos en red Ad-Hoc (`wlan0`) y enrutamiento estático multihop a partir de archivos centralizados en formato JSON.
5. Implementar el módulo de telemetría y persistencia para la emisión periódica de estados por MQTT cada 2 horas, almacenamiento local de registros en CSV y empaquetado comprimido (`tar.gz`) con subida a Google Drive.
6. Integrar algoritmos de correlación acústica para la medición de nivel en vertederos de aforo.

---

## 3. Fases de Trabajo Detalladas

### Fase 1: Publicación y Gestión de Eventos por MQTT (Acelerógrafos)
* **Objetivo:** Estandarizar la publicación de eventos detectados por acelerógrafos hacia brokers MQTT institucionales.
* **Actividades técnicas:**
  1. Desarrollar el script `PublicarEventoMQTT.py` para publicar alertas recibiendo: Fecha (AAMMDD), Hora (segundos del día) y Duración (segundos).
  2. Formatear la carga útil en JSON e integrar variables dinámicas de ubicación y dispositivo hacia el tópico MQTT `registrocontinuo/eventos`.
  3. Implementar gestores de solicitudes y respuestas MQTT (`MQTTRequestManager.py`, `MQTTResponsePublisher.py`).

### Fase 2: Preprocesamiento y Detección de Bordes en Coordinómetros (OpenCV)
* **Objetivo:** Incrementar la precisión y robustez en la medición óptica de desplazamientos del hilo del péndulo mediante procesamiento digital de imágenes.
* **Actividades técnicas:**
  1. Incorporar etapa de preprocesamiento en `imageDetected2.py` con filtro gaussiano y ecualización de histograma.
  2. Restringir el algoritmo de Canny exclusivamente a la mitad crítica de la imagen donde oscila el hilo.
  3. Controlar la iluminación auxiliar mediante modulación PWM por GPIO.
  4. Desarrollar la rutina de cálculo métrico del desplazamiento y exportación estructurada a archivos tabulares.

### Fase 3: Evaluación de Algoritmo Adaptativo (Ventana Móvil)
* **Objetivo:** Explorar y evaluar una arquitectura de controlador dinámico de área de interés para el seguimiento focalizado de bordes en el coordinómetro.
* **Actividades técnicas:**
  1. Analizar el desplazamiento dinámico de la ROI según el borde detectado en la iteración previa.
  2. Caracterizar los límites operacionales: identificar pérdida de seguimiento ante saltos mecánicos abruptos que excedan la ventana.
  3. Concluir sobre la superioridad de la ventana fija optimizada para instalaciones permanentes.

### Fase 4: Infraestructura de Red Inalámbrica Ad-Hoc en Nodos Linux
* **Objetivo:** Diseñar la parametrización de red Ad-Hoc y ruteo multihop para enlaces en túneles sin cobertura de red comercial.
* **Actividades técnicas:**
  1. Estandarizar la plantilla de red Ad-Hoc (`wlan0` en canal 5, ESSID `REDRSAIOT`).
  2. Estructurar el archivo de configuración centralizado `Configuracion_ad-hoc.json` definiendo roles de nodo cliente y gateway intermedio.
  3. Diseñar la lógica de enrutamiento estático en `rutasEstaticas.sh` con métricas y reenvío IP (`sysctl net.ipv4.ip_forward=1`).

### Fase 5: Sistema de Transmisión MQTT, Persistencia y Respaldo Cloud
* **Objetivo:** Implementar la orquestación desatendida para envío de telemetría a servidores remotos y respaldo de imágenes en Google Drive.
* **Actividades técnicas:**
  1. Integrar el cliente MQTT para publicación periódica cada 2 horas de coordenadas detectadas.
  2. Programar la rutina de empaquetado mensual: compresión en lote de imágenes procesadas en formato `tar.gz`.
  3. Configurar scripts de sincronización con Google Drive API v3 (`SubirArchivoDrive.py`, `subirArchivoCoordinometroDrive.py`, `RemoteFile2Drive.py`).

### Fase 6: Procesamiento de Vertederos y Documentación Final
* **Objetivo:** Implementar correlación acústica de sensores de vertederos y compilar la documentación técnica final.
* **Actividades técnicas:**
  1. Integrar script de correlación acústica (`CorrelacionUltrasonido.py`) para cálculo de nivel y temperatura.
  2. Generar rutinas de graficación (`GraficarDatosVertederos.py`) con Matplotlib.
  3. Redactar el Informe Final de Prácticas Preprofesionales y compilar la documentación de código y especificaciones.
