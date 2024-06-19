from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class Brand(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    file = models.FileField(upload_to='files/')
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    @property
    def brand_name(self):
        return self.brand.name

    def save(self, *args, **kwargs):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        super().save(*args, **kwargs)
