import time
# import NetworkConfig
import create_adhoc
import create_hotspot_WAP
import create_hotspot_WEP


#create_hotspot_WAP.hotspot_control('wlp4s0','down','10.1.2.3','10.1.2.1')
#create_hotspot_WEP.hotspot_control('wlp4s0', 'up', '10.1.2.3', '10.1.2.1')
create_adhoc.createadhoc_control('wlp4s0','up','10.1.2.3','10.1.2.1')

while (1):
    print ("BOGS")
    time.sleep(10)
