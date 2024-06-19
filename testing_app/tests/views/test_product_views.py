from decimal import Decimal
import json
from urllib.parse import urlparse
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from testing_app.models import Product
from testing_app.serializers import ProductSerializer, RetrieveProductSerializer
from testing_app.factories import BrandFactory, CategoryFactory, ProductFactory
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile


class ProductViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.brand = BrandFactory()
        cls.category1 = CategoryFactory()
        cls.category2 = CategoryFactory()
        cls.product = ProductFactory(
            brand=cls.brand, category=[cls.category1, cls.category2]
        )
        cls.product2 = ProductFactory(
            brand=cls.brand, category=[cls.category1, cls.category2]
        )
        cls.product_data = {
            'name': 'New Product',
            'brand': cls.brand.pk,
            'category': [cls.category1.pk, cls.category2.pk],
            'image': cls.product.image,
            'price': "99.99",
            'file': SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf"),
            'stock': 10,
        }

    def test_list_products(self):
        url = reverse("product-list")
        response = self.client.get(url)
        products = Product.objects.all()
        serializer = RetrieveProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_product(self):
        url = reverse("product-detail", kwargs={"pk": self.product.pk})
        response = self.client.get(url)
        product = Product.objects.get(pk=self.product.pk)
        serializer = RetrieveProductSerializer(product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_product(self):
        url = reverse("product-list")
        response = self.client.post(url, self.product_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        data = response.data
        self.assertEqual(data.get('name'), 'New Product')
        self.assertEqual(data.get('brand'), self.brand.pk)
        self.assertEqual(len(data.get('category')), 2)
        self.assertEqual(data.get('price'), '99.99')
        self.assertEqual(data.get('stock'), 10)

    def test_update_product(self):
        url = reverse("product-detail", kwargs={"pk": self.product.pk})
        data = {
            "name": "Updated Product",
            "brand": self.brand.id,
            "category": [self.category1.id],
            "image": self.product.image,
            "file": SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf"),
            "price": "199.99",
            "stock": 20,
        }
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")
        self.assertEqual(self.product.category.count(), 1)

    def test_delete_product(self):
        url = reverse("product-detail", kwargs={"pk": self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
