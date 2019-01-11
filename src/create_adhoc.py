import dbus, time, uuid

def createadhoc_control(iface, ip, gateway):
    generated_uuid = str(uuid.uuid4())
    s_con = dbus.Dictionary({
        'type': '802-11-wireless',
        'uuid': generated_uuid,
        'id': 'DevAdhoc'})

    addr1 = dbus.Dictionary({
        'address': ip,
        'prefix': dbus.UInt32(8)})

    s_wifi = dbus.Dictionary({
        'ssid': dbus.ByteArray("Adhoc".encode("utf-8")),
        'mode': "adhoc",
        'band': "bg",
        'channel': dbus.UInt32(1)})

    s_wsec = dbus.Dictionary({
        'key-mgmt': 'none',
        'wep-key0': '0123456789abcdef0123456789'})

    s_ip4 = dbus.Dictionary({
        'address-data': dbus.Array([addr1], signature=dbus.Signature('a{sv}')),
        'gateway': gateway,
        'method': 'manual'})

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

    #Get permissions

    #Create Connection
    connection_path = settings.AddConnection(con)

    #Activate connection
    acpath = nm.ActivateConnection(connection_path, devpath, "/")

    #Query state
    proxy = bus.get_object(service_name, acpath)
    active_props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")

    # Wait for the adhoc to start up
    start = time.time()
    while time.time() < start + 10:
        state = active_props.Get("org.freedesktop.NetworkManager.Connection.Active", "State")
        if state == 2:  # NM_ACTIVE_CONNECTION_STATE_ACTIVATED
            print("Adhoc started")
            return
    print("Failed to start adhoc")
    return

createadhoc_control('wlp4s0','10.1.2.3','10.1.2.1')