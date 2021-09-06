'''
This program is used to telnet to the router and configure
a loopback interface 0 automatically and assign an ip address to it
'''

import sys
import telnetlib
import re

def connect():
    #Enter your host IP to which you wish to telnet to instead of x.x.x.x
    HOST = "172.16.0.1"

    # Executing the below command is similar to executing "telnet x.x.x.x" in
    # command prompt, this command establishes the telnet session
    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Username: ")
    tn.write(b"ngcdi\n")
    tn.read_until(b"Password: ")
    tn.write(b"ngcdi\n")
    print(tn.read_until(b"Router#"))
    return tn

def action(process):

    if process == "upgrade":
        up_intf = "gigabitEthernet 2/0"
        down_intf = "FastEthernet 1/0"
    elif process == "downgrade":
        up_intf = "FastEthernet 1/0"
        down_intf = "gigabitEthernet 2/0"
    elif process == "test":
        test()
        return
    else:
        raise Error("invalid actio n")

    tn = connect()
    #the below commands will configure the loop back interface
    tn.write(b"conf t\n\n")
    print(tn.read_until(b"Router(config)#"))
    tn.write(("int %s\n\n"%(down_intf)).encode("ascii"))
    print(tn.read_until(b"Router(config-if)#"))
    tn.write(b"shutdown\n\n")
    print(tn.read_until(b"Router(config-if)#"))
    tn.write(b"exit\n\n")
    print(tn.read_until(b"Router(config)#"))
    tn.write(("int %s\n\n"%(up_intf)).encode("ascii"))
    print(tn.read_until(b"Router(config-if)#"))
    tn.write(b"no shutdown\n\n")
    print(tn.read_until(b"Router(config-if)#"))
    tn.write(b"end\n")
    print(tn.read_until(b"Router#"))
    tn.write(b"exit\n")
    tn.close()

def test():
    tn = connect()
    tn.write(b"ping 10.10.0.3\n")
    res = tn.read_until(b"Router#")

    print(res)
    p = re.compile("Success rate is ([0-9]*) percent")
    m = p.search(res)
    if m is None:
        return False

    print("result %s"%(m.group(1)))
    return (int(m.group(1))) > 0


if __name__ == "__main__":
    if (len(sys.argv) < 2) or (sys.argv[1] not in ["upgrade", "downgrade", "test"]):
        print("usage: ./config.py upgrade|downgrade|test")
        sys.exit(1)

    action(sys.argv[1])
