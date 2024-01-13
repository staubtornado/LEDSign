from asyncio import sleep

from network import WLAN, STA_IF  # type: ignore


async def connect_to_wlan(ssid: str, passwort: str) -> None:
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, passwort)

    if not wlan.isconnected():
        print(f"Connecting to {ssid}...")
        while not wlan.isconnected():
            await sleep(0)
    print("Connected to WLAN", wlan.ifconfig()[0])
