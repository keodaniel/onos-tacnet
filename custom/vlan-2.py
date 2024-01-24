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
        h1 = self.addHost('h1', cls=VLANHost, vlan=100, ip='10.0.0.1/24')
        h2 = self.addHost('h2', cls=VLANHost, vlan=200, ip='10.0.0.2/24')
        h3 = self.addHost('h3', cls=VLANHost, vlan=100, ip='10.0.0.3/24')
        h4 = self.addHost('h4', cls=VLANHost, vlan=200, ip='10.0.0.4/24')
        h5 = self.addHost('h5', cls=VLANHost, vlan=300, ip='10.0.0.5/24')
        h6 = self.addHost('h6', cls=VLANHost, vlan=300, ip='10.0.0.6/24')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)
        self.addLink(h6, s3)
        self.addLink(s1, s2)
        self.addLink(s2, s3)

topos = { 'vlan_same_net': ( lambda: MyTopo() ) }
