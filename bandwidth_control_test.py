import logging
from logging import *
from interact_onos import *
from interact_mininet import *
from time import sleep
import datetime

def post_control_meters():
    post_meters("of:0000000000000001", meter_data("of:0000000000000001", 3000))
    post_meters("of:0000000000000002", meter_data("of:0000000000000002", 1500))
    post_meters("of:0000000000000002", meter_data("of:0000000000000002", 1500))

def post_control_flows(appId):
    h1 = "10.0.10.1/32"
    h3 = "10.0.20.1/32"
    h6 = "10.0.30.2/32"
    priority = 10
    udp_priority = 20
    TCP = 6
    UDP = 17

    sw1_meters = []
    sw2_meters = []
    meters = get_meters()
    for meter in meters:
        if meter[1] == "of:0000000000000001":
            sw1_meters.append(meter[0])
        if meter[1] == "of:0000000000000002":
            sw2_meters.append(meter[0])

    # Direct Path from h3 to h6
    create_flow_rules(appId, priority, "of:0000000000000003", 2, 4, h6, h3, ip_proto=None)
    create_flow_rules(appId, priority, "of:0000000000000003", 4, 2, h3, h6, ip_proto=None)
    create_flow_rules(appId, priority, "of:0000000000000002", 4, 1, h6, h3, ip_proto=None, meter_id=sw2_meters[0])
    create_flow_rules(appId, priority, "of:0000000000000002", 1, 4, h3, h6, ip_proto=None, meter_id=sw2_meters[0])

    # Indirect Path from h3 to h6 through h1
    create_flow_rules(appId, udp_priority, "of:0000000000000003", 2, 3, h6, h3, ip_proto=UDP)
    create_flow_rules(appId, udp_priority, "of:0000000000000003", 3, 2, h3, h6, ip_proto=UDP)
    create_flow_rules(appId, udp_priority, "of:0000000000000001", 4, 3, h6, h3, ip_proto=UDP)
    create_flow_rules(appId, udp_priority, "of:0000000000000001", 3, 4, h3, h6, ip_proto=UDP)
    create_flow_rules(appId, udp_priority, "of:0000000000000002", 3, 1, h6, h3, ip_proto=UDP, meter_id=sw2_meters[1])
    create_flow_rules(appId, udp_priority, "of:0000000000000002", 1, 3, h3, h6, ip_proto=UDP, meter_id=sw2_meters[1])

    # Direct Path from h1 to h6
    create_flow_rules(appId, priority, "of:0000000000000003", 2, 3, h6, h1, ip_proto=None)
    create_flow_rules(appId, priority, "of:0000000000000003", 3, 2, h1, h6, ip_proto=None)
    create_flow_rules(appId, priority, "of:0000000000000001", 4, 1, h6, h1, ip_proto=None, meter_id=sw1_meters[0])
    create_flow_rules(appId, priority, "of:0000000000000001", 1, 4, h1, h6, ip_proto=None, meter_id=sw1_meters[0])

def bw_control_test():
    test_name = "Bandwidth Control"
    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime("%Y-%m-%d-%H%M")
    topo = "TC"
    sleep_time = 5
    appId = "keo"

    logging.info(f"Starting {test_name} test at {start_time_str}")
    print(f"Starting {test_name} test at {start_time_str}")

    try:
        # Starting actions
        start_onos_docker()

    except Exception as e:
        logging.error(f"Error restarting ONOS docker: {e}")
        
    try:
        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()

        purge_meters()
        purge_flow_rules(appId)

        post_control_meters()
        post_control_flows(appId)

        # Start iperf server
        sleep(sleep_time)
        mininet_process.send_command("h6 iperf3 -s &", check_stdout=True)
        sleep(sleep_time)


        bw_test_log_path = f"iperf/bw.log"

        # h3 to h6 direct
        mininet_process.send_command(f"h3 iperf3 -c 10.0.30.2 -b 10Mbps > {bw_test_log_path} &", check_stdout=True)
        logging.info("h3 to h6 direct iperf output")
        mininet_process.read_iperf3_logfile(bw_test_log_path)

        # h3 to h6 indirect UDP
        mininet_process.send_command(f"h3 iperf3 -c 10.0.30.2 -u -b 10Mbps > {bw_test_log_path} &", check_stdout=True)
        logging.info("h3 to h6 indirect UDP iperf output")
        mininet_process.read_iperf3_logfile(bw_test_log_path)

        # h1 to h6 direct
        mininet_process.send_command(f"h1 iperf3 -c 10.0.30.2 -b 10Mbps > {bw_test_log_path} &", check_stdout=True)
        logging.info("h1 to h6 direct iperf output")
        mininet_process.read_iperf3_logfile(bw_test_log_path)

        get_meters(log=True)

        mininet_process.process.stdin.close()
        mininet_process.read_stderr("Done")

    except Exception as e:
        logging.error(f"Error during test: {e}")
        print(f"Error during test: {e}")

        # Closing actions
        mininet_process.process.stdin.close()
        mininet_process.read_stderr("Done")

    elapsed_time = (datetime.datetime.now() - start_time)
    logging.info(f"{test_name} test done, elapsed time: {elapsed_time}")
    print(f"Elapsed time: {elapsed_time}")
    return True
    
def main():
    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} bw_control_test"
    logging.basicConfig(filename=f'logs/{filename}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    bw_control_test()
if __name__ == "__main__":
    main()

