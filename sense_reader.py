from sense_hat import SenseHat
import time
sense = SenseHat()


def capture_env():
    temp = sense.get_temperature()
    return temp
