from rest_framework.test import APITestCase
from testing_app.models import Brand, Category
from testing_app.serializers import BrandSerializer, CategorySerializer, ProductSerializer, RetrieveProductSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from testing_app.factories import ProductFactory

class BrandSerializerTest(APITestCase):

    @classmethod
    def setUpTestData(cls):        
        cls.brand = Brand.objects.create(name='Apple')
       
        cls.brand_data = {
            'name': 'Tablet'
        }

    # converting a python object to json/dictionary
    def test_serialization(self):
        serializer = BrandSerializer(self.brand)
        expected_data = {
            'id': self.brand.id,
            'name': self.brand.name,
        }
        self.assertEqual(serializer.data, expected_data)


    # converting dict/json back to python object
    def test_deserialization(self):
        serializer = BrandSerializer(data=self.brand_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        brand = serializer.save()
        self.assertEqual(brand.name, 'Tablet')
        self.assertEqual(brand.pk, brand.pk)



    def test_validation(self):
        invalid_data = self.brand_data.copy()
        invalid_data['name'] = ''
        serializer = BrandSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


    def test_update(self):
        updated_data = self.brand_data.copy()
        updated_data['name'] = 'Samsung'
        serializer = BrandSerializer(instance=self.brand, data=updated_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_brand = serializer.save()
        self.assertEqual(updated_brand.name, 'Samsung')


    def test_nested_serializer_handling(self):
        brand_serializer = BrandSerializer(data=[{'name': 'T-shirts'}, {'name': 'Shirts'}], many=True)
        self.assertTrue(brand_serializer.is_valid(), brand_serializer.errors)
        brands = brand_serializer.save()
        self.assertEqual(len(brands), 2)
        self.assertEqual(brands[0].name, 'T-shirts')
        self.assertEqual(brands[1].name, 'Shirts')