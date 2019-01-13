import time
import pi3_networking
from simple_settings import settings

#Start adhoc interface
pi3_networking.hotspot_control('wlan0', "up", settings.IP, settings.GATEWAY, settings.CONNECTION_UUID, settings.NETWORK_NAME)

while (1):
    print ("BOGS")
    time.sleep(10)
