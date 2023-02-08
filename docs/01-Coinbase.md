# Coinbase

This module contains important information about the `teleprint-me/coinbase` package, including its source code repository, version, and request rate limit.

## Variables

### __agent__

```py
__agent__: str
```

The identifier of the agent using the package.

### __source__

```py
__source__: str
```

The URL of the source code repository for the package.

### __version__

```py
__version__: str
```

The version number of the `teleprint-me/coinbase` package.

### __limit__

```py
__limit__: float
```

The rate limit of the API, expressed as the number of seconds between each allowed request. This is calculated as the reciprocal of the number of requests that can be made per hour, divided by the number of seconds per hour. The rate limit is 0.36 seconds.
