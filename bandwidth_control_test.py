import logging
from logging import *
from interact_onos import *
from interact_mininet import *
from time import sleep
import datetime

def post_control_meters(burst_size):
    post_meters("of:0000000000000001", meter_data("of:0000000000000001", 6000, burst_size))
    post_meters("of:0000000000000002", meter_data("of:0000000000000002", 3000, burst_size))
    post_meters("of:0000000000000002", meter_data("of:0000000000000002", 3000, burst_size))

def post_control_flows(appId):
    h1 = "10.0.10.1/32"
    h3 = "10.0.20.1/32"
    h6 = "10.0.30.2/32"
    priority = 10
    udp_priority = 10
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

def bw_control_test(filename, trials, burst_size):
    test_name = "Bandwidth Control"
    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime("%Y-%m-%d-%H%M")
    topo = "TC"
    sleep_time = 5
    appId = "keo"
    h3h6_direct_output = []
    h3h6_indirect_udp_output = []
    h1h6_direct_output = []
    successful_runs = 0
    trial_runs = trials
    bw_test_log_path1 = f"iperf/bw1.log"
    bw_test_log_path2 = f"iperf/bw2.log"
    bw_test_log_path3 = f"iperf/bw3.log"

    logging.info(f"Starting {test_name} test at {start_time_str}")
    print(f"Starting {test_name} test at {start_time_str}")

    try:
        # Starting actions
        start_onos_docker()

    except Exception as e:
        logging.error(f"Error restarting ONOS docker: {e}")

    # 20 trials
    while successful_runs < trial_runs:

        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()

        purge_meters()
        purge_flow_rules(appId)

        post_control_meters(burst_size)
        post_control_flows(appId)


        # Start iperf server
        sleep(sleep_time)
        mininet_process.send_command("h6 iperf3 -s &", check_stdout=True)
        sleep(sleep_time)

        failed_runs = 0

        while successful_runs < trial_runs:
            if failed_runs > 0:
                logging.info(f"Trial {successful_runs+1} failed, restarting mininet")
                print(f"Trial {successful_runs+1} failed, restarting mininet")
                break

            try:
                # h3 to h6 direct
                mininet_process.send_command(f"h3 iperf3 -c 10.0.30.2 -b 10Mbps > {bw_test_log_path1} &", check_stdout=True)
                logging.info("h3 to h6 direct iperf output")
                h3h6_direct_output.extend(mininet_process.read_iperf3_logfile(bw_test_log_path1))

                # h3 to h6 indirect UDP
                mininet_process.send_command(f"h3 iperf3 -c 10.0.30.2 -u -b 10Mbps > {bw_test_log_path2} &", check_stdout=True)
                logging.info("h3 to h6 indirect UDP iperf output")
                h3h6_indirect_udp_output.extend(mininet_process.read_iperf3_logfile(bw_test_log_path2))

                # h1 to h6 direct
                mininet_process.send_command(f"h1 iperf3 -c 10.0.30.2 -b 10Mbps > {bw_test_log_path3} &", check_stdout=True)
                logging.info("h1 to h6 direct iperf output")
                h1h6_direct_output.extend(mininet_process.read_iperf3_logfile(bw_test_log_path3))

                successful_runs += 1
                logging.info(f"{test_name} Test Trial {successful_runs} Success")
                timestring = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"{test_name} Test Trial {successful_runs} Success, time: {timestring}")
                # sleep(sleep_time)

            except Exception as e:
                failed_runs += 1
                logging.error(f"Error during trial {successful_runs+1}: {e}")
                print(f"Error during trial {successful_runs+1}: {e}")

        get_meters(log=True)

        # Closing actions
        mininet_process.process.stdin.close()
        mininet_process.read_stderr("Done")

    # Write iperf output to log file
    with open(f"logs/{filename}_h3h6_direct.log", "w") as f:
        f.write("\n".join(h3h6_direct_output))
    with open(f"logs/{filename}_h3h6_indirect_udp.log", "w") as f:
        f.write("\n".join(h3h6_indirect_udp_output))
    with open(f"logs/{filename}_h1h6_direct.log", "w") as f:
        f.write("\n".join(h1h6_direct_output))

    elapsed_time = (datetime.datetime.now() - start_time)
    logging.info(f"{test_name} test done, elapsed time: {elapsed_time}")
    print(f"Elapsed time: {elapsed_time}")
    return True
    
def main():
    trials = 20
    burst_size = 100

    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} bw_control_test 6Mbps Desired Policy {burst_size} Burst Size {trials} Trials"
    logging.basicConfig(filename=f'logs/{filename}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    bw_control_test(filename, trials, burst_size)
if __name__ == "__main__":
    main()

