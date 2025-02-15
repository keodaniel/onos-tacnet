This directory should hold configuration files for custom mininets.

See custom_example.py, which loads the default minimal topology.  The advantage of defining a mininet in a separate file is that you then use the --custom option in mn to run the CLI or specific tests with it.

To start up a mininet with the provided custom topology, do:
```
sudo mn --custom topokeo.py --topo topokeo
```

Example using sf_onos-tacnet/custom shared folder:
```
sudo mn --switch ovs,protocols=OpenFlow14 --controller=remote,ip=172.17.0.2 --mac --custom ../../media/sf_onos-tacnet/custom/tacnet.py --topo=DFGW
```
