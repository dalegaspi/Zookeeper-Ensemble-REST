# Zookeeper-Ensemble-REST

this tool is a Flask-based REST interface for sending [four-letter commands][1] to Zookeeper ensemble.  you can send commands to a specific Zookeeper node or to a whole ensemble as configured in app.yaml


## Installation/Pre-Requisites

```sh
$ pip install flask
$ pip install requests
$ pip install pyyaml
```

## Running 
Running the service on default port 1338

```sh
$ python zkmon.py
```

## Commands

```sh
# send 'stat' command to an ensemble 'proda' defined in app.yaml returning plain text default
curl -s -X GET 'http://127.0.0.1:1338/cluster/prodb/stat'

# ...or JSON
curl -s -X GET 'http://127.0.0.1:1338/cluster/prodb/stat' -H 'Accept: application/json'

# or for a specific zk node running on ip 10.16.0.1:
curl -s -X GET 'http://127.0.0.1:1338/zk/10.16.0.1/stat' -H 'Accept: application/json'
```

## Caveats, Etc.

- ZooKeeper's native way of sending commands is through a telnet/nc interface, this is just a convenience REST interface that fronts that interface.  Therefore, the response is just what's coming back from that telnet interface, nothing more.
- This was written in a couple of hours (more-or-less) as a result of sheer laziness of running nc on the command line.  Not intended for production use at its current form.

### Version
0.1

### Licensing
OK maybe just a shout-out if you find it useful...otherwise, feel steal this code but just use it for the betterment of mankind. :-)

[four-letter commands]:http://zookeeper.apache.org/doc/r3.1.2/zookeeperAdmin.html#sc_zkCommands
