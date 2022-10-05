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
    GPIO.setup(leds[0], GPIO.OUT)
    GPIO.setup(aux[0], GPIO.OUT)

    p_l = GPIO.PWM(leds[0], 100)
    p_l.start(0)
    p_w = GPIO.PWM(aux[0], 1000)
    p_w.start(0)

    d = input("DAC: ")
    n = input("Diod: ")
    a = input("Not Diod: ")
    while n != 'q' and a != 'q' and d != 'q':
        GPIO.output(dac, inbin(int(d)))
        p_l.ChangeDutyCycle(int(n))
        p_w.ChangeDutyCycle(100 - int(a))
        print("V =", (3.3 / 256 * int(d)) * int(a) / 100, "B")
        n = input("Diod: ")
        a = input("Not Doid: ")

except BaseException:
    if n.isdigit() or (n[:1] == '-' and n[1:].isdigit()):
        if int(n) > 0:
            if int(n) < 100:
                print("Нехороший ты человек (n)")
            else:
                print("Число не должно превышать 100 (n)")
        else:
            print("Нужно положительное целое число (n)")
    else:
        print("Нужно целое число (n)")
    if a.isdigit() or (a[:1] == '-' and a[1:].isdigit()):
        if int(a) > 0:
            if int(a) < 100:
                print("Нехороший ты человек (a)")
            else:
                print("Число не должно превышать 100 (a)")
        else:
            print("Нужно положительное целое число (a)")
    else:
        print("Нужно целое число (a)")
    if d.isdigit() or (d[:1] == '-' and d[1:].isdigit()):
        if int(d) > 0:
            if int(d) < 256:
                print("Нехороший ты человек (d)")
            else:
                print("Число не должно превышать 255 (d)")
        else:
            print("Нужно положительное целое число (d)")
    else:
        print("Нужно целое число (d)")
    

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

