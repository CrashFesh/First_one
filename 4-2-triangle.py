import RPi.GPIO as GPIO
from time import sleep as sleep

GPIO.setmode(GPIO.BCM)

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
aux = [2, 3, 14, 15, 18, 27, 23, 22]

def inbin(num):
    return [int(i) for i in bin(num)[2:].zfill(8)]

try:
    GPIO.setup(dac, GPIO.OUT)
    n = -1
    flag = True
    T = int(input("T = "))
    while True:
        if flag:
            n += 1
        else:
            n -= 1

        if n == 255:
            flag = False
        if n == 0:
            flag = True

        num_bin = inbin(int(n))

        GPIO.output(dac, num_bin)
        sleep(T / 509)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

