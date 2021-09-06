from osmclient import client

# pip3 install git+http://osm.etsi.org/gerrit/osm/IM.git
# pip3 install git+http://osm.etsi.org/gerrit/osm/osmclient.git
# pip3 install pyaml pycurl jinja2 python-magic packaging requests verboselogs

sess = client.Client(host="10.30.64.15", sol005=True)

resp = sess.ns.create("routerProxy-ns", "test", "admin", wait=True)
print(resp)

resp = sess.ns.exec_op("test", "upgrade", wait=True)
print(resp)
resp = sess.ns.exec_op("test", "downgrade", wait=True)
print(resp)
resp = sess.ns.exec_op("test", "test", op_data = {"host": "10.10.0.3"}, wait=True)
print(resp)

resp = sess.ns.delete("test")

