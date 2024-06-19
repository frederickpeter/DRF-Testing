from django.db import IntegrityError
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError
from testing_app.models import Brand

class BrandModelTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(name='Apple')
        cls.brand2 = Brand.objects.create(name='Toshiba')

    def test_brand_creation(self):
        self.assertIsInstance(self.brand, Brand)
        self.assertEqual(self.brand.name, 'Apple')
        self.assertEqual(self.brand.pk, 1)


    def test_brand_str(self):
        self.assertEqual(str(self.brand2), 'Toshiba')


    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="Apple")


    def test_update_brand(self):
        self.brand.name = 'Dell'
        self.brand.save()
        updated_brand = Brand.objects.get(id=self.brand.id)
        self.assertEqual(updated_brand.name, 'Dell')

    def test_delete_brand(self):
        brand_id = self.brand.id
        self.brand.delete()
        with self.assertRaises(Brand.DoesNotExist):
            Brand.objects.get(id=brand_id)

    
    def test_data_length_error(self):
         # create a brand with the name attribute of 101 chars
        brand = Brand(name="A" * 101)
        with self.assertRaises(ValidationError):
            brand.full_clean()
            brand.save()

