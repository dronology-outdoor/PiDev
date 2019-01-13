#!/bin/sh
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

echo "Setting adhoc wifi"
python src/main.py --settings=adhoc_network
echo "Network configured"
#i="0"
#while [ $i -lt 10 ]
#do
#echo "Hello, I'm waiting"
#pwd
#ls
#sleep 5
#done
echo "Starting pixhawk transmission script"
python application/PiDronology/main.py --settings=dronology_Settings
