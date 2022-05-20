from osmclient import client
import json
import requests
import os, time

# pip3 install git+http://osm.etsi.org/gerrit/osm/IM.git
# pip3 install git+http://osm.etsi.org/gerrit/osm/osmclient.git
# pip3 install pyaml pycurl jinja2 python-magic packaging requests verboselogs

def post_json(url, reroute_JSON):
    try:
        r = requests.post(url, data=reroute_JSON)
        print(r.status_code)
    except IOError as e:
        print(e)
        return

sess = client.Client(host="10.30.64.15", sol005=True)

#resp = sess.ns.create("routerProxy-ns", "test", "admin", wait=True)
#print(resp)

reroute_JSON = {
        "api_key": "test-key",
        "routes": [
           {
                "key": "00:00:00:00:00:06/None00:00:00:00:00:09/None",
                "route": ["00:00:00:00:00:06/None", "of:0000000000000006", "of:000000000000000b", "of:000000000000000e", "00:00:00:00:00:09/None"]
                 }
            ],

        }
print(post_json('http://localhost:5000/api/push_intent',
    json.dumps(reroute_JSON)))

print("Reroute done. Press Enter to continue...")
resp = sess.ns.exec_op("test", op_name="action", op_data = {"primitive":"upgrade", "primitive_params":{}, "member_vnf_index": "1"}, wait=True)
print(resp)
#resp = sess.ns.exec_op("test", "downgrade", wait=True)
#print(resp)
input("Interface upgrade. Press Enter to continue...")
try:
    resp = sess.ns.exec_op("test", op_name="action", op_data = {"primitive": "test", "primitive_params": {"host": "10.10.0.6"}, "member_vnf_index": "1"}, wait=True)
    print(resp)
    input("Testin results. Press Enter to continue...")
except:
    os.system("ifconfig tap2 up")
    time.sleep(30)

resp = sess.ns.exec_op("test", op_name="action", op_data = {"primitive": "test", "primitive_params": {"host": "10.10.0.6"}, "member_vnf_index": "1"}, wait=True)
print(resp)
input("Interface connectivity restored. Press Enter to continue...")

reroute_JSON = {
        "api_key": "test-key",
        "routes": [
            {
                "key": "00:00:00:00:00:06/None00:00:00:00:00:09/None",
                "route": ["00:00:00:00:00:06/None", "of:0000000000000006", "of:0000000000000011", "of:000000000000000e", "00:00:00:00:00:09/None"]
                }
            ],

        }
print(post_json('http://localhost:5000/api/push_intent',
    json.dumps(reroute_JSON)))
input("Restore routing. Press Enter to continue...")

resp = sess.ns.exec_op("test", "downgrade", wait=True)
resp = sess.ns.exec_op("test", op_name="action", op_data = {"primitive":"downgrade", "primitive_params":{}, "member_vnf_index": "1"}, wait=True)
print(resp)
os.system("ifconfig tap2 down")
input("Reroute done. Press Enter to continue...")

# resp = sess.ns.delete("test")

