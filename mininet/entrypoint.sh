#!/bin/bash

echo
echo "Starting Dynamips"
echo

echo "dynamips --idle-pc 0x641a83e4 -P 7200 -T 2001 -A 3001 \
	-p 1:PA-4E -s 1:0:tap:tap0 -s 1:1:tap:tap1 -s 1:2:tap:tap3 \
	-p 2:PA-GE -s 2:0:tap:tap2 \
	-C $DYNAGEN_ROUTER_CFG -X $DYNAGEN_IMG &"

dynamips --idle-pc 0x641a83e4 -P 7200 -T 2001 -A 3001 \
	-p 1:PA-4E -s 1:0:tap:tap0 -s 1:1:tap:tap1 -s 1:2:tap:tap10 \
	-p 2:PA-GE -s 2:0:tap:tap2 \
	-C $DYNAGEN_ROUTER_CFG -X $DYNAGEN_IMG &

brctl addbr mgmt
brctl addif mgmt tap0
ifconfig mgmt 192.168.0.100/24 up

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

ifconfig mgmt 0.0.0.0 down
brctl delif mgmt tap0
brctl delbr mgmt

service openvswitch-switch stop
