# API

The `API` module handles the creation of an API class for accessing the Coinbase REST API.

## Variables

None

## Functions

### get_api_settings

```py
def get_api_settings() -> dict:
```

Loads API keys and secrets from environment variables and returns a dictionary containing the API key, API secret, API REST endpoint, and API feed.

## Classes

### API

```py
API(settings: dict = field(default_factory=get_api_settings)) -> API
```

A class that provides access to the Coinbase REST API. 

API has default API settings obtained from environment variables, and the default can be overridden by passing `settings` as an argument when instantiating the API class.

The API class is a base class for API classes with default API settings obtained from environment variables.

#### API.settings

```py
settings: dict = field(default_factory=get_api_settings)
```

A dictionary containing API key, API secret, API REST endpoint, and API feed, loaded from environment variables.

#### API.key

```py
@property
def key(self) -> str:
```

A property that returns the API key.

#### API.secret

```py
@property
def secret(self) -> str:
```

A property that returns the API secret.

#### API.rest

```py
@property
def rest(self) -> str:
```

A property that returns the API REST endpoint.

#### API.version

```py
@property
def version(self) -> int:
```

A property that returns the API version number (2).

#### API.path

```py
def path(self, value: str) -> str:
```

Takes in a string and returns a URL path for the Coinbase API, adding the version number if not already present.

#### API.url

```py
def url(self, value: str) -> str:
```

Takes in a string and returns a URL for accessing the Coinbase API, using the REST endpoint and versioned path.

### AdvancedAPI

A subclass of the `API` class, providing access to the advanced version of the Coinbase API.

#### AdvancedAPI.version

```py
@property
def version(self) -> int:
```

A property that returns the advanced API version number (3).

#### AdvancedAPI.path

```py
def path(self, value: str) -> str:
```

Takes in a string and returns a URL path for the advanced Coinbase API, adding the version number if not already present.

### WebSocketAPI

A subclass of the `AdvancedAPI` class, providing access to the Coinbase WebSocket API.

#### WebSocketAPI.feed

```py
@property
def feed(self) -> str:
```

A property that returns the API feed endpoint for the Coinbase WebSocket API.
