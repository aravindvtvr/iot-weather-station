import time
from machine import Pin
from anemometer import read_windspeed
from connect_basestation import connect_basestation
from temperature_sensor import read_temperature
from logger import log
import config

MAIN_SLEEP = config.MAIN_SLEEP
sample_duration_s = config.WINDSPEED_SAMPLING_SIZE
rain_guage = Pin(15, Pin.IN, Pin.PULL_UP)
rainguage_count = 0

log("=== Weather Station Starting ===")
log("Config: MAIN_SLEEP={}s, LOG_ENABLED={}, LOG_FILE={}".format(
    config.MAIN_SLEEP, config.LOG_ENABLED, config.LOG_FILE))


def get_vsys():
    import machine
    vsys = machine.ADC(29)
    conversion_factor = (3.3 / 65535) * 3
    raw = vsys.read_u16()
    voltage = raw * conversion_factor
    log("vsys raw={}, conversion_factor={:.6f}, voltage={:.3f}V".format(
        raw, conversion_factor, voltage))
    return voltage


time.sleep(5)

def on_raingauge_change(_pin):
    global rainguage_count
    rainguage_count += 1
    log("Rain gauge pulse #{} detected".format(rainguage_count))

# Setup the rain gauge interrupt
rain_guage.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=on_raingauge_change)
log("Rain gauge interrupt registered on Pin 15")


cycle = 0
while True:
    cycle += 1
    log("=== Reading cycle #{} (MAIN_SLEEP={}s) ===".format(cycle, MAIN_SLEEP))

    log("Reading wind speed (pin=16, sample_duration={}s)...".format(sample_duration_s))
    rpm = read_windspeed(pin_number=16, sample_duration_s=sample_duration_s)
    log("Wind speed result: {:.2f} RPM".format(rpm))

    log("Reading temperature/pressure/humidity...")
    temperature, pressure, humidity = read_temperature()
    log("Sensor readings: temp={}, pressure={}, humidity={}".format(
        temperature, pressure, humidity))

    log("Reading battery voltage...")
    battery_voltage = get_vsys()
    log("Battery voltage: {:.3f}V".format(battery_voltage))

    log("Rain gauge count this cycle: {}".format(rainguage_count))

    log("Connecting to base station...")
    MAIN_SLEEP, sample_duration_s = connect_basestation(
        battery_voltage, rpm, MAIN_SLEEP,
        temperature, pressure, humidity, rainguage_count,
        sample_duration_s
    )
    rainguage_count = 0
    log("Rain gauge count reset to 0")

    log("Cycle #{} complete. Sleeping for {}s".format(cycle, MAIN_SLEEP))
    time.sleep(MAIN_SLEEP)
