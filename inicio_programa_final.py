#!/usr/bin/env python
import os
import sys
import RPi.GPIO as GPIO
# Botones
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
        GPIO.clear()
        print(sys.path)
        os.system('programa_finalv1.py')



