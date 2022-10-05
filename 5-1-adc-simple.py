import RPi.GPIO as GPIO
from time import sleep as sleep

GPIO.setmode(GPIO.BCM)

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
aux = [2, 3, 14, 15, 18, 27, 23, 22]
comp = 4
troyka = 17

max_volt = 3.3

def inbin(num):
    return [int(i) for i in bin(num)[2:].zfill(8)]

def adc():
    for num in range(256):
        GPIO.output(dac, inbin(num))
        volt = max_volt * num / (2**len(dac))
        sleep(0.0005)
        if GPIO.input(comp) == 0:
            print("Value:", num, "Volts: {:4f} V".format(volt))
            break


try:
    GPIO.setup(dac, GPIO.OUT)
    GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(comp, GPIO.IN)
    
    while True:
        adc()



finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()