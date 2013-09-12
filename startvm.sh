#!/bin/bash

# YOU CHANGE SETTINGS IN THE 'config.ini' FILE.
source config.ini

if [ -f .instance_info ]; then
   rm .instance_info
fi

IFNAME_ETH0=$NAME"__private"
IFNAME_ETH1=$NAME"__public"
# You add interfaces on aditional networks
# by specifying an IFNAME_ETHx line. The
# word following the '__' is the name of the
# Neutron network.
#IFNAME_ETH2=$NAME"__testnet"

# To add interfaces you also need to add lines such
# as the following two:
# -net nic,macaddr=$MACADDR_ETH2,model=e1000,vlan=2 \
# -net tap,ifname=$IFNAME_ETH2,vlan=2,script=osn-ifup-br-int,downscript=osn-ifdown-br-int \
# Use osn-ifup-br-ex/osn-ifdown-br-ex for external Neutron networks.
# Use osn-ifup-br-int/osn-ifdown-br-int for all other Neutron networks.

kvm -m 8192 -name $NAME \
-smp 4 \
-serial telnet:$TELNET_ACCESS,server,nowait \
-net nic,macaddr=$MACADDR_ETH0,model=e1000,vlan=0 \
-net tap,ifname=$IFNAME_ETH0,vlan=0,script=osn-ifup-br-int,downscript=osn-ifdown-br-int \
-net nic,macaddr=$MACADDR_ETH1,model=e1000,vlan=1 \
-net tap,ifname=$IFNAME_ETH1,vlan=1,script=osn-ifup-br-ex,downscript=osn-ifdown-br-ex \
-drive file=$IMAGE \
-boot c \
-vga cirrus \
-vnc $VNC_ACCESS

