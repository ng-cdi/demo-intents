# Automated ng-cdi intent demo stuff

## Running

1. Start everything up:`docker-compose up`
2. Connect to the onos cli: `ssh -o StrictHostKeyChecking=no -l onos -p 8101
   localhost`
3. !!important!!: In the onos cli, run: `imr:startmon 187 org.onosproject.ifwd`

### To shut down

1. Send C-c or `docker-compose down`
2. If you still have cores spinning after stopping, run `sudo mn -c` on the
   host.

## Make sure you have

1. openvswitch installed on the host (the kernel module is needed), you probably
   want mininet installed too just in case.
2. if something complains about a hostname not being found, make sure the host's
   /etc/hosts has `127.0.0.1 localhost`

<!--  LocalWords:  openvswitch
 -->
