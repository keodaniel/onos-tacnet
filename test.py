import logging
# from interact_onos import start_onos_docker, toggle_fwd, create_host_intents, get_intents, clear_intent, clear_all_intents
from interact_onos import *
from interact_mininet import MininetProcess
from time import sleep
import numpy as np
import matplotlib.pyplot as plt 
import datetime
import os
import statistics

def clear_log_file(log_file_path):
    try:
        # Open the log file in write mode
        with open(log_file_path, 'w') as log_file:
            # Write an empty string to clear the file contents
            log_file.write('')
        # print("Log file cleared successfully.")
    except Exception as e:
        print(f"Error clearing log file: {e}")

def pingall_test(topo="linear,3,2"):
    test_name = "Pingall"
    logging.info(f"Starting {test_name} test...")
    sleep_time = 3

    try:
        # Starting actions
        start_onos_docker()
        toggle_fwd("activate")
        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()

        # Test Commands
        sleep(sleep_time)
        mininet_process.send_command("pingall")
        cmd_output = mininet_process.read_stderr("*** Results")

        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_stderr("Done")

        # Logging success/failure
        if "0% dropped" in cmd_output:
            logging.info(f"{test_name} Test Success")
            print(f"{test_name} Test Success")
        else:
            logging.error(f"{test_name} Test Fail")
            print(f"{test_name} Test Fail")
        for lines in cmd_output.encode().split(b'\n'):
            if "Results" in lines.decode():
                print(lines.decode())

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def intent_functions_test(topo="linear,3,2"):
    test_name = "Intent Functions"
    logging.info(f"Starting {test_name} test...")
    sleep_time = 3

    try:
        # Starting actions
        start_onos_docker()
        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()

        # Test Commands

        # Pingall for ONOS to have hosts
        toggle_fwd("activate")
        sleep(sleep_time)
        mininet_process.send_command("pingall")
        cmd_output = mininet_process.read_stderr("*** Results")

        # HTTP request ONOS for hosts, HTTP post HostIntents, then HTTP delete request all Intents
        create_host_intents(get_mac_addresses())
        get_intents()
        clear_all_intents()

        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_stderr("Done")

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def paths_functions_test(topo="linear,3,2"):
    test_name = "Path Functions"
    logging.info(f"Starting {test_name} test...")
    sleep_time = 5

    try:
        # Starting actions
        start_onos_docker()
        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()

        # Test Commands

        # Pingall for ONOS to have hosts
        toggle_fwd("activate")
        sleep(sleep_time)
        mininet_process.send_command("pingall")
        cmd_output = mininet_process.read_stderr("*** Results")

        path_list = get_all_paths(get_mac_addresses())

        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_stderr("Done")

        # Logging success/failure
        if "0% dropped" in cmd_output:
            logging.info(f"{test_name} Test Success")
            print(f"{test_name} Test Success")
        else:
            logging.error(f"{test_name} Test Fail")
            print(f"{test_name} Test Fail")
        for lines in cmd_output.encode().split(b'\n'):
            if "Results" in lines.decode():
                print(lines.decode())

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def basic_link_auto_test(topo="linear,3,2"):
    test_name = "Basic Link Automation"
    testcase_1_success = False
    testcase_2_success = False
    testcase_1_name = "Link Automation via Reactive Forwarding"
    testcase_2_name = "Link Automation via Host Intents"
    logging.info(f"Starting {test_name} test...")
    sleep_time = 3

    try:
        # Starting actions
        start_onos_docker()
        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()

        # Test Commands
        logging.info(f"Test Case 1: {testcase_1_name}")
        toggle_fwd("activate")
        sleep(sleep_time)
        mininet_process.send_command("pingall")
        cmd_output_1 = mininet_process.read_stderr("*** Results")

        logging.info(f"Test Case 2: {testcase_2_name}")
        toggle_fwd("deactivate")
        clear_all_intents()
        create_host_intents(get_mac_addresses())
        sleep(sleep_time)
        mininet_process.send_command("pingall")
        cmd_output_2 = mininet_process.read_stderr("*** Results")

        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_stderr("Done")

        # Logging success/failure
        if "0% dropped" in cmd_output_1:
            testcase_1_success = True
        if testcase_1_success:
            print(f"Test Case 1: {testcase_1_name} Success")
        else:
            print(f"Test Case 1: {testcase_1_name} Fail")
        for lines in cmd_output_1.encode().split(b'\n'):
            if "Results" in lines.decode():
                print(lines.decode())

        if "0% dropped" in cmd_output_2:
            testcase_2_success = True
        if testcase_2_success:
            print(f"Test Case 2: {testcase_2_name} Success")
        else:
            print(f"Test Case 2: {testcase_2_name} Fail")
        for lines in cmd_output_2.encode().split(b'\n'):
            if "Results" in lines.decode():
                print(lines.decode())

        if testcase_1_success and testcase_2_success:
            logging.info(f"{test_name} Test Success")
            print(f"{test_name} Test Success")
        else:
            logging.error(f"{test_name} Test Fail")
            print(f"{test_name} Test Fail")

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def dynamic_paths_test(testcase, topo="linear,3,2"):
    test_name = "Dynamic Path Automation"
    testcase_success = False
    logging.info(f"Starting {test_name} test...")
    sleep_time = 3

    if testcase == "fwd":
        testcase_name = "Dynamic Paths via Reactive Forwarding"
    elif testcase == "intent":
        testcase_name = "Dynamic Paths via Host Intents"
    else:
        logging.error(f"Invalid testcase: {testcase}")
        return

    try:
        # Starting actions
        start_onos_docker()
        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()

        logging.info(f"Test Case: {testcase_name}")

        if testcase == "fwd":
            toggle_fwd("activate")
        elif testcase == "intent":
            toggle_fwd("activate")
            mininet_process.send_command("pingall")
            mininet_process.read_stderr("*** Results")
            toggle_fwd("deactivate")
            clear_all_intents()
            create_host_intents(get_mac_addresses())
        else:
            logging.error(f"Invalid testcase: {testcase}")
            return

        # Get initial paths
        sleep(sleep_time)
        mininet_process.send_command("pingall")
        cmd_output_1 = mininet_process.read_stderr("*** Results")
        
        mac_list = get_mac_addresses()
        paths_1 = get_all_paths(mac_list)

        # Failover
        link_failover_cmd_1 = "link s1 s2 down"
        mininet_process.send_command(link_failover_cmd_1)

        # Get new paths
        sleep(sleep_time)
        mininet_process.send_command("pingall")
        cmd_output_2 = mininet_process.read_stderr("*** Results")
        paths_2 = get_all_paths(get_mac_addresses())

        # Compare paths
        if paths_1 !=  paths_2:
            logging.info(f"Paths are different after {link_failover_cmd_1} command")
            for path_list in paths_1:
                if path_list not in paths_2:
                    if path_list:
                        logging.info("Removed Paths: " + str(path_list))
            for path_list in paths_2:
                if path_list not in paths_1:
                    if path_list:
                        logging.info("Added Paths: " + str(path_list))
        else:
            logging.info("Paths are the same")

        # Fail back
        link_failover_cmd_2 = "link s1 s2 up"
        mininet_process.send_command(link_failover_cmd_2)

        # Get new paths
        sleep(sleep_time)
        mininet_process.send_command("pingall")
        cmd_output_3 = mininet_process.read_stderr("*** Results")
        paths_3 = get_all_paths(get_mac_addresses())

        # Compare paths
        if paths_2 !=  paths_3:
            logging.info(f"Paths are different after {link_failover_cmd_2} command")
            for path_list in paths_2:
                if path_list not in paths_3:
                    if path_list:
                        logging.info("Removed Paths: " + str(path_list))
            for path_list in paths_3:
                if path_list not in paths_2:
                    if path_list:
                        logging.info("Added Paths: " + str(path_list))
        else:
            logging.info("Paths are the same")     

        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_stderr("Done")

        # Logging success/failure
        if "0% dropped" in cmd_output_1 and "0% dropped" in cmd_output_2 and "0% dropped" in cmd_output_3:
            if paths_1 != paths_2 and paths_2 != paths_3:
                testcase_success = True
        
        if testcase_success:
            logging.info(f"Test Case: {testcase_name} Success")
            print(f"Test Case: {testcase_name} Success")
        else:
            logging.error(f"Test Case: {testcase_name} Fail")
            print(f"Test Case: {testcase_name} Fail")

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def fault_tolerance_test(testcase, topo="TC"):
    test_name = "Fault Tolerance"
    testcase_success = False
    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime("%Y-%m-%d-%H%M")
    logging.info(f"Starting {test_name} test at {start_time_str}")
    sleep_time = 3
    iperf_time = 20 # 20s iperf test
    trial_runs = 20 # 20 for number of trials

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
        # Start iperf server
        sleep(10)
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
            sleep(iperf_time/2)
            mac_list = get_mac_addresses()
            paths_1 = get_all_paths(mac_list)
            logging.info("Failover at time 10s")
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
            link_reset_cmd = "link s1 s3 up"
            mininet_process.send_command(link_reset_cmd, check_stdout=True)
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
        fig.savefig(f"plots/{start_time_str}_{testcase}_boxplot.png")
        logging.info(f"{testcase} boxplot saved")

        elapsed_time = (datetime.datetime.now() - start_time)
        logging.info(f"{test_name} test done, elapsed time: {elapsed_time}")
        print(f"Elapsed time: {elapsed_time}")
        return output

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

def bandwidth_control_test(testcase, topo="BW"):
    test_name = "Bandwidth Control"
    testcase_success = False
    logging.info(f"Starting {test_name} test...")
    sleep_time = 3

    if testcase == "fwd":
        testcase_name = f"{test_name} via Reactive Forwarding"
    elif testcase == "intent":
        testcase_name = f"{test_name}via Host Intents"
    else:
        logging.error(f"Invalid testcase: {testcase}")
        return
    
    try:
        # Starting actions
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



        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_stderr("Done")

        # Logging success/failure

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def prototype(testcase, topo="TC"):
    test_name = "Fault Tolerance prototype"
    testcase_success = False
    logging.info(f"Starting {test_name} test...")
    
    try:
        mininet_process = MininetProcess(topo)
        mininet_process.start_mininet()

        baseline_throughput = None
        # logging.info("Baseline iperf output")
        mininet_process.read_logfile(f"iperf_baseline_{testcase}.log")
        
        baseline_output = mininet_process.read_logfile(f"iperf_baseline_{testcase}.log", last_line=True)
        # mininet_process.read_logfile("iperf_failover.log")

        # baseline_output = mininet_process.read_logfile("iperf_failover.log", last_line=True)
        print(baseline_output)

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def test_selection():
    user_input = input("Would you like to run a unit test or experiment?:\n1. Unit Test\n2. Experiment\n3. All\nEnter: ")
    if user_input == "1":
        unit_test = input("Which unit test would you like to run?:\n1. Pingall\n2. Intent Functions\n3. Path Functions\nEnter: ")
        if unit_test == "1":
            pingall_test()
        elif unit_test == "2":
            intent_functions_test(topo="DFGW")
        elif unit_test == "3":
            paths_functions_test(topo="DFGW")
    elif user_input == "2":
        experiment = input("Which experiment would you like to run?:\n1. Basic Link Automation\n2. Dynamic Path Automation\n3. Fault Tolerance\n4. All\nEnter: ")
        if experiment == "1":
            basic_link_auto_test(topo="DFGW")
        elif experiment == "2":
            testcase = input("Which testcase would you like to run?:\n1. Reactive Forwarding\n2. Host Intents\nEnter: ")
            if testcase == "1":
                dynamic_paths_test(testcase="fwd", topo="DFGW")
            elif testcase == "2":
                dynamic_paths_test(testcase="intent", topo="DFGW")
            else:
                print("Invalid testcase number. Exiting...")
                logging.error("Invalid testcase number. Exiting...")
        elif experiment == "3":
            testcase = input("Which testcase would you like to run?:\n1. Reactive Forwarding\n2. Host Intents\n3. All\nEnter: ")
            if testcase == "1":
                fault_tolerance_test(testcase="fwd", topo="TC")
            elif testcase == "2":
                fault_tolerance_test(testcase="intent", topo="TC")
            elif testcase == "3":
                fault_tolerance_test(testcase="fwd", topo="TC")
                fault_tolerance_test(testcase="intent", topo="TC")
            else:
                print("Invalid testcase number. Exiting...")
                logging.error("Invalid testcase number. Exiting...")
        elif experiment == "4":
            basic_link_auto_test(topo="DFGW")
            dynamic_paths_test(testcase="fwd", topo="DFGW")
            dynamic_paths_test(testcase="intent", topo="DFGW")
            fault_tolerance_test(testcase="fwd", topo="TC")
            fault_tolerance_test(testcase="intent", topo="TC")
    elif user_input == "3":
        pingall_test()
        paths_functions_test("DFGW")
        intent_functions_test("DFGW")
        basic_link_auto_test("DFGW")
        dynamic_paths_test(testcase="fwd", topo="DFGW")
        dynamic_paths_test(testcase="intent", topo="DFGW")
        fault_tolerance_test(testcase="fwd", topo="DFGW")
        fault_tolerance_test(testcase="intent", topo="DFGW")
    else:
        print("No test selected. Exiting...")
        logging.error("No test selected. Exiting...")

def main():
    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_file_path = f'logs/{datestring}_test.log'
    clear_log_file(log_file_path)
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    test_selection()
    logging.info("End of Log")

if __name__ == "__main__":
    main()
