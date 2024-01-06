__author__ = "Julian Kirchner"

from config import CONFIG

try:
    from thonny.plugins.micropython.base_api_stubs.utime import sleep_us, ticks_us
    from thonny.plugins.micropython.base_api_stubs.machine import Pin
except ImportError:
    from time import sleep_us, ticks_us  # type: ignore
    from machine import Pin  # type: ignore


class Sensor:
    def __init__(self, trigger_pin: int, echo_pin: int) -> None:
        self._trigger = Pin(trigger_pin, Pin.OUT)
        self._echo = Pin(echo_pin, Pin.IN)

    def read(self) -> float:
        """
        Reads the distance from the sensor.

        :return: the distance in cm.
        """

        self._trigger.value(0)
        sleep_us(2)
        self._trigger.value(1)
        sleep_us(10)
        self._trigger.value(0)
        while self._echo.value() == 0:
            pass
        start = ticks_us()
        while self._echo.value() == 1:
            pass
        end = ticks_us()
        return min((end - start) / 58, CONFIG['sensor']['max_distance'])  # type: ignore
