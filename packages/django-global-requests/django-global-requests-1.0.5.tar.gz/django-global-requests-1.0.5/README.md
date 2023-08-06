# Django Global Requests

Allows for global request objects in your django project

## Installation

`pip install django-global-requests`

## Configuration

1. Add to installed apps:

```
INSTALLED_APPS = [
     ...
     'global_requests',
]
```

2. Add middleware:
```
MIDDLEWARE = [
    ...
    'global_requests.GlobalRequestMiddleware',
]

```

## Usage

```
import get_request from global_requests
request = get_request()
```



  