#!/bin/bash

curl -X POST -u onos:rocks --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   "type": "HostToHostIntent",
   "appId": "org.onosproject.ovsdb",
   "priority": 55,
   "one": "00:00:00:00:00:01/-1",
   "two": "00:00:00:00:00:02/-1"
 }' 'http://172.17.0.1:8181/onos/v1/intents'
 
