# FMCAPIClient
[Firepower REST API Guides](https://www.cisco.com/c/en/us/support/security/defense-center/products-programming-reference-guides-list.html 'Firepower REST API Guides')<br />

---

![PyPI - Status](https://img.shields.io/pypi/status/FMCAPIClient)
![PyPI - Format](https://img.shields.io/pypi/format/FMCAPIClient)
![GitHub](https://img.shields.io/github/license/vsantiago113/FMCAPIClient)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/vsantiago113/FMCAPIClient)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/FMCAPIClient)

An API Client for the Cisco Firepower Management Center to be able to easily use the API in a more standard way.

## How to install
```ignorelang
$ pip install FMCAPIClient
```

## Usage
The argument 'method' must be specify every time.

Note: The class will validate the token, and refresh the token when needed as this validation method is called in between each method call.

NOTE:

#### Default arguments and attributes
```python
import FMCAPIClient

client = FMCAPIClient.Client(verify=False, warnings=False, api_version='v1')

client.get(url=None, method='', data=None, auth = None)

# client.headers
# client.base_url
# client.token
# client.auth
# client.token_expire
# client.token_refresh
# client.token_refresh_count
# client.domain_uuid
# client.server

```

#### Authentication
```python
import FMCAPIClient

client = FMCAPIClient.Client()
client.connect(url='https://FMC-server.local', username='admin', password='Admin123')

client.disconnect()
```

#### Refresh Token
```python
import FMCAPIClient

client = FMCAPIClient.Client()
client.connect(url='https://FMC-server.local', username='admin', password='Admin123')

client.refresh_token_func()

client.disconnect()
```

#### The first query
```python
import FMCAPIClient
import json

client = FMCAPIClient.Client()
client.connect(url='https://FMC-server.local', username='admin', password='Admin123')

response = client.get(method='/devicegroups/devicegrouprecords')
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Getting detailed information
```python
import FMCAPIClient
import json

client = FMCAPIClient.Client()
client.connect(url='https://FMC-server.local', username='admin', password='Admin123')

response = client.get(method=f'/devicegroups/devicegrouprecords', expanded=True)
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Filtering
```python
import FMCAPIClient
import json

client = FMCAPIClient.Client()
client.connect(url='https://FMC-server.local', username='admin', password='Admin123')

group_id = '81fe2042-9ad2-11ea-be78-cde812596ba2'
response = client.get(method=f'/devicegroups/devicegrouprecords/{group_id}')
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Paging
```python
import FMCAPIClient
import json

client = FMCAPIClient.Client()
client.connect(url='https://FMC-server.local', username='admin', password='Admin123')


response = client.get(method=f'/devicegroups/devicegrouprecords', offset=0, limit=1)
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Creating
```python
import FMCAPIClient
import json

client = FMCAPIClient.Client()
client.connect(url='https://FMC-server.local', username='admin', password='Admin123')

response = client.post(method='/devicegroups/devicegrouprecords', data={'name': 'test_group',
                                                                        'type': 'DeviceGroup'})
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Updating
```python
import FMCAPIClient
import json

client = FMCAPIClient.Client()
client.connect(url='https://FMC-server.local', username='admin', password='Admin123')

group_id = '1234567890abc'
response = client.put(method=f'/devicegroups/devicegrouprecords/{group_id}', data={'id': group_id,
                                                                                   'name': 'test_group_updated',
                                                                                   'type': 'DeviceGroup'})
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Deleting
```python
import FMCAPIClient
import json

client = FMCAPIClient.Client()
client.connect(url='https://FMC-server.local', username='admin', password='Admin123')

group_id = '1234567890abc'
response = client.delete(method=f'/devicegroups/devicegrouprecords/{group_id}')
print(json.dumps(response.json(), indent=4))

client.disconnect()
```
