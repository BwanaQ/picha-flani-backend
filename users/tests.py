from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework import status

import jwt
from users.models import *


import logging

# Disable logging during tests
logging.disable(logging.CRITICAL)


JWT_SECRET_KEY = getattr(settings, 'SECRET_KEY', None)


def decode_token(encoded_jwt):
    decoded_jwt = jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=['HS256'])
    return decoded_jwt


class UserRegisterViewTest(TestCase):
    def setUp(self):

        self.client = APIClient()
        # No Authorization header needed
        self.headers = {
            # 'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            # 'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            # 'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)

    def test_register_valid_credentials(self):
        response = self.client.post(
            reverse('users:register'),
            {'username': 'eddy', 'email': 'test@test.com', 'password': 'testpass', 'role': 'customer'}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.json()['data'])

    def test_register_invalid_credentials(self):
        response = self.client.post(
            reverse('users:register'),
            {'username': 'eddy', 'email': 'test@test.com', 'password': '', 'role': 'customer'}
        )

        self.assertEqual(response.status_code, 400)
        
    def test_register_role_not_provided(self):
        response = self.client.post(
            reverse('users:register'),
            {'username': 'eddy', 'email': 'test@test.com', 'password': ''}
        )
        self.assertEqual(response.status_code, 400)


class ObtainEmailAuthTokenTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()

        self.token = self.user.token

        self.client = APIClient()
        # Not requird but will be needed in other endpoints
        self.headers = {
        }
        self.client.credentials(**self.headers)

    def test_get_token_valid_credentials(self):

        response = self.client.post(
            reverse('users:login'),
            {'email': 'test@test.com', 'password': 'password'}
        )

        decoded_user_id = decode_token(response.json()['data']['token'])['id']
        # profile_obj = Profile.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

        self.assertTrue('token' in response.json()['data'])
        self.assertEqual(decoded_user_id, str(self.user.id))


    def test_get_token_invalid_credentials(self):
        response = self.client.post(
            reverse('users:login'),
            {'email': 'test@test.com', 'password': 'wrongpass'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
