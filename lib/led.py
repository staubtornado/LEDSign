__author__ = "Julian Kirchner"


try:
    from thonny.plugins.micropython.base_api_stubs.machine import Pin
    from thonny.plugins.micropython.base_api_stubs.neopixel import NeoPixel
    from thonny.plugins.micropython.base_api_stubs.utime import sleep
except ImportError:
    from machine import Pin  # type: ignore
    from neopixel import NeoPixel  # type: ignore
    from utime import sleep  # type: ignore

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
        self.color = color

    def set_all(self, color: Color, transition: bool = True) -> None:
        """
        Sets all LEDs to the given color.

        :param color: the color to set to.
        :param transition: whether to transition to the color or not.
        :return: None
        """

        if not transition:
            for i in range(self.num_leds):
                self.set_led(i, color.rgb)
            self.color = color
            return

        r, g, b = self.color.rgb

        while self.color.rgb != color.rgb:
            if r < color.rgb[0]:
                r = r + 1
            if r > color.rgb[0]:
                r = r - 1

            if g < color.rgb[1]:
                g = g + 1
            if g > color.rgb[1]:
                g = g - 1

            if b < color.rgb[2]:
                b = b + 1
            if b > color.rgb[2]:
                b = b - 1
            self.set_all(Color(r, g, b), False)

    def clear(self) -> None:
        """
        Sets all LEDs to the OFF-Color.

        :return: None
        """

        self.set_all(Color.off())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Leds):
            return self.num_leds == other.num_leds and self.color == other.color
        return False

    def __str__(self) -> str:
        return f"Leds({self.num_leds}, {self.color})"

    def __repr__(self) -> str:
        return f"<Leds({self.num_leds}, {self.color})>"
