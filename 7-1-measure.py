import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
from time import sleep as sleep
from time import time as time

GPIO.setmode(GPIO.BCM)

filename = "points.txt"

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
aux = [2, 3, 14, 15, 18, 27, 23, 22]
comp = 4
troyka = 17

max_volt = 3.3
delt_volt = max_volt / 256
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

    file = open(filename, "w")

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

    file.close()
    file = open(filename, "r")
    results = file.read().split()

    x = list()
    y = list()
    x_num = list()
    y_num = list()

    for i in range(0, len(results), 2):
        y.append(float(results[i]) * max_volt / 256)
        y_num.append(int(results[i]))
        x.append(float(results[i + 1]))
        x_num.append(i / 2)

    fig, ax = plt.subplots()

    T = time_endend / len(x_num)
    delt_time = 1 / T

    ax.plot(x_num, y_num, linewidth=2.0)
    ax.set_xlim(0, len(x_num) + 5)
    ax.set_ylim(0, 260)
    ax.set_xlabel('Number of checks')
    ax.set_ylabel('ADC number')

    plt.show()

finally:
    print('\n Time should be:', time_need, 'Time 1 had:', time_end - time_start, 'Time 2 had:', time_endend - time_end)
    print('Delt_time =', delt_time, 'Period =', T, 'Delt_volt =', delt_volt)
    GPIO.output(troyka, 0)
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()
    