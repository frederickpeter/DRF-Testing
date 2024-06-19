from rest_framework.test import APITestCase
from testing_app.models import Brand, Category
from testing_app.serializers import CategorySerializer, ProductSerializer, RetrieveProductSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from testing_app.factories import ProductFactory

class ProductSerializerTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name='Electronics')
        cls.category2 = Category.objects.create(name='Mobile')
        cls.product = ProductFactory(category=[cls.category1, cls.category2])
        
        cls.brand = Brand.objects.create(name='Apple')

        cls.file = SimpleUploadedFile(
            name='test_file.pdf',
            content=b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF',
            content_type='application/pdf'
        )
       
        cls.product_data = {
            'name': 'Tablet',
            'brand': cls.brand.pk,
            'category': [cls.category1.pk, cls.category2.pk],
            'image': cls.product.image,
            'price': cls.product.price,
            'file': SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf"),
            'stock': cls.product.stock,
        }



    # converting a python object to json/dictionary
    def test_serialization(self):
        serializer = RetrieveProductSerializer(self.product)
        expected_data = {
            'id': self.product.id,
            'name': self.product.name,
            'brand': {'id': self.product.brand_id, 'name': self.product.brand.name},
            'category': [
                {'id': self.category1.id, 'name': self.category1.name},
                {'id': self.category2.id, 'name': self.category2.name}
            ],
            'image': self.product.image.url,
            'file': self.product.file.url,
            'price': str(self.product.price),
            'stock': self.product.stock,
            'total_price': self.product.price * self.product.stock
        }
        self.assertEqual(serializer.data, expected_data)


    # converting dict/json back to python object
    def test_deserialization(self):
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.name, 'Tablet')
        self.assertEqual(product.brand, self.brand)
        self.assertEqual(product.category.count(), 2)
        self.assertEqual(product.category.first().name, self.category1.name)
        self.assertEqual(product.price, self.product.price)
        self.assertEqual(product.stock, self.product.stock)


    def test_validation(self):
        invalid_data = self.product_data.copy()
        invalid_data['price'] = '-999.99'
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)


    def test_methods(self):
        serializer = RetrieveProductSerializer(self.product)
        self.assertEqual(serializer.data['total_price'], self.product.price * self.product.stock)


    def test_update(self):
        updated_data = self.product_data.copy()
        updated_data['name'] = 'iPhone 13'
        updated_data['price'] = '1099.99'
        serializer = ProductSerializer(instance=self.product, data=updated_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_product = serializer.save()
        self.assertEqual(updated_product.name, 'iPhone 13')
        self.assertEqual(updated_product.price, Decimal('1099.99'))



    def test_nested_serializer_handling(self):
        category_serializer = CategorySerializer(data=[{'name': 'Electronics'}, {'name': 'Mobile'}], many=True)
        self.assertTrue(category_serializer.is_valid(), category_serializer.errors)
        categories = category_serializer.save()
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0].name, 'Electronics')
        self.assertEqual(categories[1].name, 'Mobile')