import django

django.setup()

from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Misha', 'last_name': 'Hmilenko',
            'username': 'misha', 'email': 'misha@gmail.com',
            'password1': 'misha23M56562', 'password2': 'misha23M56562'
        }

        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed('users/registration.html')

    def test_user_registration_post(self):

        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginViewTestCase(TestCase):

    def setUp(self):
        self.username = 'testusername'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.path = reverse('users:login')

    def test_user_login_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Авторизация')
        self.assertTemplateUsed('users/login.html')

    def test_success_user_login_post(self):
        login_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.path, login_data, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(self.user.is_authenticated)
        self.assertRedirects(response, reverse('index'))

    def test_error_user_login_post(self):
        login_data = {
            'username': 'invalid_username',
            'password': 'invalid_password'
        }
        response = self.client.post(self.path, login_data, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response,
        'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.',
            html=True
        )
