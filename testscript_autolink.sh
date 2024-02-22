#!/bin/bash

kill_sessions() {
    if tmux ls | grep -q "session"; then
        tmux ls | grep -q "session"
        echo "Clearing tmux sessions"
        tmux kill-session -a
        if tmux ls | grep -q "session"; then
            tmux kill-session
        fi
    fi
}

# Function to start a new tmux session
new_session() {
    local session_name="$1"
    local command="$2"
    # echo "Starting new tmux session: $session_name"
    tmux new-session -d -s "$session_name" "$command"
    sleep 1
}

# Function to close a tmux session
close_session() {
    local session_name="$1"
    # echo "Closing tmux session: $session_name"
    if [[ $session_name == *"onos"* ]]; then
        tmux send-keys -t "$session_name" "logout" Enter
    else
        tmux send-keys -t "$session_name" "exit" Enter
    fi
    sleep 1
}

# Function to check if ONOS Docker container is already running
start_onos() {
    if sudo docker ps --format '{{.Names}}' | grep -q "onos"; then
        echo "ONOS Docker container is already running."
    else
        sudo docker start onos > /dev/null 2>&1
        echo "Starting ONOS Docker container."
        sleep 20
    fi
}

# Function to start SSH session in a new tmux session and check Reactive Forwarding
enable_fwd() {
    local session_name="enable_fwd_session"
    new_session "$session_name" "sshpass -p 'rocks' ssh -p 8101 onos@172.17.0.1"

    if ! tmux ls | grep -q "$session_name"; then
        echo "Error: sshpass connection failed, retry later."
        exit 1
    fi

    tmux send-keys -t "$session_name" "app activate fwd" Enter
    while ! tmux capture-pane -p -t "$session_name" | grep "Activated org.onosproject.fwd"; do
        sleep 1
    done

    # echo "Checking active ONOS applications..."
    # tmux send-keys -t "$session_name" "apps -s -a" Enter

    # while ! tmux capture-pane -p -t "$session_name" | tail -n 1 | grep -q "onos@root >"; do
    #     sleep 1
    # done

    # if tmux capture-pane -p -t "$session_name" | grep -q "\* 111 org.onosproject.fwd"; then
    #     echo "Reactive Forwarding is Enabled"
    # else
    #     echo "Reactive Forwarding is Currently Not Enabled... "
    #     tmux send-keys -t "$session_name" "app activate fwd" Enter
    #     while ! tmux capture-pane -p -t "$session_name" | grep "Activated org.onosproject.fwd"; do
    #         sleep 1
    #     done
    # fi

    close_session "$session_name"
}

# Function to start Mininet in a new tmux session with a specified topology
open_mininet() {
    local topo_cmd="$1"
    local session_name="mininet_session_$topo_cmd"
    new_session "$session_name" "sudo mn --switch ovs,protocols=OpenFlow14 --controller=remote,ip=172.17.0.2 --mac --custom ../../media/sf_onos-tacnet/custom/tacnet.py --topo=$topo_cmd"
    echo "Starting Mininet with topology: $topo_cmd"

    while ! tmux capture-pane -p -t "$session_name" | grep -q "password"; do
        sleep 1
    done
    
    tmux send-keys -t "$session_name" "password" Enter

    while ! tmux capture-pane -p -t "$session_name" | grep -q "Starting CLI"; do
        sleep 1
    done
    sleep 1
}

mininet_ping() {
    local topo_cmd="$1"
    local session_name="mininet_session_$topo_cmd"
    tmux send-keys -t "$session_name" "time pingall" Enter

    while ! tmux capture-pane -p -t "$session_name" | grep -q "Elapsed"; do
        # Capture the output of tmux capture-pane into a variable
        sleep 1
        tmux_output=$(tmux capture-pane -p -t mininet_session)
    done

    # Use grep to filter out only the lines containing the pingall command, results, or "->"
    filtered_output=$(echo "$tmux_output" | grep -E "Ping|Results|Elapsed|->")

    # Print the filtered output
    echo "$filtered_output"
    sleep 1
}

close_mininet() {
    local topo_cmd="$1"
    local session_name="mininet_session_$topo_cmd"
    # sleep 1
    # tmux attach-session -t "$session_name"
    close_session "$session_name"
}

# Function to disable forwarding
disable_fwd() {
    local session_name="disable_fwd_session"
    new_session "$session_name" "sshpass -p 'rocks' ssh -p 8101 onos@172.17.0.1"

    if ! tmux ls | grep -q "$session_name"; then
        echo "Error: sshpass connection failed, retry later."
        exit 1
    fi

    tmux send-keys -t "$session_name" "app deactivate fwd" Enter
    while ! tmux capture-pane -p -t "$session_name" | grep "Deactivated org.onosproject.fwd"; do
        sleep 1
    done

    close_session "$session_name"
}

test_reactivefwd() {
    # Log file path
    logname="reactivefwd_testlog"
    timestamp=$(date +"%Y-%m-%d_%H-%M")
    LOG_FILE="script_logs/${logname}_${timestamp}.txt"

    # Main
    kill_sessions 2>&1 | tee -a "$LOG_FILE"
    start_onos 2>&1 | tee -a "$LOG_FILE"
    enable_fwd 2>&1 | tee -a "$LOG_FILE"
    open_mininet "DFGW" 2>&1 | tee -a "$LOG_FILE"
    mininet_ping "DFGW" 2>&1 | tee -a "$LOG_FILE"
    close_mininet "DFGW" 2>&1 | tee -a "$LOG_FILE"
    # disable_fwd 2>&1 | tee -a "$LOG_FILE"
    echo "done" 2>&1 | tee -a "$LOG_FILE"
}

test_reactivefwd

test_host_intents() {
    # Log file path
    logname="host_intents_testlog"
    timestamp=$(date +"%Y-%m-%d_%H-%M")
    LOG_FILE="script_logs/${logname}_${timestamp}.txt"

    # Main
    kill_sessions 2>&1 | tee -a "$LOG_FILE"
    start_onos 2>&1 | tee -a "$LOG_FILE"
    enable_fwd 2>&1 | tee -a "$LOG_FILE"
    open_mininet "DFGW" 2>&1 | tee -a "$LOG_FILE"
    mininet_ping "DFGW" 2>&1 | tee -a "$LOG_FILE"
    disable_fwd 2>&1 | tee -a "$LOG_FILE"
    /media/sf_onos-tacnet/intents_add.sh 2>&1 | tee -a "$LOG_FILE"
    sleep 1
    mininet_ping "DFGW" 2>&1 | tee -a "$LOG_FILE"
    close_mininet "DFGW" 2>&1 | tee -a "$LOG_FILE"
    echo "done" 2>&1 | tee -a "$LOG_FILE"
}

# test_host_intents

# Main script
# kill_sessions >> "$LOG_FILE" 2>&1
# start_onos >> "$LOG_FILE" 2>&1
# enable_fwd >> "$LOG_FILE" 2>&1
# check_mininet "base" >> "$LOG_FILE" 2>&1
# check_mininet "DFGW" >> "$LOG_FILE" 2>&1
# check_mininet "BW" >> "$LOG_FILE" 2>&1
# disable_fwd >> "$LOG_FILE" 2>&1

# check_mininet "base" >> "$LOG_FILE" 2>&1
# check_mininet "DFGW" >> "$LOG_FILE" 2>&1
# check_mininet "BW" >> "$LOG_FILE" 2>&1

