# ---------------------
# Elad Zohar
# ezohar 1745453
# CSE 150 Spring 2020
# ---------------------

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Creating the 8 hosts, server and untrusted host.
    # Untrusted host IP was modified to 10.0.10.10 to ensure code works
    h10 = self.addHost('h10',mac='00:00:00:00:00:01',ip='10.0.1.10', defaultRoute="h10-eth0")
    h20 = self.addHost('h20',mac='00:00:00:00:00:02',ip='10.0.2.20', defaultRoute="h20-eth0")
    h30 = self.addHost('h30',mac='00:00:00:00:00:03',ip='10.0.3.30', defaultRoute="h30-eth0")
    h40 = self.addHost('h40',mac='00:00:00:00:00:04',ip='10.0.4.40', defaultRoute="h40-eth0")
    h50 = self.addHost('h50',mac='00:00:00:00:00:05',ip='10.0.5.50', defaultRoute="h50-eth0")
    h60 = self.addHost('h60',mac='00:00:00:00:00:06',ip='10.0.6.60', defaultRoute="h60-eth0")
    h70 = self.addHost('h70',mac='00:00:00:00:00:07',ip='10.0.7.70', defaultRoute="h70-eth0")
    h80 = self.addHost('h80',mac='00:00:00:00:00:08',ip='10.0.8.80', defaultRoute="h90-eth0")
    sv1 = self.addHost('sv1',mac='00:00:00:00:00:09',ip='10.0.9.10', defaultRoute="sv1-eth0")
    uth = self.addHost('uth',mac='00:00:00:00:00:10',ip='10.0.10.10', defaultRoute="uth-eth0")
    
    # Creating the 6 switches for the network
    f1s1 = self.addSwitch('s1') # Floor 1 Switch 1
    f1s2 = self.addSwitch('s2') # Floor 1 Switch 2
    f2s1 = self.addSwitch('s3') # Floor 2 Switch 1
    f2s2 = self.addSwitch('s4') # Floor 2 Switch 2
    DCS = self.addSwitch('s5')  # Data Center Switch
    CoS = self.addSwitch('s6')  # Core Switch

    # Creating links from network hosts to their respective switch 
    self.addLink(h10,f1s1, port1=1, port2=1)
    self.addLink(h20,f1s1, port1=1, port2=2)
    self.addLink(h30,f1s2, port1=1, port2=1)
    self.addLink(h40,f1s2, port1=1, port2=2)
    self.addLink(h50,f2s1, port1=1, port2=1)
    self.addLink(h60,f2s1, port1=1, port2=2)
    self.addLink(h70,f2s2, port1=1, port2=1)
    self.addLink(h80,f2s2, port1=1, port2=2)
    self.addLink(sv1,DCS,  port1=1, port2=1)
    # Creating links from switches to the Core Switch
    self.addLink(f1s1,CoS, port1=3, port2=1)
    self.addLink(f1s2,CoS, port1=3, port2=2)
    self.addLink(f2s1,CoS, port1=3, port2=3)
    self.addLink(f2s2,CoS, port1=3, port2=4)
    self.addLink(uth,CoS,  port1=1, port2=5)
    self.addLink(DCS,CoS,  port1=3, port2=6)

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  #net = Mininet(topo=topo)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
