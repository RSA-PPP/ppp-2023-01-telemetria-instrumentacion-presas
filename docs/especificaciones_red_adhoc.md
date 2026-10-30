# Especificaciones Técnicas: Red Inalámbrica Ad-Hoc y Ruteo Estático

Este documento detalla la arquitectura, esquemas de direccionamiento y plantillas de configuración desarrolladas para la interconexión de nodos de instrumentación y gateways en la presa mediante enlaces 802.11 Ad-Hoc (IBSS).

---

## 1. Topología y Parámetros de Red

* **Modo de Operación:** 802.11 IBSS (Ad-Hoc)
* **Interfaz de Red:** `wlan0`
* **Canal Inalámbrico:** 5 (2.432 GHz)
* **ESSID:** `REDRSAIOT`
* **Seguridad / Clave:** `s:RSA_Iot_PCL_UC`
* **Mascara de Subred:** `255.255.255.0` (`/24`)

---

## 2. Esquema de Direccionamiento JSON

La configuración de red de cada nodo o gateway se parametriza de forma centralizada mediante un archivo `Configuracion_ad-hoc.json` estructurado de la siguiente forma:

```json
{
    "ip-local-host": "192.168.10.21",
    "ip-gateway-principal": "192.168.10.5",
    "ip-gateway-intermedio": "192.168.10.31",
    "essid": "REDRSAIOT",
    "key": "s:RSA_IoT_PCL_UC"
}
```

### Roles de Nodo:
* **Nodo Cliente / Sensor:** Cuando `ip-local-host != ip-gateway-intermedio`. Enruta tráfico hacia el gateway intermedio (métrica 1) y hacia el gateway principal (métrica 2).
* **Gateway Intermedio:** Cuando `ip-local-host == ip-gateway-intermedio`. Conmuta tráfico bidireccional entre nodos internos y el gateway principal, con reenvío IP activo (`sysctl net.ipv4.ip_forward=1`).

---

## 3. Plantillas de Configuración del Sistema

### 3.1. Archivo `/etc/network/interfaces.d/wlan0`

```bash
auto wlan0
iface wlan0 inet static
        address <ip-local-host>
        netmask 255.255.255.0
        broadcast 192.168.10.255
        wireless-channel 5
        wireless-essid <essid>
        wireless-mode ad-hoc
        wireless-key <key>
```

---

### 3.2. Script `/etc/network/rutasEstaticas.sh`

#### Caso A: Nodo Sensor Estándar
```bash
#!/bin/bash
ip route flush dev wlan0
route add <ip-local-host> dev wlan0
route add <ip-gateway-intermedio> gw <ip-local-host> metric 1 dev wlan0
route add <ip-gateway-principal> gw <ip-gateway-intermedio> metric 2 dev wlan0
route add -net 0.0.0.0 netmask 0.0.0.0 gw <ip-gateway-intermedio> metric 202 dev wlan0
sudo sysctl net.ipv4.ip_forward=1
```

#### Caso B: Gateway Intermedio
```bash
#!/bin/bash
ip route flush dev wlan0
route add <ip-local-host> dev wlan0
route add <ip-cliente-2> gw <ip-gateway-intermedio> metric 1 dev wlan0
route add <ip-gateway-principal> gw <ip-gateway-intermedio> metric 1 dev wlan0
route add -net 0.0.0.0 netmask 0.0.0.0 gw <ip-gateway-principal> metric 202 dev wlan0
sudo sysctl net.ipv4.ip_forward=1
```

---

## 4. Automatización con `automated_configuration.py`

El script `automated_configuration.py` (diseñado durante la práctica) lee el archivo JSON correspondiente a la estación y genera dinámicamente los dos archivos de sistema descritos (`/etc/network/interfaces.d/wlan0` y `/etc/network/rutasEstaticas.sh`), asignando permisos de ejecución y permitiendo desplegar nuevos nodos sin manipulación manual en campo.
