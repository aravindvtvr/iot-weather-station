from machine import Pin
import utime
from logger import log

_pulses = 0

def _count(_pin):
    global _pulses
    _pulses += 1


def read_windspeed(pin_number=16, sample_duration_s=10):
    global _pulses
    _pulses = 0
    log("Wind sensor: setting up IRQ on pin {} for {}s sample".format(pin_number, sample_duration_s))

    wind_sensor = Pin(pin_number, Pin.IN, Pin.PULL_UP)
    wind_sensor.irq(trigger=Pin.IRQ_FALLING, handler=_count)
    log("Wind sensor IRQ registered. Sampling...")

    utime.sleep(sample_duration_s)
    wind_sensor.irq(handler=None)

    log("Sampling complete. Pulse count: {}".format(_pulses))
    rpm = _pulses * (60 / sample_duration_s)
    log("Wind speed: {} pulses -> {:.2f} RPM".format(_pulses, rpm))
    _pulses = 0
    return rpm
