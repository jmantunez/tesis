#!/usr/bin/env python
import os
import sys
import RPi.GPIO as GPIO
# Botones
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)


class ControlServoBotonCamara:
    def __init__(self, status=False):
        self.status = status

    def cambiio_de_estado(self, estado_boton):
        if estado_boton == self.status:
            return False
        else:
            self.status = estado_boton
            return True

while True:
    if GPIO.input(17):
        status = bool(GPIO.input(17))
        GPIO.cleanup()
        print(sys.path)
        os.system('python ' + '/home/pi/Desktop/tesis/tesis/programa_finalv1.py')
        GPIO.setup(17, GPIO.IN)


