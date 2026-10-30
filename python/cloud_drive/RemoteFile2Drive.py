import sys 
import subprocess
import os
import LogWriter

# ////////////////////////////////// Metodos //////////////////////////////////

# **********************************************************************
# ****************** Metodo obtener_archivo_scp ************************
# **********************************************************************
# Metodo para obtener un archivo de un host remoto.
# Recibe como parametros: el usuario remoto, el host remoto, 
# y el path completo del archivo remoto.
# Guarda el archivo recuperado en el directorio local:
# /home/rsa/archivos-recibidos/
def obtener_archivo_scp(usr_remoto,host_remoto,archivo_remoto): 
    returned_output = subprocess.call('scp '+ usr_remoto +'@' + host_remoto + ':' + archivo_remoto + ' /home/rsa/archivos-recibidos/',shell = True)
    if returned_output == 1:
        print("*******************************************************************")
        LogWriter.FileLog("  Error al obtener el archivo " + usr_remoto + "@" + host_remoto + ":" + archivo_remoto)
        sys.exit()
    else:
        print("Archivo Encontrado")
        LogWriter.FileLog("  Se obtuvo el archivo " + usr_remoto + "@" + host_remoto + ":" + archivo_remoto)
        file_name = os.path.basename(archivo_remoto)
        return os.path.splitext(file_name)
# **********************************************************************
# **************** Fin Metodo obtener_archivo_scp **********************
# **********************************************************************

# /////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////// Principal /////////////////////////////////
if __name__ == '__main__':

    print("Inicio RemoteFile2Drive")
    LogWriter.FileLog("Inicio RemoteFile2Drive")

    # Obtiene los parametros de entrada
    op = sys.argv[1]                                                 
    parametro1 = sys.argv[1]                                        # Usuario del host
    parametro2 = sys.argv[2]                                        # Nombre del host
    parametro3 = sys.argv[3]                                        # Path del archivo

    # obtiene el nombre del archivo remoto
    file_name = obtener_archivo_scp(parametro1,parametro2,parametro3)
    nombreArchivoRemoto = file_name[0]+file_name[1]
    #print(file_name)
    #print(nombreArchivoRemoto)

    # Ejecuta el programa LocalFile2Drive.py
    comando = ["python3", "LocalFile2Drive.py", "1", nombreArchivoRemoto]
    subprocess.run(comando)


# /////////////////////////////////////////////////////////////////////////////