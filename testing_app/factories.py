import factory
from .models import Brand, Category, Product
from factory.django import DjangoModelFactory


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Faker('company')

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    brand = factory.SubFactory(BrandFactory)
    image = factory.django.ImageField(color='blue')
    file = factory.django.FileField(filename='test.pdf')
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=1, max=100)

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of categories were passed in, use them
            for category in extracted:
                self.category.add(category)
        else:
            # Create random categories
            for _ in range(2):
                self.category.add(CategoryFactory())


