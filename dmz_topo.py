#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSController
import os


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
	    super(LinuxRouter, self).config(**params)
	    self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate( self ):
	    self.cmd('sysctl net.ipv4.ip_forward=0')
	    super(LinuxRouter, self).terminate()


class MyTopo(Topo):
    def build(self, **_opts):
	    
	    # Adding  routers
	    r1 = self.addNode('r1', cls=LinuxRouter, ip=None)
	    r2 = self.addNode('r2', cls=LinuxRouter, ip=None)
	    
	    # Adding hosts of internal network
	    h1 = self.addHost('h1', ip='10.0.0.1/24', defaultRoute='via 10.0.0.254')
	    h2 = self.addHost('h2', ip='10.0.0.2/24', defaultRoute='via 10.0.0.254')

	    # Adding hosts of DMZ
	    d1 = self.addHost('d1', ip='10.0.1.1/24', defaultRoute='via 10.0.1.254')
	    d2 = self.addHost('d2', ip='10.0.1.2/24', defaultRoute='via 10.0.1.254')

	    # Adding host of internet - attacker
	    ext1 = self.addHost('ext1', ip='192.168.0.1/24', defaultRoute='via 192.168.0.254')
	    ext2 = self.addHost('ext2', ip='192.168.0.2/24', defaultRoute='via 192.168.0.254')
	    
	    # Adding switches for the internal network
	    s1 = self.addSwitch('s1')

	    # Adding switches for the DMZ
	    s2 = self.addSwitch('s2')

	    # Adding switches for internet 
	    s3 = self.addSwitch('s3')

	    # Linking hosts and switches
	    self.addLink(h1,s1)
	    self.addLink(h2,s1)
	    self.addLink(d1, s2)
	    self.addLink(d2, s2)
	    self.addLink(ext1,s3)
	    self.addLink(ext2,s3)

	    # Linking switches and routers
	    self.addLink(s1,r1,
			intfName2='r1-eth0', params2={'ip':'10.0.0.254/24'})
	    self.addLink(s2, r1,
			intfName2='r1-eth1', params2={'ip':'10.0.1.254/24'})
	    self.addLink(s3, r2,
			intfName2='r2-eth2', params2={'ip':'192.168.0.254/24'})
	    self.addLink(r1, r2,
			intfName3='r1-eth2', params1={'ip':'10.0.2.254/24'},
			intfName4='r2-eth1', params2={'ip':'10.0.2.253/24'})

def run():
    os.system('sudo fuser -k 6653/tcp')
    net = Mininet(topo=MyTopo())

    net.start()
    
    r1 = net['r1']
    r2 = net['r2']

    # Adding route in iptables to link the two different networks
    r1.cmd('ip route add 192.168.0.0/24 via 10.0.2.253')
    r2.cmd('ip route add 10.0.1.0/24 via 10.0.2.254')
    r2.cmd('ip route add 10.0.0.0/24 via 10.0.2.254')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
