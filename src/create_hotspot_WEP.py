import dbus, time, uuid


def hotspot_control(iface, operation, ip, gateway):
    generated_uuid = str(uuid.uuid4())
    s_con = dbus.Dictionary({
        'type': '802-11-wireless',
        'uuid': generated_uuid,
        'id': 'test hotspot'})

    addr1 = dbus.Dictionary({
        'address': ip,
        'prefix': dbus.UInt32(8)})

    s_wifi = dbus.Dictionary({
        'ssid': dbus.ByteArray("dronologyhotspot".encode("utf-8")),
        'mode': "ap",
        'band': "bg",
        'channel': dbus.UInt32(1)})

    s_wsec = dbus.Dictionary({
        'key-mgmt': 'none',
        'wep-key0': '0123456789abcdef0123456789'})

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
