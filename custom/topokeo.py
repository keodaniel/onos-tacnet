from mininet.net import Mininet
from mininet.node import Controller

from mininet.topo import Topo

############################################
### h2 - swA - swA2 - swB - swC - swE - h1
###                      \       /
###                         swD
############################################

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."
        
        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
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
