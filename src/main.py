import time 
#import NetworkConfig
import CreateHotSpot

CreateHotSpot.hotspot_control('wlp4s0','down','10.1.2.3','10.1.2.1')

while (1):
	print ("BOGS")
	time.sleep(10)
