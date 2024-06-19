from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from testing_app.models import Brand
from testing_app.serializers import (
    BrandSerializer,
    RetrieveProductSerializer,
)
from testing_app.factories import BrandFactory
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class BrandViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.brand = BrandFactory(name="Brand1")
        cls.brand2 = BrandFactory(name="Brand2")

        cls.brand_data = {"name": "New Brand"}
        cls.token = cls.generate_jwt_token(cls.user)

    @classmethod
    def generate_jwt_token(cls, user):
        access_token = AccessToken.for_user(user)
        return str(access_token)

    def test_list_brands_unauthenticated(self):
        url = reverse("brand-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_brands_authenticated(self):
        url = reverse("brand-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(url)
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_brand_unauthenticated(self):
        url = reverse("brand-detail", kwargs={"pk": self.brand.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_brand_authenticated(self):
        url = reverse("brand-detail", kwargs={"pk": self.brand.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(url)
        brand = Brand.objects.get(pk=self.brand.pk)
        serializer = BrandSerializer(brand)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_brand_unauthenticated(self):
        url = reverse("brand-list")
        response = self.client.post(url, self.brand_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_brand_authenticated(self):
        url = reverse("brand-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.post(url, self.brand_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Brand.objects.count(), 3)
        data = response.data
        self.assertEqual(data.get("name"), "New Brand")

    def test_update_brand_unauthenticated(self):
        url = reverse("brand-detail", kwargs={"pk": self.brand.pk})
        data = {"name": "Updated Brand"}
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_brand_authenticated(self):
        url = reverse("brand-detail", kwargs={"pk": self.brand.pk})
        data = {"name": "Updated Brand"}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.brand.refresh_from_db()
        self.assertEqual(self.brand.name, "Updated Brand")

    def test_delete_brand_unauthenticated(self):
        url = reverse("brand-detail", kwargs={"pk": self.brand.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_brand_authenticated(self):
        url = reverse("brand-detail", kwargs={"pk": self.brand.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Brand.objects.filter(pk=self.brand.pk).exists())
