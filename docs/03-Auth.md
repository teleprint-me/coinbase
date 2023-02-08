# Auth

Module that implements a custom authentication for the Coinbase API using `requests.auth.AuthBase` as a base class. 

## Variables

### __agent__
```py
__agent__: str
```
The agent string to be used as the User-Agent header in the API requests.

### __source__
```py
__source__: str
```
The source string to be used as part of the User-Agent header in the API requests.

### __version__
```py
__version__: str
```
The version string to be used as part of the User-Agent header in the API requests.

## Classes

### Auth

```py
Auth(api: API = None)
```

Class that provides authentication information to the Coinbase API requests.

#### api

```py
@property
def api(self) -> API:
```

Returns the API object used to obtain authentication information.

#### header

```py
def header(self, timestamp: str, message: str) -> dict:
```

Returns a dictionary containing headers required for API authentication. The headers include User-Agent, CB-ACCESS-KEY, CB-ACCESS-SIGN, CB-ACCESS-TIMESTAMP, CB-VERSION, and Content-Type.

#### signature

```py
def signature(self, message: str) -> str:
```

Returns a hexadecimal string representation of the HMAC-SHA256 hash of the API secret and the message passed as a parameter.

#### call

```py
def __call__(self, request: PreparedRequest) -> PreparedRequest:
```

Used to add authentication headers to the request before it is sent to the API.
