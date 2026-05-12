from machine import Pin
import utime
from logger import log

rain_guage = Pin(15, Pin.IN, Pin.PULL_UP)
count = 0

def on_change(_pin):
    global count
    count += 1
    log("Rain gauge pulse #{} detected".format(count))


rain_guage.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=on_change)
log("Rain gauge interrupt registered on Pin 15. Sampling for 10s...")
utime.sleep(10)
rain_guage.irq(handler=None)
log("Sampling complete. Total rain gauge count: {}".format(count))
count = 0
log("Rain gauge count reset to 0")
