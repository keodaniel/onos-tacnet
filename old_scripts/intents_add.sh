#!/bin/bash

# Define variables
ONOS_USER="onos"
ONOS_PASSWORD="rocks"
CONTROLLER_IP="172.17.0.1"
CONTROLLER_PORT="8181"
HOSTS_ENDPOINT="/onos/v1/hosts"
INTENTS_ENDPOINT="/onos/v1/intents"
PRIORITY=55

# Construct the curl command to retrieve MAC addresses
CURL_COMMAND="curl -s -u ${ONOS_USER}:${ONOS_PASSWORD} --header 'Accept: application/json' 'http://${CONTROLLER_IP}:${CONTROLLER_PORT}${HOSTS_ENDPOINT}'"

# Execute the curl command and extract MAC addresses using jq, then sort them
MAC_ADDRESSES=($(eval "${CURL_COMMAND}" | jq -r '.hosts[].mac' | sort))

# Print the retrieved and sorted MAC addresses
echo "MAC addresses of hosts connected to the ONOS controller (sorted):"
printf '%s\n' "${MAC_ADDRESSES[@]}"

# Create intents for unique pairs of hosts
for ((i = 0; i < ${#MAC_ADDRESSES[@]}; i++)); do
    for ((j = i+1; j < ${#MAC_ADDRESSES[@]}; j++)); do
        # Create an intent from MAC_ADDRESSES[i] to MAC_ADDRESSES[j]
        INTENT_DATA='{
            "type": "HostToHostIntent",
            "appId": "org.onosproject.ovsdb",
            "priority": '${PRIORITY}',
            "one": "'${MAC_ADDRESSES[i]}'/-1",
            "two": "'${MAC_ADDRESSES[j]}'/-1"
        }'

        # Construct the curl command to create the intent
        CREATE_INTENT_COMMAND="curl -s -X POST -u ${ONOS_USER}:${ONOS_PASSWORD} --header 'Content-Type: application/json' --header 'Accept: application/json' -d '${INTENT_DATA}' 'http://${CONTROLLER_IP}:${CONTROLLER_PORT}${INTENTS_ENDPOINT}'"

        # Execute the curl command to create the intent
        echo "Creating intent from ${MAC_ADDRESSES[i]} to ${MAC_ADDRESSES[j]}..."
        eval "${CREATE_INTENT_COMMAND}"
    done
done
