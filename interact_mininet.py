### Helper Functions for Interacting with Mininet ###

import subprocess
import logging
from time import sleep
import os

class MininetProcess:
    def __init__(self, topology):
        self.topology = topology
        self.process = None

    def start_mininet(self):
        try:
            script_dir = os.path.dirname(__file__)
            topology_file = os.path.join(script_dir, 'custom/tacnet.py')
            
            # Clean up Mininet before starting a new topology
            subprocess.run(["sudo", "mn", "-c"], capture_output=True, text=True, check=False)
            
            # Start Mininet with the specified topology
            command = ['sudo', 'mn', '--switch', 'ovs,protocols=OpenFlow14', '--controller', 'remote,ip=172.17.0.2', '--mac', '--custom', topology_file, '--topo=' + self.topology]
            logging.info(f"Starting Mininet topology: {self.topology}")
            self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            self.read_stderr("Starting CLI")
            return self.process
            
        except Exception as e:
            logging.error(f"Error starting Mininet: {e}")
            raise

    def send_command(self, command, check_stdout=False):
        timeout = 100
        sleep_time = 5

        while timeout > 0:
            logging.info(f"Executing Mininet command: {command}")
            self.process.stdin.write(f"{command}\n".encode())
            self.process.stdin.flush()

            if check_stdout:
                if "mininet>" in self.read_stdout():
                    logging.info(f"Command {command} successful")
                    sleep(sleep_time)
                    return True
                else:
                    logging.error(f"Command {command} failed, sleeping {sleep_time} seconds before retrying")
                    sleep(sleep_time)
                    timeout -= 1
            else:
                return True
        
        logging.error(f"Command {command} failed after multiple retries")
        return False


    def read_stderr(self, expected_keyword):
        try: 
            stderr_data = b''  # Initialize as bytes
            while True:
                stderr_line = self.process.stderr.readline()
                stderr_data += stderr_line
                logging.info(stderr_line.decode('utf-8'))

                stderr_str = stderr_data.decode('utf-8')
                if expected_keyword in stderr_str:
                    output = stderr_str.rstrip('\n')  # Remove the last newline character
                    logging.info(output)
                    return output
                elif "Exception" in stderr_str:
                    logging.error("Error in Mininet stderr")
                    return None

        except Exception as e:
            logging.error(f"Error reading Mininet display (stderr): {e}")

    def read_stdout(self, mute=True):
        try: 
            output = self.process.stdout.read1().decode("utf-8")
            if not mute:
                logging.info(output)
            return output

        except Exception as e:
            logging.error(f"Error reading stdout: {e}")

    def read_logfile(self, logfile):
        timeout = 10
        sleep_time = 5
        output = []

        while timeout > 0:
            output = []
            with open(logfile) as f:
                for line in f:
                    output.append(line.rstrip('\n'))

            if " 0.0000" in output[-1]:
                break
            else:
                logging.info(f"Sleeping {sleep_time} seconds before retrying to read {logfile}")
                sleep(sleep_time)
                timeout -= 1

        if timeout == 0:
            logging.error(f"Error reading log file: {logfile}")
            return
        else:
            for line in output:
                logging.info(line)
            return output[-1]

    def read_iperf3_logfile(self, logfile):
        timeout = 20
        sleep_time = 10
        result = []

        while timeout > 0:
            output = []
            with open(logfile) as f:
                for line in f:
                    output.append(line.rstrip('\n'))

            if len(output) > 0 and "iperf Done." in output[-1]:
                logging.info("Found iperf Done.")
                break
            for line in output:
                if "0.00-20.00" in line:
                    logging.info("Found 0.00-20.00")
                    timeout = -1
                    break
                if "0.00-10.00" in line:
                    logging.info("Found 0.00-10.00")
                    timeout = -1
                    break
            else:
                logging.info(f"Sleeping {sleep_time} seconds before retrying to read {logfile}")
                sleep(sleep_time)
                timeout -= 1

        if timeout == 0:
            logging.error(f"Runtime exceeded for reading log: {logfile}")
            for line in output:
                logging.error(line)
            raise Exception(f"Runtime exceeded for reading log")
        
        else:
            for line in output:
                if "sender" in line or "receiver" in line:
                    result.append(line)
                logging.info(line)
            return result


