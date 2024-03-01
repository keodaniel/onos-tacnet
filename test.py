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

def pingall_test():
    test_name = "Pingall"
    logging.info(f"Starting {test_name} test...")

    try:
        # Starting actions
        start_onos_docker()
        toggle_fwd("activate")
        mininet_process = MininetProcess("DFGW")
        mininet_process.start_mininet()

        # Test Commands
        cmd_output = mininet_process.send_command("time pingall", "*** Results")

        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_until("Done")

        # Logging success/failure
        for lines in cmd_output.encode().split(b'\n'):
            if "Results" in lines.decode():
                print(lines.decode())

        if "0% dropped" in cmd_output:
            print(f"{test_name} Test Success")
        else:
            print(f"{test_name} Test Fail")

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def intent_functions_test():
    test_name = "Intent Functions"
    logging.info(f"Starting {test_name} test...")

    try:
        # Starting actions
        start_onos_docker()
        mininet_process = MininetProcess("tree,2,2")
        mininet_process.start_mininet()

        # Test Commands

        # Pingall for ONOS to have hosts
        toggle_fwd("activate")
        cmd_output = mininet_process.send_command("pingall", "*** Results")

        # HTTP request ONOS for hosts, HTTP post HostIntents, then HTTP delete request all Intents
        create_host_intents()
        get_intents()
        clear_all_intents()

        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_until("Done")

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def basic_link_automation_test():
    test_name = "Basic Link Automation"
    logging.info(f"Starting {test_name} test...")

    try:
        # Starting actions
        start_onos_docker()
        mininet_process = MininetProcess("DFGW")
        mininet_process.start_mininet()

        # Test Commands
        testcase_1_success = False
        testcase_2_success = False

        logging.info(f"Test Case 1: Link Automation via Reactive Forwarding")
        toggle_fwd("activate")
        cmd_output_1 = mininet_process.send_command("pingall", "*** Results")
        for lines in cmd_output_1.encode().split(b'\n'):
            if "Results" in lines.decode():
                print(lines.decode())
        if "0% dropped" in cmd_output_1:
            testcase_1_success = True

        logging.info(f"Test Case 2: Link Automation via Installing Host Intents")
        toggle_fwd("deactivate")
        clear_all_intents()
        create_host_intents()
        cmd_output_2 = mininet_process.send_command("pingall", "*** Results")
        for lines in cmd_output_2.encode().split(b'\n'):
            if "Results" in lines.decode():
                print(lines.decode())
        if "0% dropped" in cmd_output_2:
            testcase_2_success = True

        # Closing actions
        mininet_process.process.stdin.close()
        remaining_output = mininet_process.read_until("Done")

        # Logging success/failure
        if testcase_1_success:
            print("Test Case 1 Success")
        else:
            print("Test Case 1  Fail")
        if testcase_2_success:
            print("Test Case 2 Success")
        else:
            print("Test Case 2  Fail")
        if testcase_1_success and testcase_2_success:
            print(f"{test_name} Test Success")
        else:
            print(f"{test_name} Test Fail")

    except Exception as e:
        logging.error(f"Error during {test_name} test: {e}")

    logging.info(f"{test_name} test done")

def main():
    log_file_path = 'test.log'
    clear_log_file(log_file_path)
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    pingall_test()
    intent_functions_test()
    basic_link_automation_test()

    logging.info("End of Log")

if __name__ == "__main__":
    main()
