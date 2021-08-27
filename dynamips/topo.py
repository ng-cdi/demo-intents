#!/usr/bin/env python


from mininet.net import Mininet
from mininet.link import  Intf
from mininet.log import setLogLevel, info
from mininet.cli import CLI



def myNetwork():

    net = Mininet(topo=None, controller=None,
                  build=False)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    Intf('tap0', node=s1)
    Intf('tap1', node=s2)
    Intf('tap2', node=s2)
    Intf('tap3', node=s3)

    info('*** Add hosts\n')
    m1 = net.addHost('m1', ip='172.16.0.2/16')
    h1 = net.addHost('h1', ip='10.10.0.1/16')
    h2 = net.addHost('h2', ip='10.10.0.2/16')

    info('*** Add links\n')
    net.addLink(m1, s1)
    net.addLink(h1, s2)
    net.addLink(h2, s3)

    info('*** Starting network\n')
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
