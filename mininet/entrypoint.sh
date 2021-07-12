#!/bin/bash

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

## run these just to make sure?

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

service openvswitch-switch stop
