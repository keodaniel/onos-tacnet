import subprocess
# import paramiko
import logging
from time import sleep

class MininetProcess:
    def __init__(self, topology):
        self.topology = topology
        self.process = None

    def start_mininet(self):
        try:
            topology_file = "../../media/sf_onos-tacnet/custom/tacnet.py"
            
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

    # def send_command(self, command, check_stdout=False):
    #     try: 
    #         logging.info(f"Executing Mininet command: {command}")
    #         self.process.stdin.write(f"{command}\n".encode())
    #         self.process.stdin.flush()

    #         if check_stdout:
    #             if "mininet>" in self.read_stdout():
    #                 logging.info(f"Command {command} successful")
    #                 return True
    #             else:
    #                 logging.error(f"Command {command} failed")
    #                 return False

    #     except Exception as e:
    #         logging.error(f"Error sending Mininet command: {e}")

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


    def read_stderr(self, expected_keyword):
        try: 
            stderr_data = b''  # Initialize as bytes
            while True:
                stderr_line = self.process.stderr.readline()
                stderr_data += stderr_line

                stderr_str = stderr_data.decode('utf-8')
                if expected_keyword in stderr_str:
                    output = stderr_str.rstrip('\n')  # Remove the last newline character
                    logging.info(output)
                    return output

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

    # def read_logfile(self, logfile, last_line=False):
    #     try:
    #         with open(logfile) as f:
    #             for line in f:
    #                 if last_line:
    #                     pass
    #                 else:
    #                     logging.info(line.rstrip('\n'))  # Remove the last newline character
    #             if last_line:
    #                 if "0.0000" in line:
    #                     return line.rstrip('\n')
    #                 else:
    #                     logging.error("Expected last line to contain '0.0000'")
    #                     return
    #     except Exception as e:
    #         logging.error(f"Error reading log file: {e}")

    def read_logfile(self, logfile):
        timeout = 100
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

