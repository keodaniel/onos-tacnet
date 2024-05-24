#!/bin/bash

# Function to start a new tmux session
new_session() {
    local session_name="$1"
    local command="$2"
    echo "Starting new tmux session: $session_name"
    tmux new-session -d -s "$session_name" "$command"
    sleep 2

    if ! tmux ls | grep -q "$session_name"; then
        echo "Error: $session_name connection failed, retry later."
        exit 1
    fi
}

# Function to close a tmux session
close_session() {
    local session_name="$1"
    if [[ $session_name == *"onos"* ]]; then
        tmux send-keys -t "$session_name" "logout" Enter
    else
        tmux send-keys -t "$session_name" "exit" Enter
    fi
    sleep 1
}

# Function to clean tmux sessions
kill_sessions() {
    if tmux ls > /dev/null 2>&1; then
        echo "Clearing tmux sessions"
        tmux kill-server
    else
        echo "No tmux sessions found"
    fi
}

# Function to send keys and check until finished by checking for the CLI prompt
send_keys() {
    local session_name="$1"
    local command="$2"
    local completion_msg="$3"
    local tail_lines="$4"

    tmux send-keys -t "$session_name" "$command" Enter

    while ! tmux capture-pane -p -t "$session_name" | tail -n "$tail_lines" | grep -q "$completion_msg"; do
        sleep 1
    done
}

# Start ONOS Docker container if not already running
start_onos_docker() {
    if sudo docker ps --format '{{.Names}}' | grep -q "onos"; then
        echo "ONOS Docker container is already running."
    else
        sudo docker start onos > /dev/null 2>&1
        echo "Starting ONOS Docker container."

        while ! sudo docker ps --format '{{.Names}}' | grep -q "onos"; do
            echo "Waiting for ONOS"
            sleep 1
        done
        sleep 60
    fi
}

# Function to activate or deactivate reactive forwarding
toggle_fwd() {
    local action="$1"
    local session_name="onos_toggle_fwd_$action"
    local action_msg="Activated" && [[ $action == "deactivate" ]] && action_msg="Deactivated"

    new_session "$session_name" "sshpass -p 'rocks' ssh -p 8101 onos@172.17.0.1"
    send_keys "$session_name" "app $action fwd" "$action_msg org.onosproject.fwd" 10
    close_session "$session_name"
}

# Function to start Mininet with a specified topology
start_mininet() {
    local topo_cmd="$1"
    local session_name="mininet_session_$topo_cmd"
    local custom_script="../../media/sf_onos-tacnet/custom/tacnet.py"

    new_session "$session_name" "sudo mn --switch ovs,protocols=OpenFlow14 --controller=remote,ip=172.17.0.2 --mac --custom $custom_script --topo=$topo_cmd"
    echo "Starting Mininet with topology: $topo_cmd"

    while ! tmux capture-pane -p -t "$session_name" | grep -q "password"; do
        sleep 1
    done
    send_keys "$session_name" "password" "Starting CLI" 10
    sleep 10
}

# Function to execute pingall command in Mininet session and filter output
mininet_ping() {
    local topo_cmd="$1"
    local session_name="mininet_session_$topo_cmd"

    send_keys "$session_name" "time pingall" "mininet>" 1

    line_number=$(tmux capture-pane -p -t "$session_name" | grep -n "*** Ping" | tail -n 1 | cut -d ':' -f 1)
    pingall_output=$(tmux capture-pane -p -t "$session_name" | tail -n +$line_number | head -n -1)
    summary_output=$(echo "$pingall_output" | grep -E "Ping|Results|Elapsed")

    echo "$pingall_output"

    sleep 1
}


# Function to close Mininet session
close_mininet() {
    local topo_cmd="$1"
    local session_name="mininet_session_$topo_cmd"
    close_session "$session_name"
}

# Function to display intents summary
intents_summary() {
    local session_name="$1"

    send_keys "$session_name" "intents -m" "onos@root >" 1

    line_number=$(tmux capture-pane -p -t "$session_name" | grep -n "intents -m" | tail -n 1 | cut -d ':' -f 1)
    echo "Intents Summary:"
    tmux capture-pane -p -t "$session_name" | tail -n +$((line_number+1)) | head -n -3
}

# Function to retrieve intents from ONOS
get_intents() {
    local session_name="onos_get_intents"
    new_session "$session_name" "sshpass -p 'rocks' ssh -p 8101 onos@172.17.0.1"
    intents_summary "$session_name"
    close_session "$session_name"
}

# Function to purge intents from ONOS
purge_intents() {
    local session_name="onos_purge_intents"
    new_session "$session_name" "sshpass -p 'rocks' ssh -p 8101 onos@172.17.0.1"
    send_keys "$session_name" "remove-intent -p org.onosproject.ovsdb" "onos@root >" 4
    intents_summary "$session_name"

    tmux_output=$(tmux capture-pane -p -t "$session_name" | grep "All")
    if echo "$tmux_output" | grep -q "All (0)"; then
        echo "Purged Intents Successfully"
    else
        echo "Purged Intents Failed"
    fi
    close_session "$session_name"
}

# Function to test reactive forwarding and log the results
test_reactivefwd() {
    # Log file path
    logname="reactivefwd_testlog"
    timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
    LOG_FILE="script_logs/${logname}_${timestamp}.txt"
    test_case="Reactive Forwarding"
    echo "Testing ${test_case} for Link Automation..." 2>&1 | tee -a "$LOG_FILE"

    # Main
    {
        kill_sessions
        start_onos_docker
        toggle_fwd "activate"
        start_mininet "DFGW"
        mininet_ping "DFGW"
        close_mininet "DFGW"
    } >> "$LOG_FILE" 2>&1

    # Report
    {
        if echo "$summary_output" | grep -q "0% dropped"; then
            echo "$summary_output"
            echo "Success using ${test_case}" 
        else
            echo "$summary_output" 
            echo "Failed using ${test_case}, try again."
        fi
    } 2>&1 | tee -a "$LOG_FILE"
}


# Function to test host intents and log the results
test_host_intents() {
    # Log file path
    logname="host_intents_testlog"
    timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
    LOG_FILE="script_logs/${logname}_${timestamp}.txt"
    test_case="Host Intents"
    echo "Testing ${test_case} for Link Automation..." 2>&1 | tee -a "$LOG_FILE"

    # Main
    {
        kill_sessions
        start_onos_docker
    
        # Using ReactiveFwd and Pingall so ONOS recognizes hosts
        toggle_fwd "activate"
        start_mininet "DFGW"
        mininet_ping "DFGW"

        # Deactivate ReactiveFwd and create Host Intents
        toggle_fwd "deactivate"
        /media/sf_onos-tacnet/intents_add.sh 
        get_intents 
        mininet_ping "DFGW" 
        close_mininet "DFGW" 
        purge_intents 
    } >> "$LOG_FILE" 2>&1

    # Report
    {
        if echo "$summary_output" | grep -q "0% dropped"; then
            echo "$summary_output"
            echo "Success using ${test_case}" 
        else
            echo "$summary_output" 
            echo "Failed using ${test_case}, try again."
        fi
    } 2>&1 | tee -a "$LOG_FILE"
}

# Main
test_reactivefwd
test_host_intents
echo "done"


