__author__ = 'Jose Miguel'
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#configuracion de pines como entrada
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)
#rutina leera estado entrada constantemente hasta salir del programa
while True:
    print GPIO.input(17)
    print GPIO.input(27)
    print GPIO.input(22)
   #espera medio segundo para leer nuevamente
    time.sleep(0.5)