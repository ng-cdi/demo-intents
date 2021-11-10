#!/usr/bin/env python       

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.rest import REST
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.log import lg, info
from mininet.node import Node
from mininet.topolib import TreeTopo
from mininet.util import waitListening
from mininet.node import OVSKernelSwitch

# class CustomTopo(Topo):
#     def __init__(self, bw=1e3, **opts):
#         super(CustomTopo, self).__init__(**opts)

#         s = [self.addSwitch('s%d' % n) for n in range(1, 4)]
#         h = [self.addHost('h%d' % n) for n in range(1, 5)]

#         self.addLink(s[0], s[1], bw=bw)
#         self.addLink(s[0], s[2], bw=bw)
#         self.addLink(s[2], s[1], bw=bw)

#         self.addLink(h[0], s[0], bw=bw)
#         self.addLink(h[1], s[0], bw=bw)
#         self.addLink(h[2], s[1], bw=bw)
#         self.addLink(h[3], s[1], bw=bw)

# def connectToRootNS( network, switch, ip, routes ):
#     """Connect hosts to root namespace via switch. Starts network.
#       network: Mininet() network object
#       switch: switch to connect to root namespace
#       ip: IP address for root namespace node
#       routes: host networks to route to"""
#     # Create a node in root namespace and link to switch 0
#     root = Node( 'root', inNamespace=False )
#     intf = network.addLink( root, switch ).intf1
#     root.setIP( ip, intf=intf )
#     # Start network that now includes link to root namespace
#     network.start()
#     # Add routes from root ns to hosts
#     for route in routes:
#         root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

# def sshd( network, cmd='/usr/sbin/sshd', opts='-D',
#           ip='10.123.123.1/32', routes=None, switch=None ):
#     """Start a network, connect it to root ns, and run sshd on all hosts.
#        ip: root-eth0 IP address in root namespace (10.123.123.1/32)
#        routes: Mininet host networks to route to (10.0/24)
#        switch: Mininet switch to connect to root namespace (s1)"""
#     if not switch:
#         switch = network[ 's1' ]  # switch to use
#     if not routes:
#         routes = [ '10.0.0.0/24' ]
#     connectToRootNS( network, switch, ip, routes )
#     for host in network.hosts:
#         host.cmd( cmd + ' ' + opts + '&' )
#     info( "*** Waiting for ssh daemons to start\n" )
#     for server in network.hosts:
#         waitListening( server=server, port=6767, timeout=5 )

#     info( "\n*** Hosts are running sshd at the following addresses:\n" )
#     for host in network.hosts:
#         info( host.name, host.IP(), '\n' )
#     info( "\n*** Type 'exit' or control-D to shut down network\n" )
#     CLI( network )
#     for host in network.hosts:
#         host.cmd( 'kill %' + cmd )
#     network.stop()

if __name__ == '__main__':
    net = Mininet(controller=RemoteController, link=TCLink)
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6633)

    info( '*** Adding Hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1', mac='00:00:00:00:00:01' )
    h2 = net.addHost( 'h2', ip='10.0.0.2', mac='00:00:00:00:00:02' )
    h3 = net.addHost( 'h3', ip='10.0.0.3', mac='00:00:00:00:00:03' )
    h4 = net.addHost( 'h4', ip='10.0.0.4', mac='00:00:00:00:00:04' )
    h5 = net.addHost( 'h5', ip='10.0.0.5', mac='00:00:00:00:00:05' )
    h6 = net.addHost( 'h6', ip='10.0.0.6', mac='00:00:00:00:00:06' )
    h7 = net.addHost( 'h7', ip='10.0.0.7', mac='00:00:00:00:00:07' )
    h8 = net.addHost( 'h8', ip='10.0.0.8', mac='00:00:00:00:00:08' )
    h9 = net.addHost( 'h9', ip='10.0.0.9', mac='00:00:00:00:00:09' )


    info( '*** Adding switches\n' )
    s1 = net.addSwitch( 's1', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s2 = net.addSwitch( 's2', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s3 = net.addSwitch( 's3', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s4 = net.addSwitch( 's4', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s5 = net.addSwitch( 's5', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s6 = net.addSwitch( 's6', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s7 = net.addSwitch( 's7', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s8 = net.addSwitch( 's8', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s9 = net.addSwitch( 's9', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch, batch=True, failMode="standalone")
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch, batch=True, failMode="standalone")


    bandwidth = 100
    core_bw = 1000

    info( '*** Creating links\n' )
    net.addLink(h1, s1, bw=bandwidth)
    net.addLink(h2, s2, bw=bandwidth)
    net.addLink(h3, s3, bw=bandwidth)
    net.addLink(h4, s4, bw=bandwidth)
    net.addLink(h5, s5, bw=bandwidth)
    net.addLink(h6, s6, bw=bandwidth)
    net.addLink(h7, s12, bw=core_bw)
    net.addLink(h8, s13, bw=core_bw)
    net.addLink(h9, s14, bw=core_bw)

    # Access Nodes
    net.addLink(s1, s7, bw=bandwidth)
    net.addLink(s1, s8, bw=bandwidth)
    net.addLink(s2, s7, bw=bandwidth)
    net.addLink(s2, s8, bw=bandwidth)
    net.addLink(s2, s9, bw=bandwidth)
    net.addLink(s3, s9, bw=bandwidth)
    net.addLink(s3, s10, bw=bandwidth)
    net.addLink(s4, s9, bw=bandwidth)
    net.addLink(s4, s10, bw=bandwidth)
    net.addLink(s5, s11, bw=bandwidth)
    net.addLink(s6, s11, bw=bandwidth)
    net.addLink(s5, s10, bw=bandwidth)
    net.addLink(s6, s10, bw=bandwidth)

    # Met
    net.addLink(s7, s12, bw=bandwidth)
    net.addLink(s8, s12, bw=bandwidth)
    net.addLink(s9, s12, bw=bandwidth)
    net.addLink(s10, s12, bw=bandwidth)
    net.addLink(s11, s12, bw=bandwidth)

    net.addLink(s9, s13, bw=bandwidth)
    net.addLink(s10, s13, bw=bandwidth)
    net.addLink(s11, s13, bw=bandwidth)
    net.addLink(s11, s14, bw=bandwidth)

    # Core
    net.addLink(s12, s13, bw=core_bw)
    net.addLink(s12, s14, bw=core_bw)
    net.addLink(s13, s14, bw=core_bw)

    net.start()
    net.pingAll()
    REST( net )
    CLI( net )
    net.stop()

    # sshd( net )
