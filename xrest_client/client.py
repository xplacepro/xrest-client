import requests
from json import JSONDecodeError
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth

from .exceptions import *


class ApiResponse(object):
    def __init__(self, content=None, status_code=200, status='', operation=None):
        self.status_code = status_code
        self.status = status
        self.content = content
        self.operation = operation
        self.async = status_code == 100


def bind(path, method, allowed_params=(), required_parameters=(), primary_key=None, json_request=False):
    if primary_key:
        allowed_params += (primary_key,)

    def request(self, *args, **kwargs):
        _path = path
        # validate allowed parameters
        if kwargs:
            for k, v in kwargs.items():
                if k not in allowed_params:
                    raise ValidationError('Parameter {0} is not allowed'.format(k))
        # validate required parameters
        if required_parameters:
            parameters_keys = kwargs.keys()
            for rp in required_parameters:
                if rp not in parameters_keys:
                    raise ValidationError('Parameter {0} is not supplied'.format(rp))
        # validate primary key
        if primary_key is not None:
            primary_key_value = kwargs.pop(primary_key, None)
            if not primary_key_value:
                raise ValidationError('Primary key {0} is not supplied'.format(primary_key))
            _path = _path.format(**{primary_key: primary_key_value})

        return self._request(_path, method, json_request=json_request, **kwargs)
    return request


class BaseClient(object):
    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.session = requests.session()
        self.auth = HTTPBasicAuth(user, password)

    def _get_abs_url(self, path):
        return urljoin(self.base_url, path)

    def _request(self, path, method, json_request=False, **parameters):
        kw = {'auth': self.auth}
        if parameters:
            if json_request:
                kw['json'] = parameters
            else:
                kw['parameters'] = parameters
        result = self.session.request(method, self._get_abs_url(path), **kw)
        if result.status_code == 401:
            raise Unauthorized()
        else:
            try:
                json_result = result.json()
            except JSONDecodeError:
                raise ApiException(result.content)

            if result.status_code >= 400:
                try:
                    message = json_result['error']
                except KeyError:
                    message = str(result.content)
                raise ApiException(message)
            else:
                return ApiResponse(content=json_result['metadata'],
                                   operation=json_result.get('operation'),
                                   status_code=result.status_code)
