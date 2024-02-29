import subprocess
# import paramiko
import logging
# from time import sleep

# import subprocess
# import logging

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

            self.read_until("Starting CLI")
            return self.process
            
        except Exception as e:
            logging.error(f"Error starting Mininet: {e}")

    def send_command(self, command, expected_keyword):
        try: 
            logging.info(f"Executing Mininet command: {command}")
            self.process.stdin.write(f"{command}\n".encode())
            self.process.stdin.flush()

            output = self.read_until(expected_keyword)
            return output

        except Exception as e:
            logging.error(f"Error sending Mininet command: {e}")

    def read_until(self, expected_keyword):
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
                    # break

        except Exception as e:
            logging.error(f"Error reading Mininet display (stderr): {e}")
