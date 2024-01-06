__author__ = "Julian Kirchner"


from machine import Pin  # type: ignore
from neopixel import NeoPixel  # type: ignore
from asyncio import sleep  # type: ignore

from lib.colors import Color


class Leds:
    """
    Represents a LED-Stripe. It can be used to set all LEDs to a specific color.
    """

    def __init__(self, num_leds: int, pin: int) -> None:
        """
        Constructs a Led-Stripe-Object.

        :param num_leds: an int with the count of the LEDs in the Stripe.
        :param pin: an int which represents the Pin on the Board.
        """

        self.num_leds = num_leds
        self.np = NeoPixel(Pin(pin), num_leds)
        self.color = Color.off()

    def set_led(self, led: int, color: tuple[int, int, int]) -> None:
        """
        Sets a specific LED to the given color.

        :param led: the LED to set.
        :param color: the color to set to.
        :return: None
        """

        self.np[led] = color
        self.np.write()

    async def set_all(self, color: Color, transition: bool = True, steps: int = 100) -> None:
        """
        Sets all LEDs to the given color.

        :param color: the color to set to.
        :param transition: whether to transition to the color or not.
        :param steps: the number of steps in the transition.
        :return: None
        """

        def interpolate_color(color1, color2, ratio):
            r = color1[0] * (1 - ratio) + color2[0] * ratio
            g = color1[1] * (1 - ratio) + color2[1] * ratio
            b = color1[2] * (1 - ratio) + color2[2] * ratio
            return int(r), int(g), int(b)

        def create_fade(rgb1, rgb2, _steps):
            colors = []
            for j in range(_steps + 1):
                colors.append(interpolate_color(rgb1, rgb2, j / _steps))
                sleep(0)
            return colors

        if not transition:
            for i in range(self.num_leds):
                self.set_led(i, color.rgb)
                await sleep(0)
            self.color = color
            return

        fade = create_fade(self.color.rgb, color.rgb, steps)
        for rgb in fade:
            for i in range(self.num_leds):
                self.set_led(i, rgb)
                await sleep(0)
            self.color = Color(*rgb)

    async def clear(self) -> None:
        """
        Sets all LEDs to the OFF-Color.

        :return: None
        """
        await self.set_all(Color.off())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Leds):
            return self.num_leds == other.num_leds and self.color == other.color
        return False

    def __str__(self) -> str:
        return f"Leds({self.num_leds}, {self.color})"

    def __repr__(self) -> str:
        return f"<Leds({self.num_leds}, {self.color})>"
