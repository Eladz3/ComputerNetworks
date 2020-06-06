# ---------------------
# Elad Zohar
# ezohar 1745453
# CSE 150 Spring 2020
# ---------------------

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    
    # Variables ---------------------------------------------
    ip10  = "10.0.1.10"
    ip20  = "10.0.2.20"
    ip30  = "10.0.3.30"
    ip40  = "10.0.4.40"
    ip50  = "10.0.5.50"
    ip60  = "10.0.6.60"
    ip70  = "10.0.7.70"
    ip80  = "10.0.8.80"
    ipSv1 = "10.0.9.10"
    ipUth = "10.0.10.10"

    f1s1_id = 1
    f1s2_id = 2
    f2s1_id = 3
    f2s2_id = 4
    DCS_id  = 5
    CoS_id  = 6

    isICMP = packet.find('icmp')
    isIP = packet.find('ipv4')
    endPort = 1                           # endport is 1 to save lines of code below

    # Timeout ------------------------------------------------
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30

    # Packet filtering ---------------------------------------
    if isIP is not None:
      msg.data = packet_in
      # Floor 1 Switch 1
      if switch_id == f1s1_id:
        if isIP.dstip == ip20:
          endPort = 2
        elif isIP.dstip != ip10:
          endPort = 3
      # Floor 1 Switch 2
      elif switch_id == f1s2_id:
        if isIP.dstip == ip40:
          endPort = 2
        elif isIP.dstip != ip30:
          endPort = 3
      # Floor 2 Switch 1
      elif switch_id == f2s1_id:
        if isIP.dstip == ip60:
          endPort = 2
        elif isIP.dstip != ip50:
          endPort = 3
      # Floor 2 Switch 2
      elif switch_id == f2s2_id:
        if isIP.dstip == ip80:
          endPort = 2
        elif isIP.dstip != ip70:
          endPort = 3
      # Data Center Switch
      elif switch_id == DCS_id and isIP.dstip != ipSv1:
        endPort = 3
      # Core Switch
      elif switch_id == CoS_id:
        endPort = 0                       # reset endPort var. so that it drops undesired packets
        if isICMP is None or isIP.srcip != ipUth:
          if isIP.dstip == ip10 or isIP.dstip == ip20:
            endPort = 1
          elif isIP.dstip == ip30 or isIP.dstip == ip40:
            endPort = 2
          elif isIP.dstip == ip50 or isIP.dstip == ip60:
            endPort = 3
          elif isIP.dstip == ip70 or isIP.dstip == ip80:
            endPort = 4
          elif isIP.dstip == ipUth:
            endPort = 5
          elif isIP.dstip == ipSv1 and isIP.srcip != ipUth:
            endPort = 6
      
      msg.actions.append(of.ofp_action_output(port = endPort))
      self.connection.send(msg)
    
    else:
      msg.data = packet_in
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
