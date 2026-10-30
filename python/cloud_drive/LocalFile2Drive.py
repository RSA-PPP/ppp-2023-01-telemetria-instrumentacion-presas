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
import json
#import LogWriter
import logging

# ////////////////////////////////// Metodos //////////////////////////////////

# **********************************************************************
# ************************ importar_json *******************************
# **********************************************************************
# Metodo para leer el archivo de configuracion en formato JSON
def leer_configuracion_json(param1,param2):
    with open('/home/rsa/configuracion/DatosConfiguracion.json', 'r') as config_file:
        configuracion = json.load(config_file)
    return configuracion[param1][param2]
# **********************************************************************
# ******************** Fin Metodo importar_json ************************
# **********************************************************************

# **********************************************************************
# **************** Metodo construir_ruta_archivo ***********************
# **********************************************************************
# Metodo para contruir la ruta del archivo a subir
# Revisa si se ingreso como parametro unicamente el nombre del archivo 
# o la ruta completa del archivo
def construir_ruta_archivo(path_file, nombre_archivo):
    if os.path.isabs(nombre_archivo):
        # Si nombre_archivo contiene la ruta completa
        return os.path.basename(nombre_archivo)
    else:
        # Si nombre_archivo solo contiene el nombre del archivo
        return nombre_archivo
# **********************************************************************
# *************** Fin Metodo construir_ruta_archivo ********************
# **********************************************************************

# **********************************************************************
# ******************* Metodo get_authenticated *************************
# **********************************************************************
# Metodo que permite realizar la autenticacion a Google Drive, para esto
# es necesario tener el archivo credentials.json en la misma carpeta de
# este script. La primera vezse abrira el navegador para realizar la
# autenticacion y se creara el archivo token.json que permite realizar
# directamente la autenticacion desde la segunda vez que se ejecute, sin
# necesidad del navegador
def get_authenticated(SCOPES, credential_file,
                  token_file, service_name = 'drive',
                  api_version = 'v3'):
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage(token_file)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credential_file, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build(service_name, api_version, http = creds.authorize(Http()))

    return service
# **********************************************************************
# ****************** Fin Metodo get_authenticated **********************
# **********************************************************************

# **********************************************************************
# ************************* Metodo insert_file *************************
# **********************************************************************
# Metodo que permite subir un archivo a la cuenta de Drive, no importa
# el tamaño del archivo. Si se desea subir a una carpeta en específico
# se debe colocar el parent_id
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
# **********************************************************************
# *********************** Fin Metodo insert_file ***********************
# **********************************************************************

# **********************************************************************
# Metodo para intentar conectarse a Google Drive y activar la bandera de conexion
# **********************************************************************
def Try_Autenticar_Drive(SCOPES, credential_file, token_file):
    global isConecctedDrive
    # Llama al metodo para realizar la autenticacion, la primera vez se
    # abrira el navegador, pero desde la segunda ya no
    try:
        service = get_authenticated(SCOPES, credential_file, token_file)
        isConecctedDrive = True
        print("Inicio Drive Ok")
        #LogWriter.FileLog("  Inicio Drive Ok")
        logging.info("Inicio Drive Ok")
        return service
    except:
        isConecctedDrive = False
        print("Error Inicio Drive")
        #LogWriter.FileLog("  Error Inicio Drive")
        logging.info("Error Inicio Drive")
        return 0
# **********************************************************************
# Fin del metodo para conectarse a Drive
# **********************************************************************

# /////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////// Principal /////////////////////////////////
if __name__ == '__main__':
                     
    #LogWriter.FileLog("Inicio LocalFile2Drive")

    # Configura el sistema de registro
    logging.basicConfig(filename='/home/rsa/log-files/local_file_2drive.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

    # ///////////////////////////////// Archivos //////////////////////////////////

    #usr = os.environ.get('USER')                        #Obtencion del usuario
    usr = 'rsa'                                          #Obtencion del usuario
    path_base = '/home/'+usr+'/'                        #Ruta Base 

    pathArchivosConfiguracion = path_base+'configuracion/'
    credentialFile = pathArchivosConfiguracion + 'credentials.json'
    tokenFile = pathArchivosConfiguracion + 'token.json'

    carpetaDrive = sys.argv[1] 
    nombreArchivo = sys.argv[2]

    nombreEstacion = leer_configuracion_json("dispositivo","id")
    if carpetaDrive=='1':
        #Archivos recibidos
        pathFile = leer_configuracion_json("directorios","archivosRecibidos")
        driveID = leer_configuracion_json("drive","archivosRecibidos")
    elif carpetaDrive=='2':
        #Archivos resultados vertederos
        pathFile = leer_configuracion_json("directorios","resultadosVertederos")
        driveID = leer_configuracion_json("drive","vertederos")
    elif carpetaDrive=='3':
        #Archivos resultados coordinometros
        pathFile = leer_configuracion_json("directorios","resultadosCoordinometros")
        driveID = leer_configuracion_json("drive","coordinometros")
    elif carpetaDrive=='4':
        #Archivos resultados cajas de edicion
        pathFile = leer_configuracion_json("directorios","resultadosCajasMedicion")
        driveID = leer_configuracion_json("drive","cajasMedicion")

    #nombreArchvioRegistroContinuo = construir_ruta_archivo(pathFile, nombreArchivo)
    pathArchivo = pathFile + nombreArchivo
    logging.info(nombreArchivo)
        
    #service  = 0
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/drive'
	 # Llama al metodo para realizar la autenticacion, la primera vez se
	 # abrira el navegador, pero desde la segunda ya no
	 #service = get_authenticated(SCOPES)
    
    #Llama al metodo para intentar conectarse a Google Drive
    service = Try_Autenticar_Drive(SCOPES, credentialFile, tokenFile)
    
    if isConecctedDrive == True:
        # Llama al metodo para subir el archivo a Google Drive
        try:
            # El metodo tiene este formato: insert_file(service, name, description, parent_id, mime_type, filename)
            #file_uploaded = insert_file(service, nombreArchivo, nombreArchivo, pathDriveID, 'text/x-script.txt', archivoSubir)
            print('Subiendo el archivo: %s' %pathArchivo)
            #LogWriter.FileLog("  Subiendo el archivo: " + pathArchivo)
            logging.info('Subiendo el archivo: %s' % pathArchivo)
            file_uploaded = insert_file(service, nombreArchivo, nombreArchivo, driveID, 'text/plain', pathArchivo)
            print('Archivo ' + nombreArchivo + ' subido correctamente a Google Drive ' )
            #LogWriter.FileLog("  Archivo subido correctamente a Google Drive " + str(file_uploaded))
            logging.info("Archivo subido correctamente a Google Drive. ID: " + str(file_uploaded))
            # Eliminar el archivo local después de subirlo a Google Drive
            os.remove(pathArchivo)
            print('Archivo local eliminado: %s' % pathArchivo)
            logging.info('Archivo local eliminado: %s' % pathArchivo)
        except Exception as e:
            print ('Error subiendo el archivo a Google Drive')
            #LogWriter.FileLog("  Error subiendo el archivo a Google Drive")
            logging.error("Error subiendo el archivo a Google Drive: " + str(e))
# /////////////////////////////////////////////////////////////////////////////
