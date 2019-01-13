import pi3_networking
from simple_settings import settings

if __name__ == "__main__":
    # Start adhoc interface
    pi3_networking.hotspot_control('wlan0', "up", settings.IP, settings.GATEWAY, settings.CONNECTION_UUID,
                                   settings.NETWORK_NAME)
