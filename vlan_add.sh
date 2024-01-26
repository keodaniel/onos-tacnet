#!/bin/bash

# ONOS controller details
ONOS_IP="127.0.0.1"
ONOS_PORT="8181"
ONOS_USER="onos"
ONOS_PASSWORD="rocks"

# Function to assign VLAN to a host using curl
assign_vlan_to_host() {
    local host_mac=$1
    local vlan_id=$2

    # Construct VLAN assignment data
    local data='{
        "type": "VLAN",
        "mac": "'$host_mac'",
        "vlanId": '$vlan_id'
    }'

    # Send POST request to create VLAN assignment intent
    curl -s -X POST -u "${ONOS_USER}:${ONOS_PASSWORD}" \
        --header 'Content-Type: application/json' \
        --header 'Accept: application/json' \
        -d "${data}" \
        "http://${ONOS_IP}:${ONOS_PORT}/onos/v1/intents"

    # Check response status
    if [ $? -eq 0 ]; then
        echo "VLAN assignment created successfully for host with MAC ${host_mac}"
    else
        echo "Failed to create VLAN assignment for host with MAC ${host_mac}"
    fi
}

# Example usage:
# Assume you have a list of hosts with their MAC addresses and desired VLAN IDs
hosts_with_vlans=(
    {"mac": "00:00:00:00:00:01", "vlan_id": 100}
    {"mac": "00:00:00:00:00:02", "vlan_id": 200}
    # Add more hosts as needed
)

# Assign VLANs to hosts
for host in "${hosts_with_vlans[@]}"; do
    assign_vlan_to_host "${host["mac"]}" "${host["vlan_id"]}"
done
