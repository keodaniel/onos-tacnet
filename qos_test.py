import logging
from logging import *
import os
from interact_onos import *
from interact_mininet import *
from time import sleep
import datetime

def post_qos_meters(burst_size):
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
    sw3_meters = [None, None, None]
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

def qos_test(filename, trials, burst_size):
    test_name = "QoS VLAN Test"
    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime("%Y-%m-%d-%H%M")
    topo = "VLAN"
    sleep_time = 5
    appId = "keo"
    vlan_connectivity_success = True
    qos_test_log_path1 = f"iperf/qos1.log"
    qos_test_log_path2 = f"iperf/qos2.log"
    qos_test_log_path3 = f"iperf/qos3.log"
    hostvlan_output = []
    voipvlan_output = []
    vtcvlan_output = []
    successful_runs = 0
    trial_runs = trials

    logging.info(f"Starting {test_name} test at {start_time_str}")
    print(f"Starting {test_name} test at {start_time_str}")

    try:
        # Starting actions
        start_onos_docker()

    except Exception as e:
        logging.error(f"Error restarting ONOS docker: {e}")
        
    while successful_runs < trial_runs:

        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()
        toggle_fwd("deactivate")

        purge_flow_rules(appId)
        post_qos_meters(burst_size)
        post_qos_flows(appId)

        # Start pingall
        sleep(sleep_time)
        mininet_process.send_command("pingall", check_stdout=True)
        cmd_output = mininet_process.read_stderr("*** Results")
        
        # Checking results
        if "h1 -> X X h4 X X h7 X X" in cmd_output:
            logging.info("Host VLAN 100 successful")
            print("Host VLAN 100 successful")
        else:
            logging.error("Host VLAN 100 failed")
            print("Host VLAN 100 failed")
            vlan_connectivity_success = False
        if "h2 -> X X X h5 X X h8 X" in cmd_output:
            logging.info("VoIP VLAN 200 successful")
            print("VoIP VLAN 200 successful")
        else:
            logging.error("VoIP VLAN 200 failed")
            print("VoIP VLAN 200 failed")
            vlan_connectivity_success = False
        if "h3 -> X X X X h6 X X h9" in cmd_output:
            logging.info("VTC VLAN 300 successful")
            print("VTC VLAN 300 successful")
        else:
            logging.error("VTC VLAN 300 failed")
            print("VTC VLAN 300 failed")
            vlan_connectivity_success = False

        if vlan_connectivity_success:
            logging.info(f"VLAN connectivity successful")
            print(f"VLAN connectivity successful")
            failed_runs = 0
        else:
            logging.error(f"VLAN connectivity test failed")
            print(f"VLAN connectivity test failed")
            failed_runs = 1

        # Start iperf servers
        sleep(sleep_time)
        mininet_process.send_command("h1 iperf3 -s &", check_stdout=True)
        mininet_process.send_command("h2 iperf3 -s &", check_stdout=True)
        mininet_process.send_command("h3 iperf3 -s &", check_stdout=True)
        sleep(sleep_time)

        while successful_runs < trial_runs:
            if failed_runs > 0:
                logging.info(f"Trial {successful_runs+1} failed, restarting mininet")
                print(f"Trial {successful_runs+1} failed, restarting mininet")
                break
        
            try:
                # Simultaneous iperf tests between Battalion A and NOC

                # Host VLAN 100
                mininet_process.send_command(f"h7 iperf3 -c 10.0.10.1 -b 5Mbps > {qos_test_log_path1} &", check_stdout=True)
                # VoIP VLAN 200
                mininet_process.send_command(f"h8 iperf3 -c 10.0.20.1 -b 5Mbps -u > {qos_test_log_path2} &", check_stdout=True)
                # VTC VLAN 300
                mininet_process.send_command(f"h9 iperf3 -c 10.0.30.1 -b 5Mbps -u > {qos_test_log_path3} &", check_stdout=True)
                
                # Get iperf output
                logging.info("h4 to h1 iperf output")
                hostvlan_output.extend(mininet_process.read_iperf3_logfile(qos_test_log_path1))
                logging.info("h5 to h2 iperf output")
                voipvlan_output.extend(mininet_process.read_iperf3_logfile(qos_test_log_path2))
                logging.info("h6 to h3 iperf output")
                vtcvlan_output.extend(mininet_process.read_iperf3_logfile(qos_test_log_path3))

                successful_runs += 1
                logging.info(f"{test_name} Test Trial {successful_runs} Success")
                timestring = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"{test_name} Test Trial {successful_runs} Success, time: {timestring}")

            except Exception as e:
                failed_runs += 1
                logging.error(f"Error during trial {successful_runs+1}: {e}")
                print(f"Error during trial {successful_runs+1}: {e}")

        # Closing actions
        mininet_process.process.stdin.close()
        mininet_process.read_stderr("Done")

    # write to output
    with open(f"logs/{start_time_str}_hostvlan.log", "w") as f:
        f.write("\n".join(hostvlan_output))
    with open(f"logs/{start_time_str}_voipvlan.log", "w") as f:
        f.write("\n".join(voipvlan_output))
    with open(f"logs/{start_time_str}_vtcvlan.log", "w") as f:
        f.write("\n".join(vtcvlan_output))

    elapsed_time = (datetime.datetime.now() - start_time)
    logging.info(f"{test_name} test done, elapsed time: {elapsed_time}")
    print(f"Elapsed time: {elapsed_time}")
    return True
    
def main():
    burst_size = None
    while True:
        try:
            trials = int(input("Enter number of trials (1-20): "))
            if 1 <= trials <= 20:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 20.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 20.")
            continue

    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    if not os.path.exists('logs'):
        os.makedirs('logs')
    filename = f"{datestring} qos_test {burst_size} Burst Size {trials} trials"
    logging.basicConfig(filename=f'logs/{filename}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    qos_test(filename, trials, burst_size)

if __name__ == "__main__":
    main()

