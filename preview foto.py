__author__ = 'Jose Miguel'
#Se importan las librerias correspondientes
import time
import picamera

#agregar comentarios
camera = picamera.PiCamera()
try:
    camera.start_preview()
    time.sleep(10)
    camera.stop_preview()
finally:
    camera.close()
