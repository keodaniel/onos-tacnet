import logging
from logging import *
from interact_onos import *
from interact_mininet import *
from time import sleep
import datetime

def bw_control(filename):
    test_name = "iPerf3"
    testcase_success = False
    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime("%Y-%m-%d-%H%M")
    sleep_time = 5

    logging.info(f"Starting {test_name} test at {start_time_str}")
    logging.info(f"{protocol} iperf_time: {iperf_time}s, trial_runs: {trial_runs}, parallel_connections: {parallel_connections}, bitrate: {bitrate}")
    print(f"{testcase} {protocol} iperf_time: {iperf_time}s, trial_runs: {trial_runs}, parallel_connections: {parallel_connections}, bitrate: {bitrate}")

    try:
        # Starting actions
        restart_onos_docker()
        logging.info(f"Test Case: {testcase_name}")

    except Exception as e:
        logging.error(f"Error starting {test_name} test: {e}")
        
        try:
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

            # Logging success/failure
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
    
def main():
    bw_control()
    datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{datestring} bw_control_test"
    logging.basicConfig(filename=f'logs/{filename}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    main()

# meter_data = {
#   "deviceId": "of:0000000000000001",
#   "meter": "1000",
#   "unit": "KB_PER_SEC",
#   "bands": [
#     {
#       "type": "DROP",
#       "rate": "1000",
#       "burstSize": "0"
#     }
#   ]
# }

# for device in ("of:0000000000000001", "of:0000000000000002", "of:0000000000000003"):
#     meter_id = "1000"
#     rate = "1000"
#     post_meters(device, meter_data(device, meter_id, rate))

# for device in ("of:0000000000000002", "of:0000000000000003"):
#     meter_id = "2000"
#     rate = "2000"
#     post_meters(device, meter_data(device, meter_id, rate))

# for device in ("of:0000000000000001", "of:0000000000000003"):
#     meter_id = "3000"
#     rate = "3000"
#     post_meters(device, meter_data(device, meter_id, rate))

for meter in get_meters():
#     # if meter[2] == "ADDED":
    print(meter)

# for meter in get_meters():
#     delete_meter(meter[0], meter[1])
