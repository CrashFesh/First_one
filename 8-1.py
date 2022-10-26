import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np

try:
    fdata = open("data.txt", "r")
    fsett = open("settings.txt", "r")
    sett = fsett.read().split()
    delt_volt = float(sett[0])
    delt_time = float(sett[1])
    print(delt_volt)
    print(delt_time)

    y_num = list()
    for i in fdata.read().split():
        y_num.append(int(i))
    
    y = list()
    for i in y_num:
        y.append(y_num[i] * delt_volt)
    
    x = np.linspace(0, len(y) * delt_time, len(y))

    fig, ax = plt.subplots()

    y_mark = list()
    x_mark = list()
    for i in range(0, len(y), 50):
        y_mark.append(y[i])
        x_mark.append(i * delt_time)
    
    
    ax.set_title('Процесс заряда и разряда конденсатора')
    ax.set_ylabel('V, volts')
    ax.set_xlabel('t, seconds')
    ax.annotate('Time_1 = 4.23\nTime_2 = 5.35', (7.8, 2.1))

    ax.set_ylim(0, max(y) + 0.2)
    ax.set_xlim(0, max(x) + 1)
    ax.grid(which='major')
    ax.grid(which='minor', color='grey', linestyle='-', alpha=0.1)
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))

    ax.plot(x, y, color='#7f7f7f', label='V(t)')
    ax.scatter(x_mark, y_mark)
    ax.legend()
    plt.show()
    plt.savefig("asd.svg")

finally:
    fdata.close()
    fsett.close()