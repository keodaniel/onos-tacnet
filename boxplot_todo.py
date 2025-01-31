# TODO Extract boxplot code

import logging
from interact_onos import *
from interact_mininet import MininetProcess
from time import sleep
import numpy as np
import matplotlib.pyplot as plt 
import datetime
import statistics

def fault_tolerance_test(testcase, topo="TC"):
    test_name = "Fault Tolerance"
    testcase_success = False
    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime("%Y-%m-%d-%H%M")
    sleep_time = 3
    iperf_time = 20 # 20s iperf test
    trial_runs = 20 # 20 for number of trials
    failover_time = iperf_time/2

    logging.info(f"Starting {test_name} test at {start_time_str}")
    logging.info(f"iperf_time: {iperf_time}s, trial_runs: {trial_runs}")

    if testcase == "fwd":
        testcase_name = "Fault Tolerance via Reactive Fwd"
    elif testcase == "intent":
        testcase_name = "Fault Tolerance via Host Intents"
    else:
        logging.error(f"Invalid testcase: {testcase}")
        return
    
    try:
        # Starting actions
        output = []
        baseline_capacity_data = []
        failover_capacity_data = []
        baseline_throughput_data = []
        failover_throughput_data = []
        capacity_diff_data = []
        throughput_diff_data = []

        output = []
        baseline_capacity_data = []
        failover_capacity_data = []
        baseline_throughput_data = []
        failover_throughput_data = []
        capacity_diff_data = []
        throughput_diff_data = []

        start_onos_docker()
        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()

        logging.info(f"Test Case: {testcase_name}")

        if testcase == "fwd":
            toggle_fwd("activate")
        elif testcase == "intent":
            toggle_fwd("activate")
            sleep(sleep_time)
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
        mininet_process.send_command("h1 iperf -s &", check_stdout=True)

        for i in range(trial_runs):
            paths_1 = None
            paths_2 = None
            baseline_capacity = None
            failover_capacity = None
            baseline_throughput = None
            failover_throughput = None
            capacity_diff = None
            throughput_diff = None

            sleep(sleep_time)

            # Baseline iperf test
            mininet_process.send_command(f"h6 iperf -c 10.0.10.1 -t {iperf_time} -i 1 -f mM > iperf/iperf_{testcase}_baseline.log &", check_stdout=True)
            sleep(iperf_time)
            logging.info("Baseline iperf output")
            baseline_output = mininet_process.read_logfile(f"iperf/iperf_{testcase}_baseline.log")

            # Failover iperf test
            mininet_process.send_command(f"h6 iperf -c 10.0.10.1 -t {iperf_time} -i 1 -f mM > iperf/iperf_{testcase}_failover.log &", check_stdout=True)
            sleep(failover_time)
            mac_list = get_mac_addresses()
            paths_1 = get_all_paths(mac_list)
            logging.info(f"Failover at time {failover_time}s")
            link_failover_cmd = "link s1 s3 down"
            mininet_process.send_command(link_failover_cmd, check_stdout=True)
            paths_2 = get_all_paths(mac_list)
            logging.info("Failover iperf output")
            failover_output = mininet_process.read_logfile(f"iperf/iperf_{testcase}_failover.log")

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
                logging.error(f"Test Case: {testcase_name} Trial {i+1} Fail")
                return False 

            # Parse iperf output
            for lines in baseline_output.split("  "):
                if "MBytes" in lines:
                    baseline_capacity = float(lines.split(" ")[0])
                if "Mbits/sec" in lines:
                    baseline_throughput = float(lines.split(" ")[0])
            for lines in failover_output.split("  "):
                if "MBytes" in lines:
                    failover_capacity = float(lines.split(" ")[0])
                if "Mbits/sec" in lines:
                    failover_throughput = float(lines.split(" ")[0])
            
            # Log difference between baseline and failover
            logging.info(f"Baseline Capacity: {baseline_capacity} Mbytes, Baseline Throughput: {baseline_throughput} Mbits/sec")
            logging.info(f"Failover Capacity: {failover_capacity} Mbytes, Failover Throughput: {failover_throughput} Mbits/sec")
            capacity_diff = round(float(baseline_capacity) - float(failover_capacity), 2)
            throughput_diff = round(float(baseline_throughput) - float(failover_throughput), 2)
            logging.info(f"Capacity Difference: {capacity_diff} Mbytes, Throughput Difference: {throughput_diff} Mbits/sec")

            # Logging success/failure
            if paths_1 != paths_2:
                testcase_success = True
            if testcase_success:
                logging.info(f"{testcase_name} Test Trial {i+1} Success")
                timestring = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"{testcase_name} Test Trial {i+1} Success, time: {timestring}")
                # print(f"Baseline Capacity: {baseline_capacity} Mbytes, Baseline Throughput: {baseline_throughput} Mbits/sec")
                # print(f"Failover Capacity: {failover_capacity} Mbytes, Failover Throughput: {failover_throughput} Mbits/sec")
                # print(f"Capacity Difference: {capacity_diff} Mbytes, Throughput Difference: {throughput_diff} Mbits/sec")
                baseline_capacity_data.append(baseline_capacity)
                failover_capacity_data.append(failover_capacity)
                baseline_throughput_data.append(baseline_throughput)
                failover_throughput_data.append(failover_throughput)
                capacity_diff_data.append(capacity_diff)
                throughput_diff_data.append(throughput_diff)
            else:
                logging.error(f"{testcase_name} Test Fail")
                print(f"{testcase_name} Test Fail")
                return False
            
            # Reset link
            logging.info("Resetting link")
            link_reset_cmd1 = "link s1 s3 up"
            mininet_process.send_command(link_reset_cmd1, check_stdout=True)
            link_reset_cmd2 = "link s1 s2 down"
            mininet_process.send_command(link_reset_cmd2, check_stdout=True)
            link_reset_cmd3 = "link s1 s2 up"
            mininet_process.send_command(link_reset_cmd3, check_stdout=True)
            sleep(1)
        
        # Closing actions
        output = (baseline_capacity_data, failover_capacity_data, baseline_throughput_data, failover_throughput_data, capacity_diff_data, throughput_diff_data)
        mininet_process.process.stdin.close()
        mininet_process.read_stderr("Done")
        logging.info(f"Output: {output}")

        baseline_capacity_data = np.array(baseline_capacity_data, dtype=float)
        failover_capacity_data = np.array(failover_capacity_data, dtype=float)
        baseline_throughput_data = np.array(baseline_throughput_data, dtype=float)
        failover_throughput_data = np.array(failover_throughput_data, dtype=float)
        capacity_diff_data = np.array(capacity_diff_data, dtype=float)
        throughput_diff_data = np.array(throughput_diff_data, dtype=float)

        # boxplot
        fig, ax = plt.subplots(1, 2)
        fig.set_size_inches(10, 5)
        ax[0].boxplot([baseline_capacity_data, failover_capacity_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
        ax[0].set_title("Capacity of 20s iPerf Test")
        # ticks = np.arange(0, 32, 2)
        M = max(max(baseline_capacity_data), max(failover_capacity_data))
        M = M + 10 - M % 10
        ticks = np.arange(0, M+2, 2)
        ax[0].set_yticks(ticks)
        ax[0].set_ylabel("MBytes")
        failover_median = statistics.median(failover_capacity_data)
        baseline_median = statistics.median(baseline_capacity_data)
        diff_median = (failover_median - baseline_median) / baseline_median * 100
        ax[0].text(1.6, failover_median, f"{'+' if diff_median >= 0 else '-'}{diff_median:.2f}% ", ha='center', va='center', color='red')
        ax[0].text(1.5, 0, "Median % Difference from Baseline", ha='center', va='bottom', color='red')

        ax[1].boxplot([baseline_throughput_data, failover_throughput_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
        ax[1].set_title("Throughput of 20s iPerf Test")
        ax[1].set_ylabel("Mbits/sec")
        # ticks = np.arange(0, 11, 1)
        M = max(max(baseline_throughput_data), max(failover_throughput_data))
        M = M + 10 - M % 10
        ticks = np.arange(0, M+1, 1)
        ax[1].set_yticks(ticks)
        failover_median = statistics.median(failover_throughput_data)
        baseline_median = statistics.median(baseline_throughput_data)
        diff_median = (failover_median - baseline_median) / baseline_median * 100
        ax[1].text(1.6, failover_median, f"{'+' if diff_median >= 0 else '-'}{diff_median:.2f}% ", ha='center', va='center', color='red')
        ax[1].text(1.5, 0, "Median % Difference from Baseline", ha='center', va='bottom', color='red')                      

        # plt.show()
        fig.savefig(f"plots/{start_time_str}_{testcase}_{iperf_time}sx{trial_runs}trials_boxplot.png")
        logging.info(f"{testcase} boxplot saved")

        elapsed_time = (datetime.datetime.now() - start_time)
        logging.info(f"{test_name} test done, elapsed time: {elapsed_time}")
        print(f"Elapsed time: {elapsed_time}")
        return output

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")