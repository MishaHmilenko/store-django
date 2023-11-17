import django

django.setup()

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class CreateOrderTestCase(TestCase):

    def setUp(self):
        self.data_user = {
            'first_name': 'Misha', 'last_name': 'Hmilenko',
            'username': 'misha', 'email': 'misha@gmail.com',
            'password1': 'misha23M56562', 'password2': 'misha23M56562'
        }

        self.data_order = {
            'first_name': 'tom', 'last_name': 'colin',
            'email': 'test@example.com', 'address': 'Dnipro',
            'initiator': self.data_user['username']
        }
        self.path = reverse('orders:order_create')

    def test_create_order_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Оформление заказа')
        self.assertTemplateUsed('orders/order-create.html')

    # def test_create_order_post(self):
    #     self.assertFalse(User.objects.filter(username=self.data_order['initiator']).exists())
    #     response = self.client.post(self.path, self.data_order)
