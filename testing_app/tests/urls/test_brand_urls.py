from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from testing_app.views import BrandViewSet


class BrandURLTests(APITestCase):

    def test_brand_list_url(self):
        url = reverse("brand-list")
        self.assertEqual(resolve(url).func.cls, BrandViewSet)
        self.assertEqual(resolve(url).view_name, "brand-list")

    def test_brand_detail_url(self):
        url = reverse("brand-detail", args=[1])
        self.assertEqual(resolve(url).func.cls, BrandViewSet)
        self.assertEqual(resolve(url).view_name, "brand-detail")

    def test_brand_create_url(self):
        url = reverse("brand-list")
        self.assertEqual(resolve(url).func.cls, BrandViewSet)
        self.assertEqual(resolve(url).view_name, "brand-list")

    def test_brand_update_url(self):
        url = reverse("brand-detail", args=[1])
        self.assertEqual(resolve(url).func.cls, BrandViewSet)
        self.assertEqual(resolve(url).view_name, "brand-detail")

    def test_brand_delete_url(self):
        url = reverse("brand-detail", args=[1])
        self.assertEqual(resolve(url).func.cls, BrandViewSet)
        self.assertEqual(resolve(url).view_name, "brand-detail")

    def test_brand_router_urls(self):
        list_url = reverse("brand-list")
        detail_url = reverse("brand-detail", args=[1])

        self.assertEqual(list_url, "/api/brands/")
        self.assertEqual(detail_url, "/api/brands/1/")
