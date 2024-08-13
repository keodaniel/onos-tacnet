import logging
from logging import *
from interact_onos import *
from interact_mininet import *
from time import sleep
import datetime

def post_control_meters(burst_size):
    host_qos = 2000
    voip_qos = 1000
    vtc_qos = 3000
    post_meters("of:0000000000000001", meter_data("of:0000000000000001", host_qos, burst_size))
    post_meters("of:0000000000000002", meter_data("of:0000000000000002", host_qos, burst_size))
    post_meters("of:0000000000000001", meter_data("of:0000000000000001", voip_qos, burst_size))
    post_meters("of:0000000000000002", meter_data("of:0000000000000002", voip_qos, burst_size))
    post_meters("of:0000000000000001", meter_data("of:0000000000000001", vtc_qos, burst_size))
    post_meters("of:0000000000000002", meter_data("of:0000000000000002", vtc_qos, burst_size))

def post_qos_flows(appId):
    h1 = "10.0.10.1/32"
    h2 = "10.0.20.1/32"
    h3 = "10.0.30.1/32"
    h4 = "10.0.10.2/32"
    h5 = "10.0.20.2/32"
    h6 = "10.0.30.2/32"
    h7 = "10.0.10.3/32"
    h8 = "10.0.20.3/32"
    h9 = "10.0.30.3/32"
    priority = 10
    host_vlan = 100
    voip_vlan = 200
    vtc_vlan = 300

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

    host_qos = 2000
    voip_qos = 1000
    vtc_qos = 3000
    sw1_meters = [None, None, None]
    sw2_meters = [None, None, None]
    host_qos_index = 0
    voip_qos_index = 1
    vtc_qos_index = 2
    meters = get_meters()
    for meter in meters:
        if meter[1] == "of:0000000000000001":
            if meter[3] == host_qos:
                sw1_meters[host_qos_index] = meter[0]
            if meter[3] == voip_qos:
                sw1_meters[voip_qos_index] = meter[0]
            if meter[3] == vtc_qos:
                sw1_meters[vtc_qos_index] = meter[0]
        if meter[1] == "of:0000000000000002":
            if meter[3] == host_qos:
                sw2_meters[host_qos_index] = meter[0]
            if meter[3] == voip_qos:
                sw2_meters[voip_qos_index] = meter[0]
            if meter[3] == vtc_qos:
                sw2_meters[vtc_qos_index] = meter[0]

    # Host VLAN Flows
    # h1 to h4
    create_flow_rules(appId, priority, "of:0000000000000001", 1, 4, h1, h4, ethType = "0x800", meter_id=sw1_meters[host_qos_index], match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 4, 1, h4, h1, ethType = "0x800", meter_id=sw1_meters[host_qos_index], match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 1, 4, h4, h1, ethType = "0x800", match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 4, 1, h1, h4, ethType = "0x800", match_vlan=host_vlan)

    # h1 to h7
    create_flow_rules(appId, priority, "of:0000000000000001", 1, 5, h1, h7, ethType = "0x800", meter_id=sw1_meters[host_qos_index], match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 5, 1, h7, h1, ethType = "0x800", meter_id=sw1_meters[host_qos_index], match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 1, 4, h7, h1, ethType = "0x800", match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 4, 1, h1, h7, ethType = "0x800", match_vlan=host_vlan)

    # h4 to h7
    create_flow_rules(appId, priority, "of:0000000000000002", 1, 5, h4, h7, ethType = "0x800", meter_id=sw2_meters[host_qos_index], match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 5, 1, h7, h4, ethType = "0x800", meter_id=sw2_meters[host_qos_index], match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 1, 5, h7, h4, ethType = "0x800", match_vlan=host_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 5, 1, h4, h7, ethType = "0x800", match_vlan=host_vlan)

    # # # VoIP VLAN Flows
    # # # h2 to h5
    create_flow_rules(appId, priority, "of:0000000000000001", 2, 4, h2, h5, ethType = "0x800", meter_id=sw1_meters[voip_qos_index], match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 4, 2, h5, h2, ethType = "0x800", meter_id=sw1_meters[voip_qos_index], match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 2, 4, h5, h2, ethType = "0x800", match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 4, 2, h2, h5, ethType = "0x800", match_vlan=voip_vlan)

    # h2 to h8
    create_flow_rules(appId, priority, "of:0000000000000001", 2, 5, h2, h8, ethType = "0x800", meter_id=sw1_meters[voip_qos_index], match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 5, 2, h8, h2, ethType = "0x800", meter_id=sw1_meters[voip_qos_index], match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 2, 4, h8, h2, ethType = "0x800", match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 4, 2, h2, h8, ethType = "0x800", match_vlan=voip_vlan)

    # # h5 to h8
    create_flow_rules(appId, priority, "of:0000000000000002", 2, 5, h5, h8, ethType = "0x800", meter_id=sw2_meters[voip_qos_index], match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 5, 2, h8, h5, ethType = "0x800", meter_id=sw2_meters[voip_qos_index], match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 2, 5, h8, h5, ethType = "0x800", match_vlan=voip_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 5, 2, h5, h8, ethType = "0x800", match_vlan=voip_vlan)

    # # VTC VLAN Flows
    # # h3 to h6
    create_flow_rules(appId, priority, "of:0000000000000001", 3, 4, h3, h6, ethType = "0x800", meter_id=sw1_meters[vtc_qos_index], match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 4, 3, h6, h3, ethType = "0x800", meter_id=sw1_meters[vtc_qos_index], match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 3, 4, h6, h3, ethType = "0x800", match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 4, 3, h3, h6, ethType = "0x800", match_vlan=vtc_vlan)

    # # h3 to h9
    create_flow_rules(appId, priority, "of:0000000000000001", 3, 5, h3, h9, ethType = "0x800", meter_id=sw1_meters[vtc_qos_index], match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000001", 5, 3, h9, h3, ethType = "0x800", meter_id=sw1_meters[vtc_qos_index], match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 3, 4, h9, h3, ethType = "0x800", match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 4, 3, h3, h9, ethType = "0x800", match_vlan=vtc_vlan)

    # # h6 to h9
    create_flow_rules(appId, priority, "of:0000000000000002", 3, 5, h6, h9, ethType = "0x800", meter_id=sw2_meters[vtc_qos_index], match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000002", 5, 3, h9, h6, ethType = "0x800", meter_id=sw2_meters[vtc_qos_index], match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 3, 5, h9, h6, ethType = "0x800", match_vlan=vtc_vlan)
    create_flow_rules(appId, priority, "of:0000000000000003", 5, 3, h6, h9, ethType = "0x800", match_vlan=vtc_vlan)

datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
filename = f"{datestring} qos_test"
logging.basicConfig(filename=f'logs/{filename}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
purge_meters()
purge_flow_rules("keo")
post_control_meters(100)
post_qos_flows("keo")
