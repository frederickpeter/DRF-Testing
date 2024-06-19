from django.db import IntegrityError
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from testing_app.models import Category, Brand, Product
from decimal import Decimal

class ProductModelTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        cls.file = SimpleUploadedFile(
            name='test_file.pdf',
            content=b'',
            content_type='application/pdf'
        )

        cls.category = Category.objects.create(name='Electronics')
        cls.brand = Brand.objects.create(name='Apple')
        cls.product = Product.objects.create(
            name='iPhone',
            brand=cls.brand,
            image=cls.image,
            file=cls.file,
            price=999.99,
            stock=50
        )
        cls.product.category.add(cls.category)


    def test_product_creation(self):
        self.assertIsInstance(self.product, Product)
        self.assertEqual(self.product.name, 'iPhone')
        self.assertEqual(self.product.brand, self.brand)
        self.assertIn(self.category, self.product.category.all())
        self.assertTrue(self.product.image)
        self.assertTrue(self.product.file)
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.stock, 50)


    def test_product_str(self):
        self.assertEqual(str(self.product), 'iPhone')


    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="iPhone",
                brand=self.brand,
                image=self.image,
                file=self.file,
                price=Decimal('15.00'),
                stock=50
            )

    def test_is_in_stock(self):
        self.assertTrue(self.product.is_in_stock())
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock())

    def test_brand_name_property(self):
        self.assertEqual(self.product.brand_name, 'Apple')

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            Product.objects.create(
                name='MacBook',
                brand=self.brand,
                image=self.image,
                file=self.file,
                price=-1999.99,
                stock=10
            )

    def test_negative_stock(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name='MacBook',
                brand=self.brand,
                image=self.image,
                file=self.file,
                price=1999.99,
                stock=-10
            )

    def test_update_product(self):
        self.product.name = 'iPhone 13'
        self.product.price = 1099.99
        self.product.save()
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, 'iPhone 13')
        self.assertEqual(updated_product.price, Decimal('1099.99'))

    def test_delete_product(self):
        product_id = self.product.id
        self.product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product_id)

    def test_product_method_validation(self):
        self.product.price = -100
        with self.assertRaises(ValueError):
            self.product.save()

    def test_price_max_digits(self):
        with self.assertRaises(Exception):
            Product.objects.create(
                name="Invalid Price Product",
                brand=self.brand,
                image=self.image,
                file=self.file,
                price=Decimal('10000000000.00'),  # exceeds max_digits=9
                stock=10
            )

    
    def test_data_length_error(self):
         # create a product with the name attribute of 101 chars
        product = Product(
            name="A" * 101,
            brand=self.brand,
            image=self.image,
            file=self.file,
            price=Decimal('15.00'),
            stock=50
        )
        with self.assertRaises(ValidationError):
            product.full_clean()
            product.save()

    def test_product_methods(self):
        self.assertTrue(callable(self.product.is_in_stock))
        self.assertTrue(callable(self.product.save))
        self.assertTrue(hasattr(self.product, 'brand_name'))
        self.assertEqual(self.product.brand_name, self.brand.name)
