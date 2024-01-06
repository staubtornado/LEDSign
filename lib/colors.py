from random import randint


class Color:
    def __init__(self, red: int, green: int, blue: int) -> None:
        """
        Constructs a Color-Object.

        :param red: the red value of the color.
        :param green: the green value of the color.
        :param blue: the blue value of the color.
        """

        self._red = red
        self._green = green
        self._blue = blue

    @property
    def rgb(self) -> tuple[int, int, int]:
        """
        Returns the RGB-Values of the Color.

        :return: a tuple with the RGB-Values.
        """
        return self._red, self._green, self._blue

    @classmethod
    def off(cls) -> 'Color':
        """
        Creates a Color-Object with the OFF-Color.

        :return: a Color-Object.
        """
        return cls(0, 0, 0)

    @classmethod
    def red(cls) -> 'Color':
        """
        Creates a Color-Object with the RED-Color.

        :return: a Color-Object.
        """
        return cls(255, 0, 0)

    @classmethod
    def from_hsv(cls, h: int, s: int, v: int) -> 'Color':
        """
        Creates a Color-Object from HSV-Values.

        :param h: the hue of the color.
        :param s: the saturation of the color.
        :param v: the value of the color.
        :return: a Color-Object.
        """

        h = h % 360
        s = min(max(s, 0), 1)
        v = min(max(v, 0), 1)

        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return cls(int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

    @classmethod
    def from_hex(cls, hex_value: str) -> 'Color':
        """
        Creates a Color-Object from a HEX-String.

        :param hex_value: the hex-string to create the color from.
        :return: a Color-Object.
        """

        hex_value = hex_value.lstrip('#')
        return cls(*[int(hex_value[i:i + 2], 16) for i in (0, 2, 4)])

    @classmethod
    def random(cls) -> 'Color':
        """
        Creates a random Color-Object.

        :return: a Color-Object.
        """

        return cls.from_hsv(randint(0, 360), 1, 1)
