from collections import OrderedDict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TagsGetApiTest(APITestCase):
    fixtures = ["product.json"]

    def test_tags_get(self):
        url = reverse("product_api:tags-api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = OrderedDict([("id", 1), ("name", "4K-разрешение")])
        self.assertEqual(response.data[0], data)


class ProductGetApiTest(APITestCase):
    fixtures = ["product.json"]

    def test_product_get(self):
        url = reverse("product_api:product-api", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.data["title"], "PlayStation 4 Slim")
        self.assertEqual(response.data["salePrice"], "400.00")
