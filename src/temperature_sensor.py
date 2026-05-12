import machine
import bme280
from logger import log

log("Initializing I2C bus 0 (SDA=Pin4, SCL=Pin5)...")
_i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))

log("Scanning I2C bus for devices...")
devices = _i2c.scan()
log("I2C devices found: {}".format([hex(d) for d in devices]))

log("Initializing BME280 at I2C address 0x76...")
_bme = bme280.BME280(i2c=_i2c, address=0x76)
log("BME280 initialized")


def read_temperature():
    log("Reading BME280 sensor values...")
    try:
        temperature, pressure, humidity = _bme.values
        log("BME280 raw: temp={}, pressure={}, humidity={}".format(
            temperature, pressure, humidity))
        return temperature, pressure, humidity
    except Exception as e:
        log("BME280 read error: {} - {}".format(type(e).__name__, e))
        raise
