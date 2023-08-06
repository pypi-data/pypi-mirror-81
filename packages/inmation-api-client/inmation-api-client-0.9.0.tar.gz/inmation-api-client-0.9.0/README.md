![inmation header](http://www.inmation.com/images/inmation_github_header.png "inmation")

# inmation API Client

This API client can only be used with the new inmation Web API server.

## Install

Install with `pip install inmation-api-client`.

## Dependencies

* [websockets](https://github.com/aaugustin/websockets), will be installed automatically when installing with `pip`.

## Documentation

Visit the [api client documentation](https://inmation.com/docs/python-api-client/latest/index.html) page on the inmation's docs website for various usage examples and more.

## How to use it

### Advanced authentication options

- authority can be inmation, ad (Active Directory - domain account), machine (local account)

- username can be provided in 'User Principal Name' or 'Down-Level Logon Name'

source: [https://docs.microsoft.com/en-us/windows/desktop/secauthn/user-name-formats](https://docs.microsoft.com/en-us/windows/desktop/secauthn/user-name-formats)

`auth` authentication and `authorization` fields:

```json
options = {
    'auth': {
        'username': '',
        'password': '',
        'authority': 'inmation | ad | machine',
        'grant_type': 'password',
        'include_claims': ['email', 'family_name', 'given_name', 'middle_name', 'phone_number']
    },
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
}
```

`include_claims` can only be used in combination with authority set to ad. The token will not be returned
to the client but passed via the req argument into `ExecFunction` implementation.

Note: check Web API version which `authorization` options its supports.

Example Active Directory authentication:

```json
options = {
    'auth': {
        'username': 'user@domain.com',
        'password': 'secret',
        'authority': 'ad',
        'grant_type': 'password'
    }
}
```

Example Bearer token authentication:

```json
options = {
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
}
```

Example Basic authentication:

```json
options = {
    'authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
}
```

### Connect and Read example

```python
from inmation_api_client import Client, Options, Item


def create_client():
    options = Options({
        'auth': {
            'username': 'user@domain.com',
            'password': 'secret',
            'authority': 'ad',
            'grant_type': 'password'
        }
    })
    client = Client()
    client.Connect('127.0.0.1', 8002, options)

    def connection_changed(conn_info):
        print('Connection state: {}, authenticated: {}'.format(conn_info.state_string, conn_info.authenticated))
    client.OnConnectionChanged(connection_changed)

    def on_error(err):
        if err:
            print("Error: {}".format(err.message))
    client.OnError(on_error)

    return client


def main():
    items_path = "/System/Core/"

    # Make sure you have some items with historical data
    items = [Item(items_path + i) for i in ['Item01', 'Item02', 'Item03']]
    client = create_client()

    # Read values syncroniously
    response = client.Read(items)
    print(response['data'])


if __name__ == '__main__':
    main()
```

# inmation

inmation is a vendor-independent industrial system-integration specialist. Dedicated to modern technologies such as OPC UA (Unified Architecture) and document-oriented schema-less repositories, inmation opens up new horizons for enterprise real-time data management.

More information on [inmation.com](https://inmation.com)

## License

MIT