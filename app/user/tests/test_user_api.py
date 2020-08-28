from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(email, password, **params):
    get_user_model().objects.create_user(
        email=email,
        password=password,
        **params
    )


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_valid_user_success(self):
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'John Doe',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_should_return_404_if_password_length_is_less_than_5(self):
        payload = {
            'email': 'test@gmail.com',
            'password': '1234',
            'name': 'John Doe'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_should_return_BAD_REQUEST_if_user_already_exist(self):
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'John Doe',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        payload = {
            'email': 'user@host.com',
            'password': 'password'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        create_user(email='test@gmail.com', password='testpassword')
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrong_password'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_is_not_created_if_user_doesnt_exist(self):
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrong_password'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
