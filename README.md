# ppp-2023-01-telemetria-instrumentacion-presas

> **Red Sísmica del Austro (RSA) — Universidad de Cuenca**  
> Prácticas Preprofesionales (PPP) • Sistemas Embebidos, Visión por Computador, Redes IoT y Telemetría

---

## 📋 Ficha Técnica del Proyecto

| Campo | Detalle |
| :--- | :--- |
| **Código Institucional** | `RSA-PPP-2023-01` |
| **Nombre del Proyecto** | Sistema de Adquisición, Procesamiento por Visión Artificial y Telemetría IoT para Sensores Estructurales de Presas |
| **Pasante** | Henry Castro (`henry.castro@ucuenca.edu.ec`) |
| **Carrera / Institución** | Ingeniería en Electrónica y Telecomunicaciones — Universidad de Cuenca |
| **Tutor Institucional** | Ing. Milton Muñoz (`milton.munozc@ucuenca.edu.ec`) — RSA |
| **Duración / Horas** | 144 horas (10.5 semanas) • Presencial / Remota |
| **Fecha de Ejecución** | 2023-11-22 al 2024-04-10 |
| **Estado** | `Culminado` |

---

## 🎯 Descripción General y Objetivos

Este proyecto aborda la modernización e integración de los sistemas de instrumentación estructural y auscultación para presas gestionadas por la Red Sísmica del Austro (RSA). Comprende el desarrollo y refinamiento de algoritmos de procesamiento digital de imágenes para coordinómetros ópticos (péndulos directos e inversos), correlación acústica para vertederos de aforo, estandarización de mensajería telemática MQTT para alertas de acelerógrafos y esquemas de respaldo desatendido en Google Drive.

Asimismo, contempla la arquitectura de red inalámbrica Ad-Hoc 802.11 (IBSS) y tablas de enrutamiento estático multihop para galerías subterráneas donde no existe cobertura de puntos de acceso comerciales.

### Objetivos Clave
1. **Visión por Computador en Coordinómetros:** Optimizar el algoritmo de detección de bordes en `imageDetected2.py` mediante filtro gaussiano, ecualización de histograma y restricción a región de interés (ROI).
2. **Evaluación de Controlador Adaptativo:** Analizar técnica y experimentalmente las capacidades y limitaciones de una ventana móvil de seguimiento dinámico de bordes.
3. **Telemetría y Mensajería MQTT:** Estandarizar la publicación estructurada de eventos sísmicos (`PublicarEventoMQTT.py`) y crear módulos para recepción de solicitudes y publicación de estados.
4. **Respaldo Cloud Automatizado:** Desarrollar rutinas en Python con la API de Google Drive para empaquetado mensual (`tar.gz`) y transferencia de registros.
5. **Correlación Acústica de Vertederos:** Procesar señales ultrasónicas de aforo para cálculo continuo de nivel de agua y temperatura con generación gráfica.
6. **Infraestructura de Red Ad-Hoc:** Especificar y parametrizar la autoconfiguración de interfaces `wlan0` y tablas de ruteo multihop en Linux.

> 📄 Para consultar la planificación histórica detallada, revisa el [Plan de Trabajo Oficial](docs/planificacion.md).  
> 📑 Para consultar el informe técnico completo de la pasantía, revisa la [Memoria Técnica](docs/informe_tecnico_practicas.md).

---

## 🏗️ Arquitectura del Sistema y Flujo de Trabajo

```text
+-----------------------------------------------------------------------------------------+
|                                ARQUITECTURA DEL SISTEMA                                 |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [Coordinómetro Óptico]  ---> [PiCamera + OpenCV] ---> [Canny ROI + HoughLinesP]        |
|                                                                 |                       |
|  [Sensor Ultrasonido]    ---> [Trama Binaria .dat] ---> [Correlación Acústica]          |
|                                                                 |                       |
|                                                                 v                       |
|                                              +--------------------------------------+   |
|                                              |  Raspberry Pi / Concentrador Linux   |   |
|                                              +--------------------------------------+   |
|                                                    |                          |         |
|                         (Red Ad-Hoc 802.11 IBSS)   |                          |         |
|                         (wlan0 / Rutas Estáticas)  v                          v         |
|                                            [Broker MQTT]             [Google Drive API] |
|                                       (Alertas & Telemetría)       (Backups Mensuales)  |
+-----------------------------------------------------------------------------------------+
```

---

## 📂 Estructura del Repositorio

```text
ppp-2023-01-telemetria-instrumentacion-presas/
├── config/
│   ├── DatosConfiguracion.example.json    # Plantilla de rutas locales e IDs de Drive
│   └── mqtt-configuracion.example.json    # Plantilla de broker, credenciales y tópicos
│
├── data/
│   ├── evidence/                          # Series reales de desplazamientos y gráficas
│   │   ├── DER-N1-X.txt
│   │   ├── C1-N2.csv
│   │   └── resultados.png
│   └── raw_samples/                       # Muestras crudas de calibración y referencia
│       ├── C1-N1_231006-153050.dat
│       └── Referencia_Btt-39-41-3.npy
│
├── docs/
│   ├── hardware/                          # Especificaciones físicas e instrumentales
│   ├── troubleshooting/                   # Bitácora de incidencias resueltas
│   ├── planificacion.md                   # Documento rector de la pasantía
│   ├── informe_tecnico_practicas.md       # Memoria técnica formal del practicante
│   └── especificaciones_red_adhoc.md      # Especificaciones de wlan0 y ruteo multihop
│
├── firmware/
│   ├── common/                            # Utilidades en C (parser JSON con Jansson)
│   │   ├── lector-json.c
│   │   └── lector-json.h
│   ├── drivers/
│   └── tests/
│
├── python/
│   ├── coordinometros/                    # Algoritmos de visión artificial para péndulo
│   │   └── imageDetected2.py
│   ├── telemetria_mqtt/                   # Publicadores, gestores y simulación MQTT
│   │   ├── PublicarEventoMQTT.py
│   │   ├── MQTTRequestManager.py
│   │   ├── MQTTResponsePublisher.py
│   │   ├── MQTTStorage.py
│   │   ├── SCP2Drive_MQTT.py
│   │   ├── SensorSimuladoMQTT.py
│   │   └── pruebas_mqtt.py
│   ├── vertederos/                        # Procesamiento de nivel por correlación
│   │   ├── CorrelacionUltrasonido.py
│   │   └── GraficarDatosVertederos.py
│   ├── cloud_drive/                       # Sincronización y subida a Google Drive v3
│   │   ├── SubirArchivoDrive.py
│   │   ├── subirArchivoCoordinometroDrive.py
│   │   ├── subirArchivoRemotoDrive.py
│   │   ├── CoordFiles2Drive.py
│   │   ├── LocalFile2Drive.py
│   │   └── RemoteFile2Drive.py
│   ├── utils/                             # Herramientas de soporte y logging
│   │   ├── previsualizarCoordinometro.py
│   │   ├── LogWriter.py
│   │   └── LeerArchivoJSON.py
│   └── requirements.txt                   # Dependencias de Python
│
├── README.md                              # Ficha técnica institucional
└── .gitignore                             # Reglas de exclusión Git
```

---

## 🛠️ Herramientas y Requisitos de Desarrollo

* **Hardware / SBCs:** Raspberry Pi 3 Model B+ / Raspberry Pi 4 Model B, Módulo PiCamera v2, Sensores Ultrasónicos de nivel.
* **Sistema Operativo:** Raspberry Pi OS / Debian Linux.
* **Entorno Python 3:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r python/requirements.txt
  ```
* **Librerías de Sistema (C / Linux):**
  ```bash
  sudo apt-get update
  sudo apt-get install -y libjansson-dev wireless-tools
  ```

---

## 🚀 Puesta en Marcha

### 1. Configuración de Entorno
Copiar las plantillas de configuración y definir los parámetros del entorno local:
```bash
cp config/DatosConfiguracion.example.json config/DatosConfiguracion.json
cp config/mqtt-configuracion.example.json config/mqtt-configuracion.json
```

### 2. Ejecución de Coordinómetro (Captura y Procesamiento)
```bash
python3 python/coordinometros/imageDetected2.py
```

### 3. Publicación de Eventos por MQTT
```bash
python3 python/telemetria_mqtt/PublicarEventoMQTT.py <FECHA_AAMMDD> <SEGUNDOS_DIA> <DURACION_SEG>
# Ejemplo:
python3 python/telemetria_mqtt/PublicarEventoMQTT.py 231122 54000 30
```

### 4. Procesamiento de Vertedero (Correlación Ultrasónica)
```bash
python3 python/vertederos/CorrelacionUltrasonido.py C1-N1_231006-153050
```

---

## 🛡️ Reglas de Trabajo y Control de Versiones

1. **Rama Principal:** La rama activa de trabajo es **`main`**.
2. **Formato de Commits:** Convención estándar en minúsculas:
   - `feat: nueva funcionalidad o módulo implementado`
   - `fix: corrección en script o algoritmo`
   - `docs: actualización de documentación o memoria técnica`
   - `refactor: optimización de código sin alterar funcionalidad`
