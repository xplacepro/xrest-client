import unittest
import httpretty

from xrest_client.client import BaseClient, bind
from xrest_client.exceptions import ValidationError

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


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        httpretty.enable()
        self.client = TestApiClient(BASE_URL, '', '')

    def testAllMethod(self):
        httpretty.register_uri(httpretty.GET, BASE_URL+ALL_URL,
                               body='{"type": "sync", "status": 200, "metadata": {"objects": [{"obj": 1}]}}',
                               content_type='application/json')

        response = self.client.all()
        self.assertDictEqual(response.content, {'objects': [{'obj': 1}]})
        self.assertEqual(response.status_code, 200)

    def testOneMethod(self):
        httpretty.register_uri(httpretty.GET, BASE_URL+ONE_URL.format(id=1),
                               body='{"type": "sync", "status": 200, "metadata": {"object": {"obj": 1}}}',
                               content_type='application/json')

        response = self.client.one(id=1)
        self.assertDictEqual(response.content, {'object': {'obj': 1}})
        self.assertEqual(response.status_code, 200)

    def testUpdateMethod(self):
        httpretty.register_uri(httpretty.POST, BASE_URL+ONE_URL.format(id=1),
                               body='{"type": "sync", "status": 200, "metadata": {"object": {"obj": 1}}}',
                               content_type='application/json')

        with self.assertRaises(ValidationError):
            response = self.client.update(id=1)

        response = self.client.update(id=1, obj=2)
        self.assertDictEqual(response.content, {'object': {'obj': 1}})
        self.assertEqual(response.status_code, 200)

    def testDeleteMethod(self):
        httpretty.register_uri(httpretty.DELETE, BASE_URL+ONE_URL.format(id=1),
                               body='{"type": "sync", "status": 200, "metadata": {"object": {"obj": 1}}}',
                               content_type='application/json')

        with self.assertRaises(ValidationError):
            response = self.client.delete()

        response = self.client.delete(id=1)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
