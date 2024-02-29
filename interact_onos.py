import requests
# import json
import subprocess
import paramiko
import logging
from time import sleep

# Function to start ONOS Docker container
def start_onos_docker():
    try:
        if b'onos' in subprocess.check_output(['sudo', 'docker', 'ps', '--format', '{{.Names}}']):
            logging.info("ONOS Docker container is already running.")
        else:
            logging.info("Starting ONOS Docker container.")
            subprocess.Popen(['sudo', 'docker', 'start', 'onos'])
            while b'onos' not in subprocess.check_output(['sudo', 'docker', 'ps', '--format', '{{.Names}}']):
                logging.info("Waiting for ONOS")
                sleep(1)
            sleep(60)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while starting ONOS Docker container: {e}")

def toggle_fwd(action):
    try:
        # Connect to the SSH server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('172.17.0.1', port=8101, username='onos', password='rocks')
        
        # Construct the command to activate or deactivate forward
        command = f'app {action} fwd\n'

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # Log output
        for line in stdout:
            logging.info(line.strip())
        
        ssh.close()  # Close the SSH connection
    except Exception as e:
        logging.error(f"Error while toggling forward: {e}")

def create_host_intents():
    # Define variables
    ONOS_USER = "onos"
    ONOS_PASSWORD = "rocks"
    CONTROLLER_IP = "172.17.0.1"
    CONTROLLER_PORT = "8181"
    HOSTS_ENDPOINT = "/onos/v1/hosts"
    INTENTS_ENDPOINT = "/onos/v1/intents"
    PRIORITY = 55

    try:
        # Construct the URL to retrieve MAC addresses
        url = f"http://{CONTROLLER_IP}:{CONTROLLER_PORT}{HOSTS_ENDPOINT}"

        # Make the request to retrieve MAC addresses
        response = requests.get(url, auth=(ONOS_USER, ONOS_PASSWORD))

        # Check if the request was successful
        response.raise_for_status()

        # Extract MAC addresses from the response and sort them
        mac_addresses = sorted([host["mac"] for host in response.json()["hosts"]])

        # Log the retrieved and sorted MAC addresses
        logging.info("MAC addresses of hosts connected to the ONOS controller (sorted):")
        for mac in mac_addresses:
            logging.info(mac)

        # Create intents for unique pairs of hosts
        for i in range(len(mac_addresses)):
            for j in range(i + 1, len(mac_addresses)):
                # Create an intent from mac_addresses[i] to mac_addresses[j]
                intent_data = {
                    "type": "HostToHostIntent",
                    "appId": "org.onosproject.ovsdb",
                    "priority": PRIORITY,
                    "one": f"{mac_addresses[i]}/-1",
                    "two": f"{mac_addresses[j]}/-1"
                }

                # Make the request to create the intent
                create_intent_url = f"http://{CONTROLLER_IP}:{CONTROLLER_PORT}{INTENTS_ENDPOINT}"
                response = requests.post(create_intent_url, auth=(ONOS_USER, ONOS_PASSWORD), json=intent_data)

                # Check if the request was successful
                response.raise_for_status()

                # Log the result
                logging.info(f"Creating intent from {mac_addresses[i]} to {mac_addresses[j]}...")
                logging.info(response.text)

    except requests.RequestException as e:
        logging.error(f"Error while creating intents: {e}")
