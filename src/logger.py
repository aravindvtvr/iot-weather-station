import utime
import config


def log(msg):
    if not config.LOG_ENABLED:
        return
    try:
        ts = utime.ticks_ms()
        line = "[{}ms] {}".format(ts, msg)
        if config.LOG_TO_FILE:
            with open(config.LOG_FILE, "a") as f:
                f.write(line + "\n")
        else:
            print(line)
    except Exception:
        pass  # Silently ignore log failures on device
