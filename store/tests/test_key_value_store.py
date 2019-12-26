from collections import OrderedDict
from faker import Faker
from django.urls import reverse
from key_value_store.settings import redis_client as redis
from key_value_store.test_cases import CustomTestCase


class KeyValueStoreTest(CustomTestCase):
    
    def setUp(self):
        self.url = reverse('key-value-api')
        self.fake = Faker()

        self.data = {
            'name': self.fake.first_name(),
            'first_name': self.fake.first_name(),
            'email': 'raisulru10@gmail.com',
            'phone': '01723864330',
            'description': self.fake.address()
        }
        
        self.ordered_dict = OrderedDict(self.data)
        for key, value in self.ordered_dict.items():
            redis.set(key, value)
            redis.expire(key, 5)

        super(KeyValueStoreTest, self).setUp()

    def test_key_value_get(self):
        request = self.client.get(self.url)
        self.assertSuccess(request)

        self.assertEqual(request.data['name'].decode('utf-8'), self.data['name'])
        self.assertEqual(request.data['first_name'].decode('utf-8'), self.data['first_name'])
        self.assertEqual(request.data['email'].decode('utf-8'), self.data['email'])
        self.assertEqual(request.data['phone'].decode('utf-8'), self.data['phone'])
        self.assertEqual(request.data['description'].decode('utf-8'), self.data['description'])
    
    def test_key_value_get_with_query_params(self):
        request = self.client.get(self.url, {'keys': 'name,email'})
        self.assertSuccess(request)

        self.assertEqual(request.data['name'].decode('utf-8'), self.data['name'])
        self.assertEqual(request.data['email'].decode('utf-8'), self.data['email'])

        self.assertEqual(request.data.get('first_name'), None)
        self.assertEqual(request.data.get('phone'), None)
        self.assertEqual(request.data.get('description'), None)

    def test_key_value_post(self):
        data = {
            'name': self.fake.first_name(),
            'first_name': self.fake.first_name(),
            'email': 'raisulru10@gmail.com',
            'phone': '01723864330',
            'description': self.fake.address()
        }

        request = self.client.post(self.url, data)
        self.assertCreated(request)

    def test_key_value_patch(self):
        data = {'name': 'Sujon'}
        request = self.client.patch(self.url, data)
        self.assertSuccess(request)

        value = redis.get('name')
        self.assertEqual(value.decode('utf-8'), data['name'])

        data = {'last_name': 'Islam'}
        request = self.client.patch(self.url, data)
        self.assertNotFound(request)


