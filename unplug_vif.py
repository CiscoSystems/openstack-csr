#!/usr/bin/python

import sys

from oslo.config import cfg
import neutron.openstack.common.gettextutils as gtutil
gtutil.install('')
import neutron.agent.linux.interface as vif_driver
from neutronclient.neutron import client as qclient
import neutronclient.common.exceptions as qcexp
from neutron.agent.common import config

# Arg 1: controller host
# Arg 2: name of admin user
# Arg 3: admin user password
# Arg 4: tenant name
# Arg 5: name of interface
# Arg 6: MAC address of tap interface
# Arg 7: uuid of VM
# Arg 8: name of bridge
# Arg 9: name of port
# Arg 10: id of port  
# Arg 11: name of net
# Arg 12: id of net

host = sys.argv[1]
user = sys.argv[2]
pw = sys.argv[3]
tenant = sys.argv[4]
interface = sys.argv[5]
mac_addr = sys.argv[6]
vm_uuid = sys.argv[7]
port_id = sys.argv[10]
nw_id = sys.argv[12]

br_name = 'br-int'

conf = cfg.CONF
config.register_root_helper(conf)
conf.register_opts(vif_driver.OPTS)

driver = vif_driver.OVSInterfaceDriver(cfg.CONF)
print "Unplug %s for %s" % (interface, br_name)
driver.unplug(interface, br_name)

KEYSTONE_URL='http://' + host + ':5000/v2.0'
 
qc = qclient.Client('2.0', auth_url=KEYSTONE_URL, username=user,
tenant_name=tenant, password=pw)

try:
   qc.delete_port(port_id)
   print "Deleted port %s from Neutron" % port_id
except qcexp.NeutronClientException as qce:
   print "Failed to delete port %s: %s" % (port_id, qce)
   pass
