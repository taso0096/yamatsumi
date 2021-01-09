# YAMATSUMI
This is a visualization tool for network.
A sample of packet forwarder is [here](https://github.com/taso0096/yamatsumi/tree/master/packet_forwarder).

# Installation
```bash
git clone https://github.com/taso0096/yamatsumi.git
cd yamatsumi
```

# Usage
## Run
```bash
docker-compose up -d
```
Now you can visit [https://localhost:8623](https://localhost:8623) to view login page.

## Create User
```bash
docker-compose run backend python manage.py createsuperuser
```

# Author
[taso0096](https://twitter.com/taso0096)
