================
XRest api client
================

Installation
------------

pip install git+git://github.com/xplacepro/xrest-client.git


Usage
-----

Api client class
================

.. code-block:: python

    from xrest_client.client import BaseClient, bind

    BASE_URL = 'http://test.local'
    ALL_URL = '/api/1.0/test/'
    ONE_URL = '/api/1.0/test/{id}/'


    class TestApiClient(BaseClient):
        all = bind(ALL_URL, 'GET')
        one = bind(ONE_URL, 'GET', primary_key='id')
        update = bind(ONE_URL, 'POST',
                      primary_key='id',
                      allowed_params=('obj',),
                      required_parameters=('obj',),
                      json_request=True)
        delete = bind(ONE_URL, 'DELETE',
                      primary_key='id',
                      json_request=True)
