import time, uuid
import pi3_networking

#Start adhoc interface
ip='10.1.2.5'
gateway='10.42.0.200'
connection_uuid = str(uuid.uuid4())

pi3_networking.hotspot_control('wlan0', up, ip, gateway,connection_uuid)

while (1):
    print ("BOGS")
    time.sleep(10)
