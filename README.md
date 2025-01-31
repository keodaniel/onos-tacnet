# onos_tacnet
Implementation of ONOS as an SDN Controller with Mininet emulating networks in tactical deployed scenarios

# Table of Contents
- [Prerequisites](#prerequisites)
- [Setting Up ONOS and Mininet](#setting-up-onos-and-mininet)
- [Python Experiment Scripts](#python-experiment-scripts)

# Prerequisites
- Ubuntu VM (Recommend 22.04 LTS+)
- iperf3 ```sudo apt-get install iperf3```
- vlan ```sudo apt-get install vlan```
- python3 ```sudo apt-get install python3```
- venv ```sudo apt-get install python3.12-venv```

# Setting Up ONOS and Mininet
## Install, Run, and Configure ONOS
Install Docker
```
sudo apt install docker.io
```
or use Ubuntu App Center
Pull and run ONOS Docker image (Ref: https://github.com/jatj/sdn_onos/blob/master/INSTALL.md)
```
sudo docker pull onosproject/onos
sudo docker run -t -d -p 8181:8181 -p 8101:8101 -p 5005:5005 -p 830:830 --name onos onosproject/onos
```
After creating the docker image, ensure to start the docker image.
```
sudo docker start onos
```
You can check current running dockers with the following:
```
sudo docker ps
```
Login to ONOS (Username: ```onos```  Password: ```rocks```)
```
ssh -p 8101 onos@172.17.0.1
```
Enable OpenFlow on ONOS, Proxy ARP, and Reactive Forwarding
```
app activate org.onosproject.openflow
app activate org.onosproject.fwd
app activate org.onosproject.proxyarp
```
To view the GUI visit http://172.17.0.2:8181/onos/ui or http://localhost:8181/onos/ui

Username is ```onos``` and password is ```rocks```

## Mininet Installation
Install Mininet (Ref: http://mininet.org/download/)
```
sudo apt install mininet
```
or
```
git clone https://github.com/mininet/mininet
./mininet/util/install.sh -a
```
If doing git clone, refer for common troubleshooting issue: https://github.com/intrig-unicamp/mininet-wifi/issues/536#issuecomment-2126075573

## Test Mininet Setup
Start Mininet with OpenFlow14 enabled OVS switches, connected to our ONOS SDN controller on IP ```172.17.0.2``` (using tree topology, for example)
```
sudo mn --switch ovs,protocols=OpenFlow14 --controller=remote,ip=172.17.0.2 --topo=tree,2,2
```

Without enabling the OpenFlow application on ONOS, Mininet won't be able to connect to the OpenFlow port 6653/6633. You should receive an error such as: 
```
*** Adding controller
Unable to contact the remote controller at 172.17.0.2:6653
Unable to contact the remote controller at 172.17.0.2:6633
```
To fix this you need to enable org.onosproject.openflow

# Python Experiment Scripts
## Setup Python
Set Up Python Virtual Environment in order to run python tests.
This script creates the virtual environment and installs the required package dependencies. 

You may want to read the bash code comments if you've never used virtual environments before.
```
./setup_python_virtual_environment.sh
```
Activate virtual environment
```
source venv/bin/activate
```
Proceed to running python tests

## Running Tests
### 1. Start ONOS Docker Container
```
sudo docker start onos
```

### 2. Test Basic Working Functionality
Python script to test basic functions with Mininet and ONOS before beginning experiments:
- **Pingall** starts a linear,3,2 topology on Mininet, activates Reactive Forwarding, and conducts a pingall test to show basic connectivity.
- **Intents** conducts a pingall test for ONOS to collect all host information, then generates and deletes HostIntents in ONOS to show basic ONOS REST API interaction.
- **Path** conducts a pingall test then collects and records the paths taken between each host pair.
- **Basic Link Automation** conducts pingall test using Reactive Forwarding or Host Intents
- **Dynamic Paths** tests whether link failover will cause link automation tool to create new path

```
python3 functions_test.py
```

### 3. Fault Tolerance Experiment
Conducts 20 trials of 20 seconds iPerf3 tests, where link failure is induced and path is rerouted by selected link automation tool. 

iperf3 output logs can be graphed in post to data visualize the fault tolerance of the link automation tool. 

Various network use scenarios are represented by utilizing iperf3 options.

*Script may take hours to run due to conducting 20 trials. Recommend changing trial runs variable or just ending script early and viewing log files*
```
python3 fault_tolerance_test.py
```

### 4. Implementing Bandwidth Meters with Flowrules
```
python3 bandwidth_control_test.py
```

### 5. Implementing VLANs
```
python3 vlan_test.py
```

### 6. Implementing VLANs with Metered Flowrules / Quality of Service
```
python3 qos_test.py
```

### 7. Manual Testing
Example mininet command
```
sudo mn --switch ovs,protocols=OpenFlow14 --controller remote,ip=172.17.0.2 --mac --custom ~/onos-tacnet/custom/tacnet.py --topo=VLAN
```

### Troubleshooting Tips
ONOS sometimes has unexpected issues or unresolved bugs, whether it be HostIntents not providing link connectivity, or meters being installed with letters for MeterIDs which cannot be deleted or purged. When all else fails, you can try restarting your Docker container ```sudo docker restart onos```, clear ONOS's data and cache directory. ```onos:shutdown -c -r```
