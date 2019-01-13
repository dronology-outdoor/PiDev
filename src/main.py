import pi3_networking
import time
from simple_settings import settings

if __name__ == "__main__":
    # Start adhoc interface
    pi3_networking.hotspot_control('wlan0', "up", settings.IP, settings.GATEWAY, settings.CONNECTION_UUID,
                                   settings.NETWORK_NAME)
    while(1):
        print("killing time")
        time.sleep(10)
