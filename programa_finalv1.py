import datetime
import time
import picamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# PWM
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

# Botones
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()

    while True:
        if GPIO.input(17):
            fehca = str(datetime.datetime.today())
            camera.capture(fehca)
        if GPIO.input(27):
            print('mover a algun lado')
        time.sleep(0.1)