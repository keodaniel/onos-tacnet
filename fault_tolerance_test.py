import logging
from logging import *
from interact_onos import *
from interact_mininet import *
from time import sleep
import datetime

def iperf3_test(filename, testcase, topo="TC", iperf_time=10, trial_runs=2, parallel_connections=1, udp=False, bitrate=False):
    test_name = "iPerf3"
    testcase_success = False
    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime("%Y-%m-%d-%H%M")
    sleep_time = 5
    failover_time = iperf_time/2
    baseline_output = []
    failover_output = []
    baseline_log_path = f"iperf/baseline.log"
    failover_log_path = f"iperf/failover.log"
    successful_runs = 0
    fail_runs = 0
    udp_option = "-u " if udp else ""
    protocol = "UDP" if udp else "TCP"
    bitrate_format = "mM"
    if bitrate:
        bitrate_option = f"-b {bitrate}M "
        if bitrate < 1:
            bitrate_format = "kK"
    else:
        bitrate_option = ""
        bitrate = "Default"

    logging.info(f"Starting {test_name} test at {start_time_str}")
    logging.info(f"{protocol} iperf_time: {iperf_time}s, trial_runs: {trial_runs}, parallel_connections: {parallel_connections}, bitrate: {bitrate}")
    print(f"{testcase} {protocol} iperf_time: {iperf_time}s, trial_runs: {trial_runs}, parallel_connections: {parallel_connections}, bitrate: {bitrate}")

    if testcase == "fwd":
        testcase_name = "Fault Tolerance via Reactive Fwd"
    elif testcase == "intent":
        testcase_name = "Fault Tolerance via Host Intents"
    else:
        logging.error(f"Invalid testcase: {testcase}")
        return
    
    try:
        # Starting actions
        restart_onos_docker()
        logging.info(f"Test Case: {testcase_name}")

    except Exception as e:
        logging.error(f"Error starting {test_name} test: {e}")
    
    while successful_runs < trial_runs:
        if fail_runs > 30:
            logging.error("Too many failures, ending test")
            break
        
        try:
            paths_1 = None
            paths_2 = None

            mininet_process = MininetProcess(topo)
            mininet_process.start_mininet()
            if testcase == "fwd":
                toggle_fwd("activate")
            elif testcase == "intent":
                toggle_fwd("activate")
                sleep(10)
                mininet_process.send_command("pingall")
                mininet_process.read_stderr("*** Results")
                toggle_fwd("deactivate")
                clear_all_intents()
                create_host_intents(get_mac_addresses())
            else:
                logging.error(f"Invalid testcase: {testcase}")
                return

            # Start iperf server
            sleep(sleep_time)
            mininet_process.send_command("h1 iperf3 -s &", check_stdout=True)
            sleep(sleep_time)

            # Baseline iperf test
            mininet_process.send_command(f"h6 iperf3 -c 10.0.10.1 {udp_option}{bitrate_option}-t {iperf_time} -i 1 -f {bitrate_format} -P {parallel_connections} > {baseline_log_path} &", check_stdout=True)
            sleep(iperf_time)
            logging.info("Baseline iperf output")
            baseline_log = mininet_process.read_iperf3_logfile(baseline_log_path)

            # Failover iperf test
            sleep(sleep_time)
            mininet_process.send_command(f"h6 iperf3 -c 10.0.10.1 {udp_option}{bitrate_option}-t {iperf_time} -i 1 -f {bitrate_format} -P {parallel_connections} > {failover_log_path} &", check_stdout=True)
            mac_list = get_mac_addresses()
            paths_1 = get_all_paths(mac_list)
            sleep(failover_time)
            logging.info(f"Failover at time {failover_time}s")
            link_failover_cmd = "link s1 s3 down"
            mininet_process.send_command(link_failover_cmd, check_stdout=True)
            sleep(sleep_time)
            paths_2 = get_all_paths(mac_list)
            sleep(failover_time)
            logging.info("Failover iperf output")
            failover_log = mininet_process.read_iperf3_logfile(failover_log_path)

            # Compare paths
            if paths_1 !=  paths_2:
                logging.info(f"Paths are different after {link_failover_cmd} command")
                for path_list in paths_2:
                    if path_list not in paths_1:
                        if path_list:
                            logging.info("Added Paths: " + str(path_list))
                for path_list in paths_1:
                    if path_list not in paths_2:
                        if path_list:
                            logging.info("Removed Paths: " + str(path_list))
            else:
                logging.info("Paths are the same")  
                logging.error(f"Test Case: {testcase_name} Trial {successful_runs+1} Fail")

            # Logging success/failure
            if paths_1 != paths_2:
                testcase_success = True
            if testcase_success:
                # Closing actions
                mininet_process.process.stdin.close()
                mininet_process.read_stderr("Done")
                logging.info(f"{testcase_name} Test Trial {successful_runs+1} Success")
                timestring = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"{testcase_name} Test Trial {successful_runs+1} Success, time: {timestring}")
                baseline_output.extend(baseline_log)
                failover_output.extend(failover_log)
                successful_runs += 1
            else:
                logging.error(f"{testcase_name} Test Fail")
                print(f"{testcase_name} Test Fail")

        except Exception as e:
            logging.error(f"Fail {fail_runs+1} during trial {successful_runs+1}: {e}, retrying...")
            print(f"Fail {fail_runs+1} during trial {successful_runs+1}: {e}, retrying...")
            fail_runs += 1

            # Closing actions
            mininet_process.process.stdin.close()
            mininet_process.read_stderr("Done")

    # Write output to log file     
    output_path = f"logs/{filename}_output.log"
    with open(output_path, 'w') as output_file:
        output_file.write("Baseline Output:\n")
        logging.info("Baseline Output:")
        for i in baseline_output:
            output_file.write(i + "\n")
            logging.info(i)
        output_file.write("Failover Output:\n")
        logging.info("Failover Output:")
        for i in failover_output:
            output_file.write(i + "\n")
            logging.info(i)

        elapsed_time = (datetime.datetime.now() - start_time)
        logging.info(f"{test_name} test done, elapsed time: {elapsed_time}")
        print(f"Elapsed time: {elapsed_time}")
        return True

def tcp_1(testcase = "fwd"):
    topo = "TC"
    iperf_time = 20
    trial_runs = 20
    parallel_connections = 1

    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} {testcase}-{topo}-t{iperf_time}-P{parallel_connections}-{trial_runs}runs"
    iperf3_test(filename, testcase, topo, iperf_time, trial_runs, parallel_connections)

def tcp_3(testcase = "fwd"):
    topo = "TC"
    iperf_time = 20
    trial_runs = 20
    parallel_connections = 3

    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} {testcase}-{topo}-t{iperf_time}-P{parallel_connections}-{trial_runs}runs"
    iperf3_test(filename, testcase, topo, iperf_time, trial_runs, parallel_connections)

def voip_1(testcase = "fwd"):
    topo = "TC"
    iperf_time = 20
    trial_runs = 20
    parallel_connections = 1
    udp = True
    protocol = "udp"
    bitrate = 0.1

    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} {testcase}-{topo}-{protocol}-t{iperf_time}-P{parallel_connections}-b{round(bitrate)}M-{trial_runs}runs"
    iperf3_test(filename, testcase, topo, iperf_time, trial_runs, parallel_connections, udp, bitrate)

def voip_3(testcase = "fwd"):
    topo = "TC"
    iperf_time = 20
    trial_runs = 20
    parallel_connections = 3
    udp = True
    protocol = "udp"
    bitrate = 0.1

    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} {testcase}-{topo}-{protocol}-t{iperf_time}-P{parallel_connections}-b{round(bitrate)}M-{trial_runs}runs"
    iperf3_test(filename, testcase, topo, iperf_time, trial_runs, parallel_connections, udp, bitrate)

def video_1(testcase = "fwd"):
    topo = "TC"
    iperf_time = 20
    trial_runs = 20
    parallel_connections = 1
    udp = True
    protocol = "udp"
    bitrate = 2

    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} {testcase}-{topo}-{protocol}-t{iperf_time}-P{parallel_connections}-b{bitrate}M-{trial_runs}runs"
    iperf3_test(filename, testcase, topo, iperf_time, trial_runs, parallel_connections, udp, bitrate)

def video_2(testcase = "fwd"):
    topo = "TC"
    iperf_time = 20
    trial_runs = 20
    parallel_connections = 2
    udp = True
    protocol = "udp"
    bitrate = 2

    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} {testcase}-{topo}-{protocol}-t{iperf_time}-P{parallel_connections}-b{bitrate}M-{trial_runs}runs"
    iperf3_test(filename, testcase, topo, iperf_time, trial_runs, parallel_connections, udp, bitrate)

def main():
    print("Choose test: TCP, VoIP, Video")
    test = input()
    print("Choose parallel connections: Single or Multi")
    connections = input()
    print("Choose testcase: fwd, intent")
    testcase = input()

    if test == "TCP":
        if connections == "Single":
            tcp_1(testcase)
        elif connections == "Multi":
            tcp_3(testcase)
    elif test == "VoIP":
        if connections == "Single":
            voip_1(testcase)
        elif connections == "Multi":
            voip_3(testcase)
    elif test == "Video":
        if connections == "Single":
            video_1(testcase)
        elif connections == "Multi":
            video_2(testcase)

    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} {test}-{connections}-{testcase}"
    logging.basicConfig(filename=f'logs/{filename}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    main()
