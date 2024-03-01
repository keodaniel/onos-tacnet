import logging
from interact_onos import start_onos_docker, toggle_fwd
from interact_mininet import MininetProcess

def clear_log_file(log_file_path):
    try:
        # Open the log file in write mode
        with open(log_file_path, 'w') as log_file:
            # Write an empty string to clear the file contents
            log_file.write('')
        # print("Log file cleared successfully.")
    except Exception as e:
        print(f"Error clearing log file: {e}")

def pingall_test(mininet_process):
    logging.info("Starting basic pingall test")

    try:
        cmd_output = mininet_process.send_command("pingall", "*** Results")
        mininet_process.process.stdin.close()
        end = mininet_process.read_until("Done")

        for lines in cmd_output.encode().split(b'\n'):
            if "Results" in lines.decode():
                print(lines.decode())

        if "0% dropped" in cmd_output:
            print("Pingall Test Success")
        else:
            print("Pingall Test Fail")
        if "Done" in end:
            print("Done")

    except Exception as e:
        logging.error(f"Error during pingall test: {e}")

    logging.info("Done")

def main():
    log_file_path = 'test.log'
    clear_log_file(log_file_path)

    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting test")
    start_onos_docker()
    toggle_fwd("activate")
    mininet_process = MininetProcess("DFGW")
    mininet_process.start_mininet()

    pingall_test(mininet_process)
    
    logging.info("Done")

if __name__ == "__main__":
    main()
