import datetime
import time
import picamera
import RPi.GPIO as GPIO
import os
import copy
GPIO.setmode(GPIO.BCM)

# PWM
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

# Botones
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)


class ContadorApagado:
    def __init__(self, tiempo_final):
        self.contador = 0
        self.contador_final = tiempo_final*10

    def agregar_counter(self):
        self.contador += 1

    def reset_counter(self):
        self.contador = 0

    @property
    def threshold(self):
        if self.contador == self.contador_final:
            return True
        else:
            return False


class ControlServoBoton:
    def __init__(self, status=False):
        self.status = status

    def cambiio_de_estado(self, estado_boton):
        if estado_boton == self.status:
            return False
        else:
            self.status = estado_boton
            return True

class ControlServoBotonAmarillo:
    def __init__(self, status=False):
        self.status = status

    def cambiio_de_estado(self, estado_boton):
        if estado_boton == self.status:
            return False
        else:
            self.status = estado_boton
            return True





class ControlServo:
    def __init__(self, angulo_inicial=90, limite_dercha=180, limite_izquierda=0, escalon=10):
        self.angulo = angulo_inicial
        self.limite_derecha = limite_dercha
        self.limite_izquierda = limite_izquierda
        self.escalon = escalon

    def inicializacion(self):
        return self.transformar_angulo(90)

    def mover_derecha(self):
        if self.angulo + self.escalon > self.limite_derecha:
            return self.transformar_angulo(self.angulo)

        else:
            self.angulo += self.escalon
            return self.transformar_angulo(self.angulo)

    def mover_izquierda(self):
        if self.angulo - self.escalon < self.limite_izquierda:
            return self.transformar_angulo(self.angulo)

        else:
            self.angulo -= self.escalon
            return self.transformar_angulo(self.angulo)

    @staticmethod
    def transformar_angulo(angulo):
        return float(angulo)/10.0 + 2.5

control_apagado = ContadorApagado(5)

control_servo_treshhold_rojo = ControlServoBoton()
control_servo_treshhold_amarillo = ControlServoBotonAmarillo()
control_servo_treshhold_camara = ControlServoBotonCamara()

control_servo = ControlServo(angulo_inicial=90, limite_dercha=180, limite_izquierda=0, escalon=10)


with picamera.PiCamera() as camera:
    camera.resolution = (600, 600)
    camera.start_preview()

    while True:
        # verde 17/ palanca para arriba

        if GPIO.input(17):
            status = bool(GPIO.input(17))
            if control_servo_treshhold_camara.cambiio_de_estado(status):
                print('sacar foto')
                fehca = str(datetime.datetime.today()) + '.jpg'
                camera.capture('/home/pi/Desktop/tesis/tesis/fotos/' + fehca)
            control_apagado.agregar_counter()
            lista = ['*']*(control_apagado.contador_final - control_apagado.contador)
            barra = ''.join(lista) + '\n'
            print(barra)
            if control_apagado.threshold:
                print('apagar')
                camera.stop_preview()
                break
        else:
            control_apagado.reset_counter()
            control_servo_treshhold_camara.cambiio_de_estado(False)

        # rojo izquierda o derecha
        if GPIO.input(27):
            status = bool(GPIO.input(27))
            if control_servo_treshhold_rojo.cambiio_de_estado(status):
                pwm_salida = control_servo.mover_derecha()
                # pwm.ChangeDutyCycle(pwm_salida)
                print(control_servo.angulo)
                print('mover derecha')
        else:
            control_servo_treshhold_rojo.cambiio_de_estado(False)

        # amarillo izquierda o derecha

        if GPIO.input(22):
            status = bool(GPIO.input(22))
            if control_servo_treshhold_amarillo.cambiio_de_estado(status):
                pwm_salida = control_servo.mover_izquierda()
                # pwm.ChangeDutyCycle(pwm_salida)
                print(control_servo.angulo)
                print('mover izquierda')
        else:
            control_servo_treshhold_amarillo.cambiio_de_estado(False)
        time.sleep(0.1)






