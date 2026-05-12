# DIY IoT Weather Station

A MicroPython-based weather station that reads environmental sensors and reports data to a local Node-RED server over WiFi.

## Features

- Wind speed measurement via Hall effect sensor (interrupt-driven)
- Rain gauge measurement via Hall effect sensor (state-change counting)
- Temperature & humidity via BME280 (I2C)
- Battery voltage monitoring
- Reports to a Node-RED base station over HTTP
- Configurable sleep interval retrieved from the server

## Hardware

| Component | Description |
|-----------|-------------|
| Microcontroller | Raspberry Pi Pico W (or similar MicroPython board) |
| Wind sensor | Hall effect sensor on GPIO 16 |
| Rain gauge | Hall effect sensor on GPIO 15 |
| Temp/Humidity | BME280 on I2C0 (SDA: GPIO 4, SCL: GPIO 5) |
| Battery monitor | ADC pin 29 (Vsys) |

## Project Structure

```
├── src/                    # Deploy these files to the device
│   ├── main.py             # Main application loop
│   ├── read_windspeed.py   # Wind speed sensor module
│   ├── read_rainguage.py   # Rain gauge sensor module
│   ├── config.py           # Your credentials (gitignored)
│   └── config_example.py   # Credential template (safe to commit)
├── lib/                    # Third-party MicroPython libraries
│   └── bme280.py           # BME280 driver (add manually)
├── tests/                  # Standalone test/bench scripts
│   ├── test_wifi.py
│   └── test_temp.py
├── docs/                   # Additional documentation
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/iot-weather-station.git
cd iot-weather-station
```

### 2. Configure credentials

```bash
cp src/config_example.py src/config.py
```

Edit `src/config.py` with your WiFi credentials and Node-RED server address. This file is gitignored and will never be committed.

### 3. Install MicroPython libraries

Download the `bme280.py` driver and place it in `lib/`. A compatible driver can be found at [micropython-bme280](https://github.com/robert-hh/BME280).

### 4. Deploy to device

Using [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) or [Thonny](https://thonny.org/):

```bash
# Copy all source files
mpremote cp src/main.py :main.py
mpremote cp src/config.py :config.py
mpremote cp src/read_windspeed.py :read_windspeed.py
mpremote cp src/read_rainguage.py :read_rainguage.py
mpremote cp lib/bme280.py :bme280.py
```

### 5. Node-RED setup

The device expects two endpoints on your Node-RED server:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/endpoint/wstn/config` | GET | Returns a `main_sleep` response header (seconds) |
| `/endpoint/wstn/readings` | POST | Receives JSON: `{ temp, humidity, volts }` |

## Configuration Reference (`config.py`)

| Key | Description |
|-----|-------------|
| `WIFI_SSID` | WiFi network name |
| `WIFI_PASSWORD` | WiFi password |
| `SERVER_BASE_URL` | Base URL of your Node-RED instance |
| `MAIN_SLEEP` | Default sleep interval in seconds (overridden by server) |

## License

MIT — see [LICENSE](LICENSE).
