__author__ = 'Jose Miguel'
#!usr/bin/env/ python
#parpadea.py
#importamos la libreria GPIO
import RPi.GPIO as GPIO
#Importamos la libreria time
import time
#Definimos el modo BCM
GPIO.setmode(GPIO.BCM)
#Ahora definimos el pin GPIO 17 como salida
GPIO.setup(17, GPIO.OUT)
#Queremos que lo que contenga el for i in range se repita 5 veces
for i in range(0,10):
    # Asignamos valor logico alto para encenderlo
    GPIO.output(17, GPIO.HIGH)
    # Esperamos un segundo
    time.sleep(1)
    # Asignamos valor logico bajo para apagarlo
    GPIO.output(17, GPIO.LOW)
    # Esperamos un segundo
    time.sleep(1)
#Una vez termina las 5 repeticiones, liberamos el pin GPIO utilizado; en este caso el 17
GPIO.cleanup()
