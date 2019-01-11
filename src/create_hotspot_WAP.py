#!/usr/bin/env python
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2010 - 2012 Red Hat, Inc.
#

#
# This example starts or stops a wifi hotspot
#
# Configuration settings are described at
# https://developer.gnome.org/NetworkManager/1.0/ref-settings.html
#

import dbus, sys, time, uuid


def hotspot_control(iface, operation, ip, gateway):
    generated_uuid = str(uuid.uuid4())
    s_con = dbus.Dictionary({
        'type': '802-11-wireless',
        'uuid': generated_uuid,
        'id': 'Test Hotspot'})

    addr1 = dbus.Dictionary({
        'address': ip,
        'prefix': dbus.UInt32(8)})

    s_wifi = dbus.Dictionary({
        'ssid': dbus.ByteArray("DronologyHotspot".encode("utf-8")),
        'mode': "ap",
        'band': "bg",
        'channel': dbus.UInt32(1)})

    s_wsec = dbus.Dictionary({
        'key-mgmt': 'wpa-psk',
        'psk': 'DronologyHotspot'})

    s_ip4 = dbus.Dictionary({'method': 'shared'})
    #     s_ip4 = dbus.Dictionary({
    #         'address-data': dbus.Array([addr1], signature=dbus.Signature('a{sv}')),
    #         'gateway': gateway,
    #         'method': 'manual'})

    s_ip6 = dbus.Dictionary({'method': 'ignore'})

    con = dbus.Dictionary({
        'connection': s_con,
        '802-11-wireless': s_wifi,
        '802-11-wireless-security': s_wsec,
        'ipv4': s_ip4,
        'ipv6': s_ip6})

    bus = dbus.SystemBus()
    service_name = "org.freedesktop.NetworkManager"
    proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager/Settings")
    settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

    proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager")
    nm = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
    devpath = nm.GetDeviceByIpIface(iface)

    # Find our existing hotspot connection
    connection_path = None
    for path in settings.ListConnections():
        proxy = bus.get_object(service_name, path)
        settings_connection = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings.Connection")
        config = settings_connection.GetSettings()
        if config['connection']['uuid'] == generated_uuid:
            connection_path = path
            break

    # If the hotspot connection didn't already exist, add it
    if not connection_path:
        connection_path = settings.AddConnection(con)

    # Now start or stop the hotspot on the requested device
    proxy = bus.get_object(service_name, devpath)
    device = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Device")
    if operation == "up":
        acpath = nm.ActivateConnection(connection_path, devpath, "/")
        proxy = bus.get_object(service_name, acpath)
        active_props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")

        # Wait for the hotspot to start up
        start = time.time()
        while time.time() < start + 10:
            state = active_props.Get("org.freedesktop.NetworkManager.Connection.Active", "State")
            if state == 2:  # NM_ACTIVE_CONNECTION_STATE_ACTIVATED
                print("Access point started")
                return
        print("Failed to start access point")
    elif operation == "down":
        device.Disconnect()
        print "Access point stopped"
        return
