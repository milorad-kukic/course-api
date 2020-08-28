from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        email = "kukic.milorad@gmail.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = "someUser@GMAIL.com"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, 'someUser@gmail.com')

    def test_new_user_with_invalid_email_should_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'password')

    def test_create_new_super_user(self):
        user = get_user_model().objects.create_superuser(
            'test@gmial.com',
            'test_password'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)