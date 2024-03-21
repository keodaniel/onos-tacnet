import logging
# from interact_onos import start_onos_docker, toggle_fwd, create_host_intents, get_intents, clear_intent, clear_all_intents
from interact_onos import *
from interact_mininet import MininetProcess
from time import sleep 

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

def fault_tolerance_test(testcase, topo="linear,3,2"):
    test_name = "Fault Tolerance"
    testcase_success = False
    logging.info(f"Starting {test_name} test...")
    sleep_time = 3

    if testcase == "fwd":
        testcase_name = "Fault Tolerance via Reactive Forwarding"
    elif testcase == "intent":
        testcase_name = "Fault Tolerance via Host Intents"
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

        # Start iperf
        sleep(sleep_time)
        mininet_process.send_command("h1 iperf -s &", check_stdout=True)
        sleep(sleep_time)
        mininet_process.send_command("h6 iperf -c 10.0.10.1 -t 20 -i 1 > iperf_throwaway.log &", check_stdout=True)
        sleep(25)
        mininet_process.send_command("h6 iperf -c 10.0.10.1 -t 20 -i 1 > iperf_baseline.log &", check_stdout=True)
        sleep(25)
        mininet_process.send_command("h6 iperf -c 10.0.10.1 -t 20 -i 1 > iperf_failover.log &", check_stdout=True)

        # Get paths
        sleep(10)
        mac_list = get_mac_addresses()
        paths_1 = get_all_paths(mac_list)

       # Failover and get new paths
        logging.info("Failover at time 10s")
        link_failover_cmd = "link s1 s3 down"
        mininet_process.send_command("link s1 s3 down", check_stdout=True)
        sleep(1)
        paths_2 = get_all_paths(get_mac_addresses())

        sleep(15)
        mininet_process.send_command("h6 cat iperf_throwaway.log", check_stdout=True)
        logging.info("Throwaway iperf output")
        sleep(1)
        mininet_process.read_stderr("0.0000-20")
        mininet_process.send_command("h6 cat iperf_baseline.log", check_stdout=True)
        logging.info("Baseline iperf output")
        sleep(1)
        mininet_process.read_stderr("0.0000-20")
        mininet_process.send_command("h6 cat iperf_failover.log", check_stdout=True)
        logging.info("Failover iperf output")
        sleep(1)
        mininet_process.read_stderr("0.0000-20")

        # Compare paths
        if paths_1 !=  paths_2:
            logging.info(f"Paths are different after {link_failover_cmd} command")
            for path_list in paths_2:
                if path_list not in paths_1:
                    if path_list:
                        logging.info("Removed Paths: " + str(path_list))
            for path_list in paths_1:
                if path_list not in paths_2:
                    if path_list:
                        logging.info("Added Paths: " + str(path_list))
        else:
            logging.info("Paths are the same")     

        # Logging success/failure
        mininet_process.send_command("h6 cat iperf_baseline.log | grep '0.0000-20'", check_stdout=True)
        baseline_output = mininet_process.read_stderr("0.0000-20")
        sleep(1)
        mininet_process.send_command("h6 cat iperf_failover.log | grep '0.0000-20'", check_stdout=True)
        failover_output = mininet_process.read_stderr("0.0000-20")

        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_stderr("Done")

        for lines in baseline_output.split("  "):
            if "GBytes" in lines:
                baseline_capacity = lines.split(" ")[0]
            if "Gbits/sec" in lines:
                baseline_throughput = lines.split(" ")[0]
        for lines in failover_output.split("  "):
            if "GBytes" in lines:
                failover_capacity = lines.split(" ")[0]
            if "Gbits/sec" in lines:
                failover_throughput = lines.split(" ")[0]
        
        # Log difference between baseline and failover
        logging.info(f"Baseline Capacity: {baseline_capacity} Gbytes, Baseline Throughput: {baseline_throughput} Gbits/sec")
        logging.info(f"Failover Capacity: {failover_capacity} Gbytes, Failover Throughput: {failover_throughput} Gbits/sec")
        capacity_diff = round(float(baseline_capacity) - float(failover_capacity), 2)
        throughput_diff = round(float(baseline_throughput) - float(failover_throughput), 2)
        logging.info(f"Capacity Difference: {capacity_diff} Gbytes, Throughput Difference: {throughput_diff} Gbits/sec")

        # Logging success/failure
        if paths_1 != paths_2:
            testcase_success = True
        if testcase_success:
            logging.info(f"Test Case: {testcase_name} Success")
            print(f"Test Case: {testcase_name} Success")
            print(f"Capacity Difference: {capacity_diff} Gbytes, Throughput Difference: {throughput_diff} Gbits/sec")
        else:
            logging.error(f"Test Case: {testcase_name} Fail")
            print(f"Test Case: {testcase_name} Fail")

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
            testcase = input("Which testcase would you like to run?:\n1. Reactive Forwarding\n2. Host Intents\nEnter: ")
            if testcase == "1":
                fault_tolerance_test(testcase="fwd", topo="DFGW")
            elif testcase == "2":
                fault_tolerance_test(testcase="intent", topo="DFGW")
            else:
                print("Invalid testcase number. Exiting...")
                logging.error("Invalid testcase number. Exiting...")
        elif experiment == "4":
            basic_link_auto_test(topo)
            dynamic_paths_test(testcase="fwd", topo="DFGW")
            dynamic_paths_test(testcase="intent", topo="DFGW")
            fault_tolerance_test(testcase="fwd", topo="DFGW")
            fault_tolerance_test(testcase="intent", topo="DFGW")
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
    log_file_path = 'test.log'
    clear_log_file(log_file_path)
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    test_selection()
    logging.info("End of Log")

if __name__ == "__main__":
    main()
