from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product


class ProductTests(APITestCase):

    def setUp(self):
        # создаём продукт, который будет использоваться в тестах
        self.product = Product.objects.create(title="Молоко",
                                              description="1 литр")
        self.list_url = reverse('product-list')  # /api/v1/products/

    def test_get_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Молоко")

    def test_create_product(self):
        data = {"title": "Хлеб", "description": "Багет", "price": 80}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.last().title, "Хлеб")
