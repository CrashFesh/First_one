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
    r = 256
    left = 0
    md = (r + left) // 2
    while (r - left) > 1:
        GPIO.output(dac, inbin(md))
        sleep(0.001)
        compVal = GPIO.input(comp)
        if compVal == 0:
            r = md
        else:
            left = md
        md = (r + left) // 2
    
    volt = max_volt * left / (2**len(dac))
    print("Value:", left, "Volts: {:.4f} V".format(volt))


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