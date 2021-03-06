# in bash 1st: export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
import dbus

print "pi3 networking loaded"


def hotspot_control(iface, operation, ip, gateway, connection_uuid, network_name):
    print "attempting config"
    s_con = dbus.Dictionary({
        'type': '802-11-wireless',
        'uuid': connection_uuid,
        'id': 'test hotspot'})

    addr1 = dbus.Dictionary({
        'address': ip,
        'prefix': dbus.UInt32(8)})

    s_wifi = dbus.Dictionary({
        'ssid': dbus.ByteArray(network_name.encode("utf-8")),
        'mode': "adhoc",
        'band': "bg",
        'channel': dbus.UInt32(1)})

    s_wsec = dbus.Dictionary({
        'key-mgmt': 'none',
        'wep-key0': '0123456789abcdef0123456789'})

    # Use link-local for auto IP selection and manual for ability to set gateway etc but ability to manually
    # configure unique IPs within balena framework isn't yet done
    s_ip4 = dbus.Dictionary({'method': 'link-local'})

    #    s_ip4 = dbus.Dictionary({
    #        'address-data': dbus.Array([addr1], signature=dbus.Signature('a{sv}')),
    #        'gateway': gateway,
    #        'method': 'manual'})

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

    # Find the existing hotspot connection if it exists
    connection_path = None
    for path in settings.ListConnections():
        proxy = bus.get_object(service_name, path)
        settings_connection = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings.Connection")
        config = settings_connection.GetSettings()
        if config['connection']['uuid'] == connection_uuid:
            connection_path = path
            break
    # If the hotspot connection didn't already exist, add it
    if not connection_path:
        connection_path = settings.AddConnection(con)
    print "got a connection path"

    # Now start or stop the hotspot on the requested device
    proxy = bus.get_object(service_name, devpath)
    device = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Device")
    if operation == "up":
        acpath = nm.ActivateConnection(connection_path, devpath, "/")
        proxy = bus.get_object(service_name, acpath)
        active_props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
        state = active_props.Get("org.freedesktop.NetworkManager.Connection.Active", "State")
        print "started access point"
        print "Access point started, state: {}".format(state)

    elif operation == "down":
        device.Disconnect()
        print "Access point stopped"
        return
