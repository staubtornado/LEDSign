from random import randint

from uasyncio import sleep  # type: ignore

from config import CONFIG
from lib.colors import Color
from lib.led import Leds
from lib.ultra_sonic import Sensor


async def s_blink(leds: list[Leds], color_1: Color, color_2: Color) -> None:
    """
    Blinks the LEDs in the given colors.

    :param leds: the LEDs to blink.
    :param color_1: the first color to blink.
    :param color_2: the second color to blink.
    :return: None
    """

    for led in leds:
        await led.set_all(color_1)
    await sleep(1)
    for led in leds:
        await led.set_all(color_2)
    await sleep(1)


async def blink(leds: list[Leds]) -> None:
    """
    Blinks the LEDs in the given colors.

    :param leds: the LEDs to blink.
    :return: None
    """

    await s_blink(leds, Color.random(), Color.off())


async def error(leds: list[Leds]) -> None:
    """
    Blinks the LEDs in the given colors.

    :param leds: the LEDs to blink.
    :return: None
    """

    for led in leds:
        await led.set_all(Color.red())
    await sleep(0.25)
    for led in leds:
        await led.set_all(Color.off())
    await sleep(0.25)


async def fade(leds: list[Leds], progress: int = 0) -> None:
    """
    Fades the LEDs in the given colors.

    :param leds: the LEDs to fade.
    :param progress: the progress of the fade.

    :return: None
    """

    if progress >= 360:
        return

    for led in leds:
        await led.set_all(Color.from_hsv(progress, 1, 1))
    await fade(leds, progress + 20)


async def distance(leds: list[Leds], sensor: Sensor) -> None:
    """
    Changes the color of the LEDs depending on the distance to an object.

    :param leds: the LEDs to change.
    :param sensor: the sensor to read from.
    :return: None
    """

    _distance = sensor.read()
    color = Color.from_hsv(int(_distance / CONFIG['sensor']['max_distance'] * 360), 1, 1)
    for led in leds:
        await led.set_all(color, steps=30)


async def rave(leds: list[Leds]) -> None:
    """
    Rave mode for the LEDs

    :param leds: the LEDs to change.
    :return: None
    """

    color: Color = Color.from_hsv(randint(0, 360), 1, 1)
    for led in leds:
        await led.set_all(color, transition=False)
    await sleep(0.1)
