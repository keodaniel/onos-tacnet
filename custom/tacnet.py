from mininet.net import Mininet
from mininet.node import Controller
from mininet.node import Host
from mininet.topo import Topo
from mininet.link import TCLink
# edit

topos = {
    'base': ( lambda: Base() ), 
    'DFGW': ( lambda: DFGateway() ),
    'BW': ( lambda: Bandwidth() )
    }

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
  
