'''
Programa principal, tiene el control de los botones, servo y camaara
'''
import datetime
import time
import picamera
import RPi.GPIO as GPIO
import os
import copy
'''
setea los pines en modo BCM y los declara como entrada para los botones y el pwm de salida
'''
GPIO.setmode(GPIO.BCM)

# PWM
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

# Botones
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)


'''
Se crea el objeto contador apagado, controla el mantener presionado el boton durante
cierto tiempo hasta que llega al threshold y sale del ciclo principal
'''
class ContadorApagado:

    def __init__(self, tiempo_final):
        '''
        constructor, que agrega las variables inciales al objeto, contador y tiempo final
        :param tiempo_final: tiempo que quiero que salga el programa
        :return: None
        '''
        self.contador = 0
        self.contador_final = tiempo_final*10

    def agregar_counter(self):
        '''
        se suma uno al contaddor cada vez que se llame
        :return:
        '''
        self.contador += 1

    def reset_counter(self):
        '''
        cuandos se deja de apretar el boton, el contador se reinicia
        :return:
        '''
        self.contador = 0

    @property
    def threshold(self):
        '''
        si el contador final es igual al contador, este retorna la senal de apagado
        :return: retorna si debe salir o no en True o False
        '''
        if self.contador == self.contador_final:
            return True
        else:
            return False


class ControlServoBoton:
    '''
    objeto que controla el cambio de estado, si se mantiene apretado el boton retorna falso
    en caso de haber cambio retorna verdadero
    '''
    def __init__(self, status=False):
        '''
        en primera instancia el estado es False
        :param status: estado inicial
        :return: None
        '''
        self.status = status

    def cambiio_de_estado(self, estado_boton):
        '''
        determina si hay cambiuo de estado, se le entrega el estado actual y retorna True
        si hay cambio de estado, en caso contrario falso
        :param estado_boton:
        :return:
        '''
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


class ControlServoBotonCamara:
    def __init__(self, status=False):
        self.status = status

    def cambiio_de_estado(self, estado_boton):
        if estado_boton == self.status:
            return False
        else:
            self.status = estado_boton
            return True



class ControlServo:
    '''
    controla los servos, determina cuando se debe mover
    '''
    def __init__(self, angulo_inicial=90, limite_dercha=180, limite_izquierda=0, escalon=10):
        '''
        inicializa las configuraciones de los movimientos
        :param angulo_inicial: el angulo inicial cuando parte el proceso
        :param limite_dercha: limite superior a la derecha
        :param limite_izquierda: limite inferior a la izquierda
        :param escalon: saltos cada vez que se aprieta el boton
        :return:
        '''
        self.angulo = angulo_inicial
        self.limite_derecha = limite_dercha
        self.limite_izquierda = limite_izquierda
        self.escalon = escalon

    def inicializacion(self):
        '''
        inicializa la posicion del servo a 90 grados
        :return:
        '''
        return self.transformar_angulo(90)

    def mover_derecha(self):
        '''
        mueve la referencia del servo a la derecha
        :return:
        '''
        if self.angulo + self.escalon > self.limite_derecha:
            return self.transformar_angulo(self.angulo)

        else:
            self.angulo += self.escalon
            return self.transformar_angulo(self.angulo)

    def mover_izquierda(self):
        '''
        mueve la referencia del servo a la izquierda
        :return:
        '''
        if self.angulo - self.escalon < self.limite_izquierda:
            return self.transformar_angulo(self.angulo)

        else:
            self.angulo -= self.escalon
            return self.transformar_angulo(self.angulo)

    @staticmethod
    def transformar_angulo(angulo):
        '''
        transformacion lineal de angulo a pwm
        :param angulo:
        :return:
        '''
        return float(angulo)/10.0 + 2.5

'''
configura los objetos para los botones, el control de apagado, y la salida del cicli principal

'''
control_apagado = ContadorApagado(5)

control_servo_treshhold_rojo = ControlServoBoton()
control_servo_treshhold_amarillo = ControlServoBotonAmarillo()
control_servo_treshhold_camara = ControlServoBotonCamara()

control_servo = ControlServo(angulo_inicial=90, limite_dercha=180, limite_izquierda=0, escalon=10)

'''
ciclo principal
'''
with picamera.PiCamera() as camera:
    camera.resolution = (600, 600)
    camera.start_preview()

    while True:
        # verde 17/ palanca para arriba
        # revisa si el boton esta presionado
        if GPIO.input(17):
            # guarda el estatus del boton a la variable status
            status = bool(GPIO.input(17))
            # si hay cambio de estado saca foto
            if control_servo_treshhold_camara.cambiio_de_estado(status):
                print('sacar foto')
                fehca = str(datetime.datetime.today()) + '.jpg'
                camera.capture('/home/pi/Desktop/tesis/tesis/fotos/' + fehca)
            # si no hay cambio de estado se agrega el counter y se imprime la barra
            # de tiempo restante
            control_apagado.agregar_counter()
            lista = ['*']*(control_apagado.contador_final - control_apagado.contador)
            barra = ''.join(lista) + '\n'
            print(barra)
            if control_apagado.threshold:
                # si el contador llega a su final el programa se sale deteniendo el preview
                # y haciendo un break
                print('apagar')
                camera.stop_preview()
                break
        else:
            # resetea el contador de apagado
            control_apagado.reset_counter()
            # cambia el estado actual de la camaara a falso
            control_servo_treshhold_camara.cambiio_de_estado(False)

        # rojo izquierda o derecha
        # revisa si el boton rojo esta presionad
        if GPIO.input(27):
            # guarda la variable del estado del boton en estatus
            status = bool(GPIO.input(27))
            if control_servo_treshhold_rojo.cambiio_de_estado(status):
                # si hay camnbio de estado manda la orden del pwm
                pwm_salida = control_servo.mover_derecha()
                pwm.ChangeDutyCycle(pwm_salida)
                print(control_servo.angulo)
                print('mover derecha')
        else:
            # si de deja de presionar el boton cambioa el estado a falso
            control_servo_treshhold_rojo.cambiio_de_estado(False)

        # amarillo izquierda o derecha

        if GPIO.input(22):
            status = bool(GPIO.input(22))
            if control_servo_treshhold_amarillo.cambiio_de_estado(status):
                pwm_salida = control_servo.mover_izquierda()
                pwm.ChangeDutyCycle(pwm_salida)
                print(control_servo.angulo)
                print('mover izquierda')
        else:
            control_servo_treshhold_amarillo.cambiio_de_estado(False)
        time.sleep(0.1)






