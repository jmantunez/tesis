import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

while True:
    try:
        for angulo in range(0, 180):
	    angulo = float(angulo)/10.0 + 2.5
	    print angulo
	    pwm.ChangeDutyCycle(angulo)
	    time.sleep(0.1)

        for angulo in range(180, 0, -1):
	    angulo = float(angulo)/10.0 + 2.5
	    print angulo
            pwm.ChangeDutyCycle(angulo)
	    time.sleep(0.1)
    except KeyboardInterrupt:
	angulo = 45
	pwm.ChangeDutyCycle(angulo)
	print 'chaoooooooooooo' 
	sys.exit(0)
