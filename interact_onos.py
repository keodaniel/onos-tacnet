import requests
import json
import subprocess
import paramiko
import logging
from time import sleep
import urllib.parse

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

def get_mac_addresses():
    # Define variables
    ONOS_USER = "onos"
    ONOS_PASSWORD = "rocks"
    CONTROLLER_IP = "172.17.0.1"
    CONTROLLER_PORT = "8181"
    HOSTS_ENDPOINT = "/onos/v1/hosts"

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

        return mac_addresses

    except requests.RequestException as e:
        logging.error(f"Error while retrieving MAC addresses: {e}")
        return []

def create_host_intents(mac_addresses):
    # Define variables
    ONOS_USER = "onos"
    ONOS_PASSWORD = "rocks"
    CONTROLLER_IP = "172.17.0.1"
    CONTROLLER_PORT = "8181"
    INTENTS_ENDPOINT = "/onos/v1/intents"
    PRIORITY = 55

    try:
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

                if response.text:
                    logging.info(response.text)

    except requests.RequestException as e:
        logging.error(f"Error while creating intents: {e}")

def get_intents():
    # Define variables
    ONOS_USER = "onos"
    ONOS_PASSWORD = "rocks"
    CONTROLLER_IP = "172.17.0.1"
    CONTROLLER_PORT = "8181"
    INTENTS_ENDPOINT = "/onos/v1/intents"

    try:
        # Construct the URL to retrieve intents
        url = f"http://{CONTROLLER_IP}:{CONTROLLER_PORT}{INTENTS_ENDPOINT}"

        # Make the request to retrieve intents
        response = requests.get(url, auth=(ONOS_USER, ONOS_PASSWORD))

        # Check if the request was successful
        response.raise_for_status()

        # Extract and log the retrieved intents
        intents = response.json().get("intents", [])
        if intents:
            logging.info("List of intents:")
            for intent in intents:
                appId = intent.get("appId")
                key = intent.get("key")
                logging.info(f"AppId: {appId}, Key: {key}")
        else:
            logging.info("No intents found.")

        return intents

    except requests.RequestException as e:
        logging.error(f"Error while retrieving intents: {e}")
        return []

def clear_intent(appId, key):
    # Define variables
    ONOS_USER = "onos"
    ONOS_PASSWORD = "rocks"
    CONTROLLER_IP = "172.17.0.1"
    CONTROLLER_PORT = "8181"
    INTENTS_ENDPOINT = f"/onos/v1/intents/{appId}/{key}"

    try:
        # Construct the URL to clear intents
        url = f"http://{CONTROLLER_IP}:{CONTROLLER_PORT}{INTENTS_ENDPOINT}"

        # Make the DELETE request to clear intents
        response = requests.delete(url, auth=(ONOS_USER, ONOS_PASSWORD))

        # Check if the request was successful
        response.raise_for_status()
        # logging.info("Intents cleared successfully.")

    except requests.RequestException as e:
        logging.error(f"Error while clearing intents: {e}")

def clear_all_intents():
    logging.info("Starting to clear all intents.")
    try:
        while True:
            # Retrieve all intents
            intents = get_intents()

            if not intents:
                # logging.info("No intents found. Exiting the loop.")
                break

            # Log the number of intents found
            logging.info(f"Found {len(intents)} intents to clear.")

            # Iterate over each intent and clear it
            for index, intent in enumerate(intents, start=1):
                appId = intent.get("appId")
                key = intent.get("key")
                logging.info(f"Clearing intent {index}/{len(intents)} - AppId: {appId}, Key: {key}")
                clear_intent(appId, key)

            # Wait for last intent to clear
            sleep(1)
        logging.info("All intents cleared successfully.")
    except Exception as e:
        logging.error(f"An error occurred while clearing intents: {e}")

def get_flows():
    # Define variables
    ONOS_USER = "onos"
    ONOS_PASSWORD = "rocks"
    CONTROLLER_IP = "172.17.0.1"
    CONTROLLER_PORT = "8181"
    FLOWS_ENDPOINT = "/onos/v1/flows"

    try:
        # Construct the URL to retrieve flows
        url = f"http://{CONTROLLER_IP}:{CONTROLLER_PORT}{FLOWS_ENDPOINT}"

        # Make the request to retrieve flows
        response = requests.get(url, auth=(ONOS_USER, ONOS_PASSWORD))

        # Check if the request was successful
        response.raise_for_status()

        # Extract and return the retrieved flows
        flows = response.json().get("flows", [])
        return flows

    except requests.RequestException as e:
        logging.error(f"Error while retrieving flows: {e}")
        return []

def encode_mac_address(mac_address):
    # URL encode the MAC address
    encoded_mac_address = urllib.parse.quote(mac_address+"/None", safe="")
    # Append "/None" to signify absence of VLAN information
    encoded_mac_address_with_none = encoded_mac_address

    return encoded_mac_address_with_none

def get_path(source_mac, destination_mac):
    '''Get the path between two MAC addresses using the ONOS REST API.
    Returns a list of paths, where each path is a list of switches, beginning and ending with the source and destination MAC address.'''
    # Define variables
    ONOS_USER = "onos"
    ONOS_PASSWORD = "rocks"
    CONTROLLER_IP = "172.17.0.1"
    CONTROLLER_PORT = "8181"
    PATHS_ENDPOINT = f"/onos/v1/paths/{encode_mac_address(source_mac)}/{encode_mac_address(destination_mac)}"

    try:
        # Construct the URL
        url = f"http://{CONTROLLER_IP}:{CONTROLLER_PORT}{PATHS_ENDPOINT}"

        # Make the GET request
        response = requests.get(url, auth=(ONOS_USER, ONOS_PASSWORD))

        # Check if the request was successful
        response.raise_for_status()

        # Extract paths from the response
        path_list = []
        path = []
        for path_dict in response.json().get("paths", []):
            path.append(source_mac)
            for link in path_dict.get("links", []):
                dst = link.get("dst")
                if dst.get("device"):
                    path.append(dst["device"])
            path.append(destination_mac)

            # Log the paths
            path_list.append(path)
            logging.info(f"Path between {source_mac} and {destination_mac}: {path}")


        # Return the paths
        return path_list

    except requests.RequestException as e:
        logging.error(f"Error while retrieving paths: {e}")
        return []

def get_all_paths(mac_addresses):
    all_paths = []

    for source_mac in mac_addresses:
        for destination_mac in mac_addresses:
            if source_mac != destination_mac:
                all_paths.append(get_path(source_mac, destination_mac))

    return all_paths
