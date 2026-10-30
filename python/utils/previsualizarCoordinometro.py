import subprocess
import sys
import time

def ejecutar_script_remoto(hostname):
    try:
        # Ejecutar el script de previsualización en la Raspberry Pi
        #ssh_command = f"ssh pi@{hostname} 'python3 /home/pi/previsualizar.py'"
        #subprocess.run(ssh_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Transferir la imagen a la máquina local
        scp_command = f"scp pi@{hostname}:/home/pi/capturas/preview.jpg /home/rsa/archivos-recibidos/"
        subprocess.run(scp_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def abrir_imagen():
    # Abre la imagen en el directorio local
    subprocess.run(['xdg-open', '/home/rsa/archivos-recibidos/preview.jpg'])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 previsualizarCoordinometro <hostname>")
        sys.exit(1)

    hostname = sys.argv[1]
    if ejecutar_script_remoto(hostname):
        # Esperar un poco antes de abrir la imagen
        time.sleep(3)
        abrir_imagen()
    else:
        print("Falló la ejecución remota o la transferencia de archivos.")
