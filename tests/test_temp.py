import machine
import bme280

# Initialize I2C (using GPIO 4 and 5)
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))

# Initialize Sensor (Default I2C address is usually 0x76)
bme = bme280.BME280(i2c=i2c, address=0x76)

# Read values
print(bme.values)
