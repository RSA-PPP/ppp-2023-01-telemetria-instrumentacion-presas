########################################## ~ LIBRERIAS ~ ###############################################
from __future__ import print_function
from googleapiclient import errors
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
from datetime import datetime
import time
import sys 
import subprocess
import json
########################################################################################################
usr = os.environ.get('USER')                        #Obtencion del usuario
path_base = '/home/'+usr+'/'                        #Ruta Base 
pathArchivosConfiguracion = path_base+'configuracion/'
pathNombresArchvivosRC = path_base+'tmp/'
pathLogFiles = path_base+'log-files/'
archivoDatosConfiguracion = pathArchivosConfiguracion + 'DatosConfiguracion.txt'
archivoNombresArchivosRC = pathNombresArchvivosRC + 'NombreArchivoRegistroContinuo.tmp'

credentialsFile = pathArchivosConfiguracion + 'credentials.json'
tokenFile = pathArchivosConfiguracion + 'token.json'
########################################## ~ FUNCIONES ~ ############################################### 
# Funcion: Ejecucion del comando scp rsa@__:/home/rsa/prueba/archivo___.txt 
def consola(lista):
    arch = []
    usr = os.environ.get('USER')
    conta = 0
    for k1 in lista:
        op = lista[conta]
        returned_output = subprocess.call('scp '+op+':/home/pi/resultados/'+op+'.txt '+'/home/'+usr+'/archivos-recibidos/',shell = True) 
        if returned_output == 0:
            print("\t >Coordinómetro " + op + " disponible\n")
            arch.append(k1+'.txt')
        else:
            print("\t >Coordinómetro " + op + " no disponible\n")
        conta = conta+1
    return arch

def importar_json(param1,param2):
    # Abre y lee el archivo JSON de configuración
    with open('/home/pasante1/configuracion/DatosConfiguracion.json', 'r') as config_file:
        configuracion = json.load(config_file)
    return configuracion[param1][param2]

# Funcion: Subir el archivo a drive
def subirArchivo(nameFile):
    # Directorios y archivos  
    nombreEstacion = importar_json("dispositivo","id")
    pathFile = importar_json("directorios","archivosRecibidos")
    driveID = importar_json("drive","coordinometro")
    nombreArchvioRegistroContinuo = construir_ruta_archivo(pathFile,nameFile)
    pathArchivoRegistroContinuo = pathFile + nombreArchvioRegistroContinuo
    if __name__ == '__main__':

        SCOPES = 'https://www.googleapis.com/auth/drive'
        fechaActual = datetime.now()
        fechaFormato = fechaActual.strftime('%Y-%m-%d') 
                
        ficheroConfiguracion = open(archivoDatosConfiguracion)
            
        lineasFicheroConfiguracion = ficheroConfiguracion.readlines()
            
        #nombreArchvioRegistroContinuo = sys.argv[1]
        print(nombreArchvioRegistroContinuo)
        #Subir evento extraido:
        #Subir archivo registro continuo:
        #pathArchivoRegistroContinuo = pathFile + nombreArchvioRegistroContinuo
            
        # Crea el archivo para almacenar los logs del proyectos, que eventos ocurren
        objLogFile = pathLogFiles + 'Log' + nombreEstacion + fechaFormato + '.txt'
        # Llama al metodo para crear un nuevo archivo log
        #guardarDataInLogFile ("Inicio")
        #Llama al metodo para intentar conectarse a Google Drive
        service = Try_Autenticar_Drive(SCOPES,objLogFile)
        if isConecctedDrive == True:
            # Llama al metodo para subir el archivo a Google Drive
            try:
                # El metodo tiene este formato: insert_file(service, name, description, parent_id, mime_type, filename)
                #file_uploaded = insert_file(service, nombreArchivo, nombreArchivo, pathDriveID, 'text/x-script.txt', archivoSubir)
                print('Subiendo el archivo: %s' %pathArchivoRegistroContinuo)
                guardarDataInLogFile ("Subiendo el archivo: " + nombreArchvioRegistroContinuo,objLogFile)
                file_uploaded = insert_file(service, nombreArchvioRegistroContinuo, nombreArchvioRegistroContinuo, driveID, 'text/plain', pathArchivoRegistroContinuo)
                guardarDataInLogFile ("Archivo subido correctamente a Google Drive " + str(file_uploaded),objLogFile)
                print('Archivo ' + nombreArchvioRegistroContinuo + ' subido correctamente a Google Drive ' )
                # Eliminar el archivo local después de subirlo a Google Drive
                os.remove(pathArchivoRegistroContinuo)
                print('Archivo local eliminado: %s' % pathArchivoRegistroContinuo)
            except:
                # Llama al metodo para guardar el evento ocurrido en el archivo
                guardarDataInLogFile ("Error subiendo el archivo a Google Drive",objLogFile)
                print ('Error subiendo el archivo a Google Drive')
# Funcion: Ruta del Archivo
def construir_ruta_archivo(path_file, nombre_archivo):
    if os.path.isabs(nombre_archivo):
        # Si nombre_archivo contiene la ruta completa
        return os.path.basename(nombre_archivo)
    else:
        # Si nombre_archivo solo contiene el nombre del archivo
        return nombre_archivo

# Funcion: Autenticación 
def get_authenticated(SCOPES, credential_file = credentialsFile,
                  token_file = tokenFile, service_name = 'drive',
                  api_version = 'v3'):
    store = file.Storage(token_file)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credential_file, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build(service_name, api_version, http = creds.authorize(Http()))
    return service

#Funcion: Método Insert File
def insert_file(service, name, description, parent_id, mime_type, filename):
    """Insert new file.
    Args:
        service: Drive API service instance.
        name: Name of the file to insert, including the extension.
        description: Description of the file to insert.
        parent_id: Parent folder's ID.
        mime_type: MIME type of the file to insert.
        filename: Filename of the file to insert.
    Returns:
        Inserted file metadata if successful, None otherwise.
    """
    media_body = MediaFileUpload(filename, mimetype = mime_type, chunksize=-1, resumable = True)
    body = {
        'name': name,
        'description': description,
        'mimeType': mime_type
    }
        
    # Si se recibe la ID de la carpeta superior, la coloca
    if parent_id:
        body['parents'] = [parent_id]

    # Realiza la carga del archivo en la carpeta respectiva de Drive
    try:
        #print("punto de control")
        file = service.files().create(
            body = body,
            media_body = media_body,
            fields='id').execute()
            
        return file
            
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None

# Funcion:  Metodo para intentar conectarse a Google Drive y activar la bandera de conexion 
def Try_Autenticar_Drive(SCOPES,filelog):
    global isConecctedDrive
    # Llama al metodo para realizar la autenticacion, la primera vez se
    # abrira el navegador, pero desde la segunda ya no
    try:
        service = get_authenticated(SCOPES)
        isConecctedDrive = True
        print("Inicio Drive Ok")
        guardarDataInLogFile ("Inicio Drive Ok",filelog)
        return service
    except:
        isConecctedDrive = False
        print("********** Error Inicio Drive ********")
        guardarDataInLogFile ("Error Inicio Drive",filelog)
        return 0

# Funcion: Método para guardar archivo LogFile 
def guardarDataInLogFile (info,objLogFile):
    timeActual = datetime.now()
    timeFormato = timeActual.strftime('%Y-%m-%d %H:%M:%S')
    # Abre o crea el nuevo archivo de texto y en formato para escribir
    archivo = open(objLogFile, "a")
    archivo.write((timeFormato + "\t" + info + "\n"))
    archivo.close()

################################################################################################

####################################### ~ MAIN ~ ###############################################
# 
lista = ('IZQ-N1-X','IZQ-N1-Y','IZQ-N2-X','IZQ-N2-Y','IZQ-N3-X','IZQ-N3-Y','DER-N1-X','DER-N1-Y','DER-N2-X','DER-N2-Y','DER-N3-X','DER-N3-Y')
arch = consola(lista)
for k1 in arch:
    subirArchivo(k1)