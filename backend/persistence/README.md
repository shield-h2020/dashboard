# Recommendations Persistence

The security recommendations get persisted whenever DARE sends a new one. The persistence purpose is to provide a track record of which security measures were applied, the ones pending, and context information for each recommendation.

## Architecture

The recommendations persistence comprises two components, one for the persistence logic and another which provides a RESTful API for CRUD operations on said recommendations.

A recommendation application (i.e., sent to the vNSF so the perceived threat is countered as per the configuration stated in the recommendation) is done through the API. Upon commanded to do so the API conveys the recommendation to the Orchestrator so it can be applied to the vNSFs in question. This process is depicted in the sequence below.

![Apply recommendation](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=VXNlci0-K0FQSTogQXBwbHkgcmVjb21tZW5kYXRpb24KQVBJLT4rT3JjaGVzdHJhdG9yABIXABcMLT4tAE0FUgA_DSBhcHBsaWVkAE4GLVVzZXI6IERvbmUK&s=rose)

### Datastore

The data persisted for each recommendation is:

```python
policy_model = {
    # The tenant to whom the policy is for.
    'tenant_id': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Time and date when the thread was detected. Format: ISO 8601.
    'detection': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # The severity assigned to the threat. Format: user-defined.
    'severity': {
        'type': 'integer',
        'empty': False,
        'required': True
    },

    # The applicability of the policy for the tenant in question. Format: user-defined.
    'status': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # The kind of network attack. Format: user-defined.
    'attack': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # The recommendation to counter the threat. Format: user-defined.
    'recommendation': {
        'type': 'string',
        'empty': False,
        'required': True
    }
}
```

### API

The API to interact with the recommendations follows the RESTful principles and serves for CRUD operations on the recommendations.

The API documentation follows the [OpenAPI Specification](https://swagger.io/specification/) (fka Swagger RESTful API Documentation Specification) Version 2.0 and is defined in the [swagger.yaml](swagger.yaml) file. To have it in a user-friendly way simple paste its contents into the [Swagger Editor](https://editor.swagger.io/) and navigate the documentation Swagger style.


## Implementation

The implementation makes use of the following modules:

**Datastore**

* [settings.py](settings.py) defines the datastore documents schema.

**API**

* [api.py](api.py) sets up the API through the [Eve REST API framework](http://eve.readthedocs.io/en/stable/).
* [persistence.py](dashboardpersistence.py/persistence.py) implements the persistence-tailored-operations such as conveying a recommendation to the Orchestrator (which makes use of the [Orchestrator Adapter](../vnsfo/README.md)).
