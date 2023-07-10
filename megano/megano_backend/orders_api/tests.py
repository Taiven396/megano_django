import json
from collections import OrderedDict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class OrderTestApi(APITestCase):
    fixtures = ['product.json', 'orders.json', 'user.json', 'auth.json']

    def test_order_get(self):
        url = reverse('auth_api:sign-in')
        data = {
            'username' : 'Katy',
            'password' : '123456'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('frontend:order-pk', kwargs={'pk' : 1})
        response = self.client.get(url)
        self.assertEqual(response.data['fullName'], 'Папкина Екатерина Антоновна')
        self.assertEqual(response.data['city'], 'Москва')
        url = reverse('auth_api:sign-out')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

