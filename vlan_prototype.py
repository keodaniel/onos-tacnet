import logging
from logging import *
from interact_onos import *
from interact_mininet import *
from time import sleep
import datetime

def vlan_flow_rules():
    h1 = "10.0.10.1/32"
    h2 = "10.0.20.1/32"
    h3 = "10.0.30.1/32"
    h4 = "10.0.10.2/32"
    h5 = "10.0.20.2/32"
    h6 = "10.0.30.2/32"
    h7 = "10.0.10.3/32"
    h8 = "10.0.20.3/32"
    h9 = "10.0.30.3/32"
    appId = "vlan"
    priority = 10
    host_vlan = 100
    voip_vlan = 200
    vtc_vlan = 300

    purge_flow_rules(appId)

    # Mininet Topology
    # h1-eth0.100<->s1-eth1 (OK OK) 
    # h2-eth0.200<->s1-eth2 (OK OK) 
    # h3-eth0.300<->s1-eth3 (OK OK) 
    # h4-eth0.100<->s2-eth1 (OK OK) 
    # h5-eth0.200<->s2-eth2 (OK OK) 
    # h6-eth0.300<->s2-eth3 (OK OK) 
    # h7-eth0.100<->s3-eth1 (OK OK) 
    # h8-eth0.200<->s3-eth2 (OK OK) 
    # h9-eth0.300<->s3-eth3 (OK OK) 
    # s1-eth4<->s2-eth4 (OK OK) 
    # s1-eth5<->s3-eth4 (OK OK) 
    # s2-eth5<->s3-eth5 (OK OK) 

    # Host VLAN Flows
    # h1 to h4
    create_flow_rules(appId, priority, "of:0000000000000001", 1, 4, h1, h4, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 4, 1, h4, h1, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 1, 4, h4, h1, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 4, 1, h1, h4, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)

    # h1 to h7
    create_flow_rules(appId, priority, "of:0000000000000001", 1, 5, h1, h7, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 5, 1, h7, h1, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 1, 4, h7, h1, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 4, 1, h1, h7, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)

    # h4 to h7
    create_flow_rules(appId, priority, "of:0000000000000002", 1, 5, h4, h7, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 5, 1, h7, h4, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 5, 1, h7, h4, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 1, 5, h4, h7, ethType = "0x800", ip_proto=None, match_vlan=host_vlan)

    # VoIP VLAN Flows
    # h2 to h5
    create_flow_rules(appId, priority, "of:0000000000000001", 2, 4, h2, h5, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 4, 2, h5, h2, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 4, 2, h5, h2, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 2, 4, h2, h5, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)

    # h2 to h8
    create_flow_rules(appId, priority, "of:0000000000000001", 2, 5, h2, h8, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 5, 2, h8, h2, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 4, 2, h8, h2, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 2, 4, h2, h8, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)

    # h5 to h8
    create_flow_rules(appId, priority, "of:0000000000000002", 2, 5, h5, h8, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 5, 2, h8, h5, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 5, 2, h8, h5, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 2, 5, h5, h8, ethType = "0x800", ip_proto=None, match_vlan=voip_vlan)

    # VTC VLAN Flows
    # h3 to h6
    create_flow_rules(appId, priority, "of:0000000000000001", 3, 4, h3, h6, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 4, 3, h6, h3, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 4, 3, h6, h3, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 3, 4, h3, h6, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)

    # h3 to h9
    create_flow_rules(appId, priority, "of:0000000000000001", 3, 5, h3, h9, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 5, 3, h9, h3, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 4, 3, h9, h3, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 3, 4, h3, h9, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)

    # h6 to h9
    create_flow_rules(appId, priority, "of:0000000000000002", 3, 5, h6, h9, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 5, 3, h9, h6, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 5, 3, h9, h6, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 3, 5, h6, h9, ethType = "0x800", ip_proto=None, match_vlan=vtc_vlan)

datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
filename = f"{datestring} vlan_test"
logging.basicConfig(filename=f'logs/{filename}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
vlan_flow_rules()

