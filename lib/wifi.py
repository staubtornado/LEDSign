from network import WLAN, STA_IF  # type: ignore


def connect_to_wlan(ssid: str, passwort: str) -> None:
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, passwort)

    if not wlan.isconnected():
        print(f"Connecting to {ssid}...")
        while not wlan.isconnected():
            pass
    print("Connected to WLAN", wlan.ifconfig()[0])
