from asyncio import sleep

from machine import ADC  # type: ignore

from config import CONFIG
from lib.colors import Color
from lib.led import Leds
from lib.microdot import Microdot, send_file, Response, Request
from lib.modes import blink, fade, distance, rave, s_blink, cyberpunk
from lib.thread import Thread
from lib.ultra_sonic import Sensor


def run_server(loop, leds: list[Leds], sensor: Sensor) -> None:
    app: Microdot = Microdot()
    thread: Thread = Thread(loop, distance, leds, sensor)
    thread.start()

    @app.route("/", methods=['GET'])
    async def index(request) -> Response:
        return send_file('/web/index.html', content_type='text/html')

    @app.route("/css/<path:path>", methods=['GET'])
    async def static(request, path: str) -> Response:
        return send_file('/web/css/' + path)

    @app.route("/img/<path:path>", methods=['GET'])
    async def static(request, path: str) -> Response:
        return send_file('/web/img/' + path)

    @app.route("/js/<path:path>", methods=['GET'])
    async def static(request, path: str) -> Response:
        return send_file('/web/js/' + path)

    @app.route("/api/info", methods=['GET'])
    async def get_info(request) -> Response:
        sensor_temp = ADC(4)
        conversion_factor = 3.3 / 65535
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = round(27 - (reading - 0.706) / 0.001721, 2)

        return Response({
            'network': CONFIG['network']['ssid'],
            'temp': f"{temperature}°C",
            'version': CONFIG['version'],
            'mode': thread.get_target().__name__[:-1],
        })

    @app.route("/api/leds", methods=['POST'])
    async def set_leds(request: Request) -> Response:
        """
        Sets all LEDs to the given color.

        :param request: the request.
        :return: None
        """

        mode = request.json.get('mode')
        color = request.json.get('color')

        print(mode, color)

        if not mode:
            return Response("Missing mode", status_code=400)

        if mode != "static" and not thread.is_running():
            thread.start()

        if mode in ["static", "s-blink"]:
            if not color:
                return Response("Missing color", status_code=400)

            if mode == "s-blink":
                thread.update(s_blink, leds, Color.from_hex(color), Color.off())
            else:
                thread.cancel()

                while thread.is_running():
                    await sleep(0)

                for led in leds:
                    try:
                        await led.set_all(Color.from_hex(color))
                    except (ValueError, TypeError):
                        return Response(f"Invalid color: {color}", status_code=400)
        elif mode == "blink":
            thread.update(blink, leds)
        elif mode == "fade":
            thread.update(fade, leds)
        elif mode == "distance":
            thread.update(distance, leds, sensor)
        elif mode == "rave":
            thread.update(rave, leds)
        elif mode == "cyberpunk":
            thread.update(cyberpunk, leds)
        else:
            return Response(f"Unknown mode: {mode}", status_code=400)
        return Response("OK")

    app.run()
