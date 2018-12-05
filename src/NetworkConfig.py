#!/bin/env python
import dbus
import sys
import posix
import time
import uuid

uuid = str(uuid.uuid4())

s_con = {'id': 'MyAdHoc',
         'uuid': uuid,
         'type': '802-11-wireless',
         'autoconnect': False,
         'name': 'connection'}

s_wifi = {'ssid': dbus.ByteArray("foobar"),
          'mode': 'adhoc',
 #         'security': '802-11-wireless-security',
        'name': '802-11-wireless'}

#s_wsec = {'key-mgmt': 'none',
#          'wep-key0': '0123456789abcdef0123456789',
#          'name': '802-11-wireless-security'}

s_ip4 = {'method': 'link-local',
         'name': 'ipv4'}

con = {'connection': s_con,
       '802-11-wireless': s_wifi,
#       '802-11-wireless-security': s_wsec,
       'ipv4': s_ip4}

# init dbus
sys_bus = dbus.SystemBus()
#ses_bus = dbus.SessionBus()

#ss_proxy = sys_bus.get_object('org.freedesktop.NetworkManagerSystemSettings', '/org/freedesktop/NetworkManagerSettings')
#ss_iface = dbus.Interface(ss_proxy, 'org.freedesktop.NetworkManagerSettings')
#ss_sys_iface = dbus.Interface(ss_proxy, 'org.freedesktop.NetworkManagerSettings.System')

nm_proxy = sys_bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')
nm_iface = dbus.Interface(nm_proxy, 'org.freedesktop.NetworkManager')

#pk_proxy = ses_bus.get_object('org.freedesktop.PolicyKit.AuthenticationAgent', '/')
#pk_iface = dbus.Interface(pk_proxy, 'org.freedesktop.PolicyKit.AuthenticationAgent')



def find_connection(requested_uuid):
#    for c in ss_iface.ListConnections():
#        print "get the details of the connection"
#        c_proxy = sys_bus.get_object('org.freedesktop.NetworkManagerSystemSettings', c)
#        c_iface = dbus.Interface(c_proxy, 'org.freedesktop.NetworkManagerSettings.Connection')
#        settings = c_iface.GetSettings()
#        if settings['connection']['uuid'] == requested_uuid:
#            print "found our connection"
#            return c
#    return None


def try_add(connection):
    try:
        print "Ask the system settings service to create the connection"
        ss_sys_iface.AddConnection(connection)
        return None
    except Exception, e:
        parts = str(e).split(' ')
        if parts[0].find('org.freedesktop.NetworkManagerSettings.System.NotPrivileged') < 0:
            print "not a permission denied, give up and exit"
            print e
            sys.exit(1)
        print "yay, permission denied, we can handle this"
        return parts[1]


# MAIN PROGRAM
def configure_adhoc():

    con_path = find_connection(uuid)
#    if not con_path:
#        print "Try to create the connection, which could fail if we need authorization.\n If auth is required, " \
#              "get the auth and try adding it again "
#        action = try_add(con)
#        if action:
#            gained = pk_iface.ObtainAuthorization(action, 0, posix.getpid())
#            if gained:
#                print "Yay, we have the privilege now, try adding again"
#                action = try_add(con)
#                if action:
#                    print "hmm, something went wrong and PolicyKit wasn't able to auth the user"
#                    sys.exit(1)
#
#                con_path = find_connection(uuid)
#
    print " Check again in case it was just added"
    if not con_path:
        print "Couldn't get newly created connection from system settings"

    print "Find a wifi device to activate this connection on"
    dev_path = None
    for dev in nm_iface.GetDevices():
        dev_proxy = sys_bus.get_object('org.freedesktop.NetworkManager', dev)
        dev_props_iface = dbus.Interface(dev_proxy, 'org.freedesktop.DBus.Properties')
        props = dev_props_iface.GetAll('org.freedesktop.NetworkManager.Device')
        if props['DeviceType'] == 2:  # wifi
            dev_path = dev
            break

    if not dev_path:
        print "No wifi devices available"
        sys.exit(1)

    # Now ask NM to activate that connection
    active_path = nm_iface.ActivateConnection('org.freedesktop.NetworkManagerSystemSettings', con_path, dev_path, "/")
    if not active_path:
        print "Couldn't activate connection"
        sys.exit(1)

    # Wait for the connection to become active
    active_proxy = sys_bus.get_object('org.freedesktop.NetworkManager', active_path)
    active_props_iface = dbus.Interface(active_proxy, 'org.freedesktop.DBus.Properties')

    state = 0
    while state != 2:  # 2 == activated
        state = active_props_iface.Get('org.freedesktop.NetworkManager.Connection.Active', 'State')
        if state != 2:
            print "waiting for connection to become active..."
            time.sleep(1)

    print "activated!"
