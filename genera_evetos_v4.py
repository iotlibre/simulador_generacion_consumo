import paho.mqtt.publish as publish
import csv
import os
import sys
import datetime
from time import sleep
import logging
from logging.handlers import RotatingFileHandler

''' Niveles de logging
Para obtener _TODO_ el detalle: level=logging.INFO
Para comprobar los posibles problemas level=logging.WARNINg
Para comprobar el funcionamiento: level=logging.DEBUG
'''
logging.basicConfig(
        level=logging.DEBUG,
        handlers=[RotatingFileHandler('./logs/log_datadis.log', maxBytes=1000000, backupCount=4)],
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')
        



# Variable de mensajes que se ejecutan en modo debug si se cambia a True
# Nombre del archivo de lectura que se pasa como argumento por consola
archivo_lectura = sys.argv[1]

def envioContenido(topic, contenido, hostname = "localhost", user = "", contras = ""):
    # Una vez que la fecha ha pasado de la hora del archivo, 
    # se lleva a cabo el envío de mensajes
    lista = []
    for i in range(len(contenido)):
        lista.append((topic+str(i+1),contenido[i]))
    publicarMQTT( lista, hostname, user, contras)

def publicarMQTT(lista, hostname = "localhost", user = "", contras = ""):
    # Esta función publica los elementos de la lista en el host
    # hacen falta una lista, el hostname, el usuario y la contraseña
    # la lista es un conjunto de tuplas compuestas de la siguiente forma:
    #   lista = [(topic1,mensaje1),(topic2,mensaje2),...]
    # todos en formato strings
    autoriz = { 'username': user, 'password': contras }
    if user == "" and contras == "":
        publish.multiple(lista, hostname = hostname)
    else:
        publish.multiple(lista, hostname = hostname, auth = autoriz)

def soloHora(fecha:str, formato:str):
    # A partir de una variable fecha, diciendo el formato que lleva
    # devuelve las horas, minutos y segundos de esa fecha
    try:
        aux = datetime.datetime.strptime(fecha,formato)
    except:
        aux = datetime.datetime.now()
    horas = aux.hour
    minutos = aux.minute
    segundos = aux.second
    return horas,minutos,segundos

if __name__ == "__main__":
    # Intervalos de tiempo en segundos, minutos y horas entre comprobacion y comprobacion
    intervs = 10
    intervm = 0
    intervh = 0

    # Formatos de fechas
    formato = "%H:%M:%S"
    while True:
        logging.debug(datetime.datetime.now())
        # Directorio del archivo a leer
        direccion = os.path.join(sys.path[0],archivo_lectura)
        with open(direccion, newline='\n') as csvfile:
            # Se resetea la fecha de inicio del programa
            fechaActual = datetime.datetime.now()
            # Se abre el archivo con la librería csv
            spamreader = csv.reader(csvfile, delimiter=',')
            #Bucle de lectura del archivo en el que se lee cada fila del archivo csv
            for row in spamreader:
                # De la columna primera se saca el tiempo horario
                horas,minutos,segundos = soloHora(row[0],formato)
                # Se copia la hora del archivo el dia de la fecha de inicio del programa
                ahoraArch = datetime.datetime(fechaActual.year,fechaActual.month,fechaActual.day,horas,minutos,segundos)
                # Mientras la fecha del programa sea menor que la fecha del archivo
                while fechaActual < ahoraArch:
                    # Se añade un incremento de tiempo a la fecha y se duerme en cada iteración
                    sleep(intervs)
                    fechaActual = datetime.datetime.now()
                
                envioContenido('63a77c6c080db2bb/simulador/valores', row, "localhost", "iotlibre", "EeFfSytg33")

                logging.debug("Se ha mandado el mensaje de las: ")
                logging.debug(ahoraArch.__format__(formato))

            sleep(61)
