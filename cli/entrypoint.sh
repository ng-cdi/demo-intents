#!/bin/bash

echo "CLI waiting for ONOS"

response=1

while [ $response -ne 0 ]; do
  sleep 1
  curl -f --user onos:rocks http://localhost:8181/onos/v1/devices >/dev/null
  response=$?
done

echo "ONOS is up! waiting 5 more seconds to be sure"

sleep 5

ssh -o StrictHostKeyChecking=no -l onos -p 8101 localhost
