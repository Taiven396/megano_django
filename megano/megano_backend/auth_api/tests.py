import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase



class SignInOutApiTest(APITestCase):
    fixtures = ['auth.json', 'user.json']

    def test_sign_in_out(self):
        url = reverse('auth_api:sign-in')
        data = {
            'username' : 'Katy',
            'password' : '123456',
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('auth_api:sign-out')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileGetApiTest(APITestCase):
    fixtures = ['auth.json', 'user.json']

    def test_profile(self):
        url = reverse('auth_api:sign-in')
        data = {
            'username' : 'Sam',
            'password' : '123456',
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('auth_api:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['fullName'], 'Горков Сэм Антонович')
        self.assertEqual(response.data['email'], 'Sam@sam.lj')
        url = reverse('auth_api:sign-out')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfilePostApiTest(APITestCase):
    fixtures = ['auth.json', 'user.json']

    def test_profile_post(self):
        url = reverse('auth_api:sign-in')
        data = {
            'username' : 'Tom',
            'password' : '123456',
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('auth_api:profile')
        data = {
            'fullName' : 'Test Test',
            'email' : 'test@test.ru',
            'phone' : '+7 911 123 43 54',
            'avatar' : {
                'src' : '',
                'alt' : '',
            }
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.data['fullName'], 'Test Test')
        self.assertEqual(response.data['email'], 'test@test.ru')
        self.assertEqual(response.data['phone'], '+7 911 123 43 54')
        url = reverse('auth_api:sign-out')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





