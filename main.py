__author__ = "Julian Kirchner"

from asyncio import get_event_loop, run  # type: ignore

from config import CONFIG
from lib.led import Leds
from lib.modes import error
from lib.thread import Thread
from lib.ultra_sonic import Sensor
from lib.web import run_server
from lib.wifi import connect_to_wlan


async def main() -> None:
    led_strips: list[Leds] = [Leds(strip['num_leds'], strip['pin']) for strip in CONFIG['led_strips']]
    sensor = Sensor(CONFIG['sensor']['trigger_pin'], CONFIG['sensor']['echo_pin'])
    loop = get_event_loop()

    blink_task = Thread(loop, error, led_strips)
    blink_task.start()

    await connect_to_wlan(CONFIG['network']['ssid'], CONFIG['network']['password'])

    blink_task.cancel()
    run_server(loop, led_strips, sensor)


if __name__ == '__main__':
    run(main())
