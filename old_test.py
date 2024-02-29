import subprocess
from time import sleep
import paramiko
from interact_onos import start_onos_docker, toggle_fwd, create_intents

# Function to start custom Mininet topology connected to a remote controller
def start_mininet(topology):
    topology_file = "../../media/sf_onos-tacnet/custom/tacnet.py"
    
    # Clean up Mininet before starting a new topology
    clean_output = subprocess.run(["sudo", "mn", "-c"], capture_output=True, text=True, check=False)
    if "*** Cleanup complete." in clean_output.stderr:
        print("*** Cleanup complete.")

    # Start Mininet with the specified topology
    command = ['sudo', 'mn', '--switch', 'ovs,protocols=OpenFlow14', '--controller', 'remote,ip=172.17.0.2', '--mac', '--custom', topology_file, '--topo=' + topology]
    return subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Function to conduct pingall
def conduct_pingall(mininet_process):
    stderr_data = ''
    while True:
        stderr_chunk = mininet_process.stderr.read1()
        if stderr_chunk:
            stderr_data += stderr_chunk.decode()
        if "Starting CLI" in stderr_data:
            # print(stderr_data)
            break
    
    toggle_fwd("activate")
    # sleep(10)
    command1 = b'pingall\n'
    mininet_process.stdin.write(command1)
    mininet_process.stdin.flush()
    # toggle_fwd("deactivate")
    sleep(10)
    command2 = b'h1 ping h2 -c 3\n'
    mininet_process.stdin.write(command2)
    mininet_process.stdin.flush()

    create_intents()

    mininet_process.stdin.close()
    counter = 0
    while True:
        sleep(1)
        print(counter)
        counter += 1

        stderr_chunk = mininet_process.stderr.read1()
        stderr_data += stderr_chunk.decode()
        if "*** Done" in stderr_data:
            break
    print(stderr_data)


# Main function
def main():
    start_onos_docker()
    # toggle_fwd("activate")

    mininet_process = start_mininet("DFGW")
    conduct_pingall(mininet_process)

    # sleep(10)
    # conduct_pingall(mininet_process)
    # mininet_process.communicate()

    # conduct_pingall(mininet_process)

if __name__ == "__main__":
    main()
