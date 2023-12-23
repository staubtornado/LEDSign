__author__ = "Julian Kirchner"

from config import CONFIG
from lib.colors import Color
from lib.led import Leds
from lib.ultra_sonic import Sensor

try:
     from thonny.plugins.micropython.base_api_stubs.uasyncio import sleep_ms
except ImportError:
    from uasyncio import sleep_ms


def main():
    sensor: Sensor = Sensor(CONFIG['sensor']['trigger_pin'], CONFIG['sensor']['echo_pin'])
    led_strips: list[Leds] = [Leds(strip['num_leds'], strip['pin']) for strip in CONFIG['led_strips']]

    while True:
        distance: int = int(sensor.read())

        if distance < 5:
            for led_strip in led_strips:
                    led_strip.set_all(Color.off(), step_size=CONFIG['transition_step_size'])
            sleep_ms(100)
            continue

        if distance == CONFIG['max_distance']:
            continue

        hue: int = int(distance / CONFIG['max_distance'] * 360)
        color: Color = Color.from_hsv(hue, 1, 1)
        for led_strip in led_strips:
            led_strip.set_all(color, step_size=CONFIG['transition_step_size'])


if __name__ == '__main__':
    main()
