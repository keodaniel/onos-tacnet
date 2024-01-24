from mininet.net import Mininet
from mininet.node import Controller

from mininet.node import Host
from mininet.topo import Topo



class MyTopo( Topo ):
    "Simple topology example."

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
        

topos = { 'custom_tacnet': ( lambda: MyTopo() ) }
