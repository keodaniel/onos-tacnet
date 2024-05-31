import logging
from logging import *
from interact_onos import *
from interact_mininet import *
from time import sleep
import datetime

def bw_control_meters():
    purge_meters()
    post_meters("of:0000000000000001", meter_data("of:0000000000000001", 3000))
    post_meters("of:0000000000000002", meter_data("of:0000000000000002", 1500))
    post_meters("of:0000000000000002", meter_data("of:0000000000000002", 1500))

def test_flow_rules():
    h1 = "10.0.10.1/32"
    h3 = "10.0.20.1/32"
    appId = "keo"
    priority = 10
    TCP = 6
    UDP = 17

    purge_flow_rules(appId)

    # Direct Path from h1 to h3
    create_flow_rules(appId, priority, "of:0000000000000001", 1, 3, h1, h3)
    create_flow_rules(appId, priority, "of:0000000000000001", 3, 1, h3, h1)
    create_flow_rules(appId, priority, "of:0000000000000002", 3, 1, h1, h3)
    create_flow_rules(appId, priority, "of:0000000000000002", 1, 3, h3, h1)

def bw_control_flow_rules():
    h1 = "10.0.10.1/32"
    h3 = "10.0.20.1/32"
    h6 = "10.0.30.2/32"
    appId = "keo"
    priority = 10
    TCP = 6
    UDP = 17

    purge_flow_rules(appId)

    sw1_meters = []
    sw2_meters = []
    meters = get_meters()
    for meter in meters:
        if meter[1] == "of:0000000000000001":
            sw1_meters.append(meter[0])
        if meter[1] == "of:0000000000000002":
            sw2_meters.append(meter[0])

    
    # Direct Path from h3 to h6
    create_flow_rules(appId, priority, "of:0000000000000003", 2, 4, h6, h3, ethType = "0x800", ip_proto=None)
    create_flow_rules(appId, priority, "of:0000000000000003", 4, 2, h3, h6, ethType = "0x800", ip_proto=None)
    create_flow_rules(appId, priority, "of:0000000000000002", 4, 1, h6, h3, ethType = "0x800", ip_proto=None, meter_id=sw2_meters[0])
    create_flow_rules(appId, priority, "of:0000000000000002", 1, 4, h3, h6, ethType = "0x800", ip_proto=None, meter_id=sw2_meters[0])

    # Indirect Path from h3 to h6 through h1
    create_flow_rules(appId, priority, "of:0000000000000003", 2, 3, h6, h3, ethType = "0x800", ip_proto=UDP)
    create_flow_rules(appId, priority, "of:0000000000000003", 3, 2, h3, h6, ethType = "0x800", ip_proto=UDP)
    create_flow_rules(appId, priority, "of:0000000000000001", 4, 3, h6, h3, ethType = "0x800", ip_proto=UDP)
    create_flow_rules(appId, priority, "of:0000000000000001", 3, 4, h3, h6, ethType = "0x800", ip_proto=UDP)
    create_flow_rules(appId, priority, "of:0000000000000002", 3, 1, h6, h3, ethType = "0x800", ip_proto=UDP, meter_id=sw2_meters[1])
    create_flow_rules(appId, priority, "of:0000000000000002", 1, 3, h3, h6, ethType = "0x800", ip_proto=UDP, meter_id=sw2_meters[1])

    # Direct Path from h1 to h6
    create_flow_rules(appId, priority, "of:0000000000000003", 2, 3, h6, h1, ethType = "0x800", ip_proto=None)
    create_flow_rules(appId, priority, "of:0000000000000003", 3, 2, h1, h6, ethType = "0x800", ip_proto=None)
    create_flow_rules(appId, priority, "of:0000000000000001", 4, 1, h6, h1, ethType = "0x800", ip_proto=None, meter_id=sw1_meters[0])
    create_flow_rules(appId, priority, "of:0000000000000001", 1, 4, h1, h6, ethType = "0x800", ip_proto=None, meter_id=sw1_meters[0])

datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
filename = f"{datestring} bw_control_test"
logging.basicConfig(filename=f'logs/{filename}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
bw_control_meters()
bw_control_flow_rules()
# test_flow_rules()




