__author__ = 'Jose Miguel'
#importar libreria GPIO
import RPi.GPIO as GPIO
#Importar libreria time
import time
#Definir modo BCM
GPIO.setmode(GPIO.BCM)
#Definicion del pin GPIO 17 como salida
GPIO.setup(17, GPIO.OUT)

#La instruccion contenida en el for i in range se repetira 10 veces
for i in range(0,10):
    # Se asigna valor logico alto para encenderlo
    GPIO.output(17, GPIO.HIGH)
    # Tiempo de espera
    time.sleep(1)
    # Se asigna valor logico bajo para apagarlo
    GPIO.output(17, GPIO.LOW)
    # Tiempo de espera
    time.sleep(1)

#Terminadas las 10 repeticiones, se libera el pin GPIO 17
GPIO.cleanup()
