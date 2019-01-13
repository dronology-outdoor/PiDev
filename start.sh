#!/bin/sh
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

echo "Setting adhoc wifi"
python src/main.py --settings=adhoc_network
echo "Network configured"

echo "Starting pixhawk transmission script"
python app/main.py --settings=dronology_Settings

