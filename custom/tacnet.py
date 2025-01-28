from mininet.net import Mininet
from mininet.node import Controller
from mininet.node import Host
from mininet.topo import Topo
from mininet.link import TCLink
from functools import partial

topos = {
    'base': ( lambda: Base() ), 
    'DFGW': ( lambda: DFGateway() ),
    'TC': ( lambda: TC() ),
    'BW': ( lambda: Bandwidth() ),
    'VLAN': ( lambda: Vlan() )
    }

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

class Base( Topo ):
    """Basic tacnet topology with assigned IPs"""

    def build( self ):
        "Create custom topo."
        
        # Add hosts and switches
        h1 = self.addHost('h1', ip='10.0.10.1/24')
        h2 = self.addHost('h2', ip='10.0.10.2/24')
        h3 = self.addHost('h3', ip='10.0.20.1/24')
        h4 = self.addHost('h4', ip='10.0.20.2/24')
        h5 = self.addHost('h5', ip='10.0.30.1/24')
        h6 = self.addHost('h6', ip='10.0.30.2/24')
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
        
        # Interunit Links
        self.addLink(s1, s2)
        
        # Backhaul Links
        self.addLink(s1, s3)
        self.addLink(s2, s3)

class DFGateway( Topo ):
    """Adding default routes / default gateway\n
    Without default gateways, hosts can only connect within their subnet"""

    def build( self ):
        "Create custom topo."
        
        # Add hosts and switches
        h1 = self.addHost('h1', ip='10.0.10.1/24', defaultRoute='via 10.0.10.1')
        h2 = self.addHost('h2', ip='10.0.10.2/24', defaultRoute='via 10.0.10.2')
        h3 = self.addHost('h3', ip='10.0.20.1/24', defaultRoute='via 10.0.20.1')
        h4 = self.addHost('h4', ip='10.0.20.2/24', defaultRoute='via 10.0.20.2')
        h5 = self.addHost('h5', ip='10.0.30.1/24', defaultRoute='via 10.0.30.1')
        h6 = self.addHost('h6', ip='10.0.30.2/24', defaultRoute='via 10.0.30.2')
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
        
        # Interunit Links
        self.addLink(s1, s2)

        # Backhaul Links
        self.addLink(s1, s3)
        self.addLink(s2, s3)

class TC( Topo ):
    """Traffic Control (TC) Links between units"""

    def build( self ):
        "Create custom topo."
        
        # Add hosts and switches
        h1 = self.addHost('h1', ip='10.0.10.1/24', defaultRoute='via 10.0.10.1')
        h2 = self.addHost('h2', ip='10.0.10.2/24', defaultRoute='via 10.0.10.2')
        h3 = self.addHost('h3', ip='10.0.20.1/24', defaultRoute='via 10.0.20.1')
        h4 = self.addHost('h4', ip='10.0.20.2/24', defaultRoute='via 10.0.20.2')
        h5 = self.addHost('h5', ip='10.0.30.1/24', defaultRoute='via 10.0.30.1')
        h6 = self.addHost('h6', ip='10.0.30.2/24', defaultRoute='via 10.0.30.2')
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
        
        # Interunit Links
        self.addLink(s1, s2, cls=TCLink, bw=50, delay="10ms") # 50Mbps interunit link WPPL-T approx 1ms

        # Backhaul Links
        self.addLink(s1, s3, cls=TCLink, bw=10, delay="10ms") # 10Mbps backhaul link VSAT-L approx propagation delay to satellite
        self.addLink(s2, s3, cls=TCLink, bw=5, delay="10ms") # 5Mbps backhaul link VSAT-E
        
class Bandwidth( Topo ):
    """Implemented TC Links between units\n
    10MBps between s1 and s2 (Interunit link)\n
    5MBps between s1 and s3 (Battalion A backhaul)\n
    1MBps between s2 and s3 (Battalion B backhaul)"""

    def build( self ):
        "Create custom topo."
        
        # Add hosts and switches
        h1 = self.addHost('h1', ip='10.0.10.1/24', defaultRoute='via 10.0.10.1')
        h2 = self.addHost('h2', ip='10.0.20.1/24', defaultRoute='via 10.0.20.1')
        h3 = self.addHost('h3', ip='10.0.30.1/24', defaultRoute='via 10.0.30.1')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        
        # Interunit Links
        self.addLink(s1, s2, cls=TCLink, bw=10)

        # Backhaul Links
        self.addLink(s1, s3, cls=TCLink, bw=5)
        self.addLink(s2, s3, cls=TCLink, bw=1)


class Vlan( Topo ):
    """VLAN Host with assigned VLANs"""

    def build( self ):
        "Create custom topo."
        host_vlan = 100
        voip_vlan = 200
        vtc_vlan = 300
        
        # Add hosts and switches
        h1 = self.addHost('h1', ip='10.0.10.1/24', defaultRoute='via 10.0.10.1', cls=VLANHost, vlan=host_vlan)
        h2 = self.addHost('h2', ip='10.0.20.1/24', defaultRoute='via 10.0.20.1', cls=VLANHost, vlan=voip_vlan)
        h3 = self.addHost('h3', ip='10.0.30.1/24', defaultRoute='via 10.0.30.1', cls=VLANHost, vlan=vtc_vlan)
        h4 = self.addHost('h4', ip='10.0.10.2/24', defaultRoute='via 10.0.10.2', cls=VLANHost, vlan=host_vlan)
        h5 = self.addHost('h5', ip='10.0.20.2/24', defaultRoute='via 10.0.20.2', cls=VLANHost, vlan=voip_vlan)
        h6 = self.addHost('h6', ip='10.0.30.2/24', defaultRoute='via 10.0.30.2', cls=VLANHost, vlan=vtc_vlan)
        h7 = self.addHost('h7', ip='10.0.10.3/24', defaultRoute='via 10.0.10.3', cls=VLANHost, vlan=host_vlan)
        h8 = self.addHost('h8', ip='10.0.20.3/24', defaultRoute='via 10.0.20.3', cls=VLANHost, vlan=voip_vlan)
        h9 = self.addHost('h9', ip='10.0.30.3/24', defaultRoute='via 10.0.30.3', cls=VLANHost, vlan=vtc_vlan)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s2)
        self.addLink(h5, s2)
        self.addLink(h6, s2)
        self.addLink(h7, s3)
        self.addLink(h8, s3)
        self.addLink(h9, s3)
        
        # Interunit Links
        self.addLink(s1, s2, cls=TCLink, bw=50, delay="10ms") # 50Mbps interunit link WPPL-T approx 1ms

        # Backhaul Links
        self.addLink(s1, s3, cls=TCLink, bw=10, delay="10ms") # 10Mbps backhaul link VSAT-L approx propagation delay to satellite
        self.addLink(s2, s3, cls=TCLink, bw=5, delay="10ms") # 5Mbps backhaul link VSAT-E