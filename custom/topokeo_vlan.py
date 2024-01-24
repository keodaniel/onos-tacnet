from mininet.net import Mininet
from mininet.node import Controller

from mininet.node import Host
from mininet.topo import Topo

class VLANHost( Host ):
    "Host connected to VLAN interface"

    # pylint: disable=arguments-differ
    def config( self, vlan=100, **params ):
        """Configure VLANHost according to (optional) parameters:
           vlan: VLAN ID for default interface"""

        r = super( VLANHost, self ).config( **params )

        intf = self.defaultIntf()
        # remove IP from default, "physical" interface
        self.cmd( 'ifconfig %s inet 0' % intf )
        # create VLAN interface
        self.cmd( 'vconfig add %s %d' % ( intf, vlan ) )
        # assign the host's IP to the VLAN interface
        self.cmd( 'ifconfig %s.%d inet %s' % ( intf, vlan, params['ip'] ) )
        # update the intf name and host's intf map
        newName = '%s.%d' % ( intf, vlan )
        # update the (Mininet) interface to refer to VLAN interface name
        intf.name = newName
        # add VLAN interface to host's name to intf map
        self.nameToIntf[ newName ] = intf

        return r


hosts = { 'vlan': VLANHost }

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."
        
        # Add hosts and switches
        h1 = self.addHost('h1', cls=VLANHost, vlan=100)
        h2 = self.addHost('h2', cls=VLANHost, vlan=200)
        swA = self.addSwitch('s1')
        swA2 = self.addSwitch('s2')
        swB = self.addSwitch('s3')
        swC = self.addSwitch('s4')
        swD = self.addSwitch('s5')
        swE = self.addSwitch('s6')

        # Add links
        self.addLink(h2, swA)
        self.addLink(swA, swA2)
        self.addLink(swA2, swB)
        self.addLink(swB, swC)
        self.addLink(swB, swD)
        self.addLink(swD, swE)
        self.addLink(swC, swE)
        self.addLink(swE, h1)


topos = { 'topokeo': ( lambda: MyTopo() ) }
# net = Mininet
# print(net.items())
