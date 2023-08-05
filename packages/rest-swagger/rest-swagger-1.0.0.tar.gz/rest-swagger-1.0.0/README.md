.. role:: python(code)
   :language: python

# Rest-Swagger




#### An API documentation generator for Swagger UI and Django REST Framework


<a href="https://www.buymeacoffee.com/AjibsBaba" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-green.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>


## Installation

1. `pip install rest-swagger`

2. Add `rest_swagger` to your `INSTALLED_APPS` setting:

    ```python
        INSTALLED_APPS = (
            ...
            'rest_swagger',
        )
    ```

## Rendering Swagger Specification and Documentation

This package ships with two renderer classes:

1. `OpenAPIRenderer` generates the OpenAPI (fka Swagger) JSON schema specification. This renderer will be presented if:
  -  `Content-Type: application/openapi+json` is specified in the headers.
  - `?format=openapi` is passed as query param
2. `SwaggerUIRenderer` generates the Swagger UI and requires the `OpenAPIRenderer`


### Quick Start Example:
```python
from django.conf.urls import url
from rest_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view)
]
```

## Requirements
* Django >=2.2
* Django REST framework >=3.5
* Python >=3.7




## Bugs & Contributions
Please report bugs by opening an issue

Contributions are welcome and are encouraged!
