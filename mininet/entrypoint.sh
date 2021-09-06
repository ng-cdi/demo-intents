#!/bin/bash

echo
echo "Starting Dynamips"
echo

echo "dynamips --idle-pc 0x641a83e4 -P 7200 -T 2001 -A 3001 \
	-p 1:PA-4E -s 1:0:tap:tap0 -s 1:1:tap:tap1 -s 1:2:tap:tap3 \
	-p 2:PA-GE -s 2:0:tap:tap2 \
	-C $DYNAGEN_ROUTER_CFG -X $DYNAGEN_IMG &"

ip tuntap add mode tap tap0
ip tuntap add mode tap tap1
ip tuntap add mode tap tap3
ip tuntap add mode tap tap2
ip link set dev tap0 up 
ip link set dev tap1 up 
ip link set dev tap3 up 
ip link set dev tap2 up 

dynamips --idle-pc 0x641a83e4 -P 7200 -T 2001 -A 3001 \
	-p 1:PA-4E -s 1:0:tap:tap0 -s 1:1:tap:tap1 -s 1:2:tap:tap3 \
	-p 2:PA-GE -s 2:0:tap:tap2 \
	-C $DYNAGEN_ROUTER_CFG -X $DYNAGEN_IMG &


## hack this in, otherwise we start before onos is up fully and die
echo "MININET waiting for ONOS"

response=1

while [ $response -ne 0 ]; do
  sleep 1
  curl -f --user onos:rocks http://localhost:8181/onos/v1/devices >/dev/null
  response=$?
done

echo "ONOS is up! waiting 5 more seconds to be sure"

sleep 5

# run these just to make sure?
curl -X POST --user onos:rocks http://localhost:8181/onos/v1/applications/org.onosproject.openflow/active
curl -X DELETE --user onos:rocks http://localhost:8181/onos/v1/applications/org.onosproject.fwd/active
curl -X POST --user onos:rocks http://localhost:8181/onos/v1/applications/org.onosproject.imr/active

service openvswitch-switch start
ovs-vsctl set-manager ptcp:6640

echo
echo "Cleaning MN"
echo

sudo mn -c

echo
echo "Running Topology: " $TOPO
echo

python3 $TOPO

echo
echo "Quitting Mininet: " $TOPO
echo

service openvswitch-switch stop
ip link delete tap0
ip link delete tap1
ip link delete tap2
ip link delete tap3
