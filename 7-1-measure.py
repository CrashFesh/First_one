import RPi.GPIO as GPIO
from time import sleep as sleep
from time import time as time

GPIO.setmode(GPIO.BCM)

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
aux = [2, 3, 14, 15, 18, 27, 23, 22]
comp = 4
troyka = 17

file = open("points.txt", "w")

max_volt = 3.3
tau = 10
mx = 237
mn = 9 

time_need = 3.5  * tau


def inbin(num):
    return [int(i) for i in bin(num)[2:].zfill(8)]

def adc():
    r = 256
    left = 0
    md = (r + left) // 2
    while (r - left) > 1:
        GPIO.output(dac, inbin(md))
        sleep(0.0007)
        compVal = GPIO.input(comp)
        if compVal == 0:
            r = md
        else:
            left = md
        md = (r + left) // 2
    
    volt = max_volt * left / 256
    print("Value:", left, "Volts: {:.4f} V".format(volt))
    return left

def adc_simple():
    for num in range(256):
        GPIO.output(dac, inbin(num))
        volt = max_volt * num / (2**len(dac))
        sleep(0.0005)
        if GPIO.input(comp) == 0:
            print("Value:", num, "Volts: {:4f} V".format(volt))
            return num
    return 0

def volt_in_leds(num):
    GPIO.output(leds, inbin(num))

try:
    GPIO.setup(dac, GPIO.OUT)
    GPIO.setup(leds, GPIO.OUT)
    GPIO.setup(troyka, GPIO.OUT)
    GPIO.setup(comp, GPIO.IN)

    GPIO.output(troyka, 1)
    time_start = time()
    time_end = 0
    time_endend = 0
    while True:
        n = adc()
        time_now = time()
        if (n > mx):
            GPIO.output(troyka, 0)
            time_end = time()
            sleep(0.01)
            break
        volt_in_leds(n)
        file.write(f'{n} {time_now - time_start}\n')
        sleep(0.01)

    while True:
        n = adc()
        if (n < mn):
            time_endend = time()
            break
        volt_in_leds(n)
        file.write(f'{n} {time_now - time_start}\n')
        sleep(0.01)
finally:
    print('\n Time should be:', time_need, 'Time 1 had:', time_end - time_start, 'Time 2 had:', time_endend - time_end)
    GPIO.output(troyka, 0)
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()
    