# Packet Forwarder
This is a sample packet forwarder available on [YAMATSUMI](https://github.com/taso0096/yamatsumi).

# Dependency
* Python3.8

# Installation
```bash
pip install -r requirements.txt
cp config.example.py config.py
```

# Usage
## Config
Write to config.py.

### Example
```python
SOCKETIO_HOST = 'http://localhost:5000'
NETWORK_ID = 'test_network'
INTERFACES = ['en0']
```

* SOCKETIO_HOST
YAMATSUMI API URL(http://localhost:5000)
Only available in this URL now. (https://localhost:8623 is unavailable.)

* NETWORK_ID
The network id created in YAMATSUMI.

* INTERFACES
Name of the NIC that you want to monitor.
Must be an array.

## Run
```bash
python main.py
```

# Author
[taso0096](https://twitter.com/taso0096)
