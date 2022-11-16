import spidev
import matplotlib.pyplot as plt

spi = spedev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1600000


def getAdc():
    adcResponce = spi.xfer2([0, 0])
    return ((adcResponce[0] & 0x1F) << 8 | adcResponce[1]) >> 1


try:
    samples = []

    for i in range(20000):
        samples.append(getAdc())

    plt.plot(samples)
    plt.show()


finally:
    spi.close()