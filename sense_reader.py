from sense_hat import SenseHat
import time
sense = SenseHat()


def capture_temp():
    temp = sense.get_temperature()
    return temp

def capture_humidity():
    hum = sense.get_humidity()
    return hum
