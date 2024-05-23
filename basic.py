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

	    '''
	        h1 <-> r1 <-> h2
	    '''	    

	    # Adding  routers
	    r1 = self.addNode('r1', cls=LinuxRouter, ip=None)

	    # Adding hosts
	    h1 = self.addHost('h1', ip=None, defaultRoute='via 10.0.1.254')
	    h2 = self.addHost('h2', ip=None, defaultRoute='via 10.0.2.254')
	    
	    # Linking routers with hosts
	    self.addLink(h1,r1,
		         intfName1='h1-eth0',params1={'ip':'10.0.1.1/24'},
		         intfName2='r1-eth0',params2={'ip':'10.0.1.254/24'})	   	         
	    self.addLink(h2,r1,
		         intfName1='h2-eth2',params1={'ip':'10.0.2.2/24'},
		         intfName2='r1-eth1',params2={'ip':'10.0.2.254/24'})
	    
def run():
    os.system('sudo fuser -k 6653/tcp')
    net = Mininet(topo=MyTopo())

    net.start()
    
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
