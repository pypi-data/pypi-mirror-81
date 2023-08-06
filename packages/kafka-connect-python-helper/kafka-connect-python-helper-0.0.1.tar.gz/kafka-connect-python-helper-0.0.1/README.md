# AACB Kafka Connect Helper

## Description
This package can be used to simplify HTTP command for the Kafka Connect REST API. The package is created spefically for deploying connectors automatically, but can also be used to simplify one-time commands.

## Dependencies and limitations
The package heavily relies on the Requests package and is currently designed to expect that the Requests session is created upfront.

The code must still be extended to support other Connect REST commands (e.g. resume/pause and POSTs).

## Usage
Prepare the requests session and setup the helper library, for example for a Connect REST API with SASL_SSL:
```
import requests
import logging
from connect_helper import ConnectHelper

logging.basicConfig(level=logging.INFO)

username = "dummy"
password = "supersecret"
base_url = "https://localhost:8083"

s = requests.Session()
s.verify = ca_cert
s.auth = (username, password)

connect = ConnectHelper(s, base_url)

r = connect.get_connectors()
```

