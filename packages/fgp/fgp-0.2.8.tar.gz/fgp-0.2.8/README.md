# fgp-api-python
Python client for Future Grid Platform API

>
> **Work in progress!**
> This is still under active design.
>
> (dragons be here).

### Installation 
```
pip install fgp
```

### On the command line
The module will install a command line wrapper, `fgp` which will allow you to perform common API operations on the command line.
```bash
➜ fgp --help                                                                                                                                               
2020-04-28 14:55:17,591 - fgp - INFO - Configured logger
Usage: fgp [OPTIONS] COMMAND [ARGS]...

Options:
  --api-url TEXT          Futuregrid API url
  --api-app TEXT          Futuregrid API application name
  --api-header-host TEXT  Host header for HTTP requests
  --help                  Show this message and exit.

Commands:
  extension
  relation
  store
```

#### Using environment variables
All parameters may be provided as environment variables, provided:
 - as all uppercase,
 - replace dash with underscore
 - prefix with `FGP_`

The following commands are both valid:
```
fgp --api-url http://localhost:18082 --api-app ada store --device-type meter --store-name meterPqStore get-first-last --device-name 9990000001_9880000001
```
and
```
export FGP_API_URL=http://localhost:18082
export FGP_API_APP=ada
fgp store --device-type meter --store-name meterPqStore get-first-last --device-name 9990000001_9880000001
```

### In a Docker container
```
➜ docker run --net host --rm -it fgp-api-python --api-url http://localhost:18082 extension --device-type meter --extension-name meter_no get --device-name 9990000001_9880000001
2020-04-28 05:13:25,058 - fgp - INFO - Configured logger
2020-04-28 05:13:25.060 | DEBUG    | fgp.cli.extension.commands:get:32 - Fetching extension value for extension=meter_no device=9990000001_9880000001 at timestamp=None
{
  "deviceKey": {
    "id": "f674e867-e987-4373-a292-96ea7657ed87"
  },
  "meterNo": "9990000001",
  "timeKey": 1582820145000,
  "timeKeyAsDate": 1582820145000,
  "timestamp": 1582820145000
}

```

### In your application
```python
import fgp
import datetime

# Initialise the client with your server url and application name
client = fgp.ApiClient(
    url='http://localhost:8082', 
    application='myapp', 
    # Headers: optional, but useful if you're port forwarding to a kubernetes environment and need to use
    # a hostname to hit the correct ingress
    headers={
        'Host': 'api.some-environment.domain.com'    
    }
)

# Request data for a device
df = client.store.get_data(
    device_type='meter', 
    store_name='meterPqStore',
    date_from=datetime.datetime(year=2019, month=10, day=1),
    date_to=datetime.datetime(year=2019, month=10, day=2),
    fields=['voltageA', 'currentA'],
    devices=['9000000002_9000000002']
)

# Request extension for a device
result = client.extension.get_at(
    device_type='meter',
    device_name='9990000001_9880000001',
    extension_name='meter_no'
)

# Request a device relationship
result = client.relation.get_at(
    device_type='meter',
    device_name='9990000001_9880000001',
    relation_name='meter_transformer'
)

# Query some reference data
client.reference.query(
    reference_name='event_reference',
    query='eventState==NEW;nmi==9880000001',
    order_by="timeKey",
    limit=100,
    page=0
)

```

### Planned
- Update events
