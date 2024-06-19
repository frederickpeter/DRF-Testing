from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from testing_app.views import ProductViewSet


class ProductURLTests(APITestCase):

    def test_product_list_url(self):
        url = reverse("product-list")
        self.assertEqual(resolve(url).func.cls, ProductViewSet)
        self.assertEqual(resolve(url).view_name, "product-list")

    def test_product_detail_url(self):
        url = reverse("product-detail", args=[1])
        self.assertEqual(resolve(url).func.cls, ProductViewSet)
        self.assertEqual(resolve(url).view_name, "product-detail")

    def test_product_create_url(self):
        url = reverse("product-list")
        self.assertEqual(resolve(url).func.cls, ProductViewSet)
        self.assertEqual(resolve(url).view_name, "product-list")

    def test_product_update_url(self):
        url = reverse("product-detail", args=[1])
        self.assertEqual(resolve(url).func.cls, ProductViewSet)
        self.assertEqual(resolve(url).view_name, "product-detail")

    def test_product_delete_url(self):
        url = reverse("product-detail", args=[1])
        self.assertEqual(resolve(url).func.cls, ProductViewSet)
        self.assertEqual(resolve(url).view_name, "product-detail")

    def test_product_router_urls(self):
        list_url = reverse("product-list")
        detail_url = reverse("product-detail", args=[1])

        self.assertEqual(list_url, "/api/products/")
        self.assertEqual(detail_url, "/api/products/1/")
