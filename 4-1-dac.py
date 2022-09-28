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
    n = input()
    while n != 'q':
        num_bin = inbin(int(n))

        GPIO.output(dac, num_bin)
        print(3.3 / 256 * int(n))

        n = input()
    print("Конец работы")
except BaseException or ValueError:
    if n.isdigit():
        if int(n) > 0:
            if int(n) < 256:
                print("Нехороший ты человек")
            else:
                print("Число не должно превышать 255")
        else:
            print("Нужно положительное целое число")
    else:
        print("Нужно целое число")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

