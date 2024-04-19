#!/bin/bash

curl -X DELETE -u onos:rocks --header 'Accept: application/json' 'http://172.17.0.1:8181/onos/v1/flows/application/keo'

curl -X POST -u onos:rocks --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
  "priority": 999,
  "timeout": 0,
  "isPermanent": true,
  "deviceId": "of:0000000000000001",
  "treatment": {
    "instructions": [
      {
        "type": "OUTPUT",
        "port": "2"
      }
    ]
  },
  "selector": {
    "criteria": [
      {
        "type": "ETH_DST",
        "mac": "00:00:00:00:00:02"
      },
      {
        "type": "ETH_SRC",
        "mac": "00:00:00:00:00:01"
      },
      {
        "type": "IN_PORT",
        "port": 1
      }
    ]
  }
}' 'http://172.17.0.1:8181/onos/v1/flows/of:0000000000000001?appId=keo'

curl -X POST -u onos:rocks --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
  "priority": 999,
  "timeout": 0,
  "isPermanent": true,
  "deviceId": "of:0000000000000001",
  "treatment": {
    "instructions": [
      {
        "type": "OUTPUT",
        "port": "1"
      }
    ]
  },
  "selector": {
    "criteria": [
      {
        "type": "ETH_DST",
        "mac": "00:00:00:00:00:01"
      },
      {
        "type": "ETH_SRC",
        "mac": "00:00:00:00:00:02"
      },
      {
        "type": "IN_PORT",
        "port": 2
      }
    ]
  }
}' 'http://172.17.0.1:8181/onos/v1/flows/of:0000000000000001?appId=keo'
