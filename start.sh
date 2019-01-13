#!/bin/sh
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
echo "Hello from bash"
python src/main.py --settings=adhoc_network
echo "all donr from bash"
