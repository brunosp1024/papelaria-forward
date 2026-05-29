import factory
from faker import Faker

from apps.product.models import Product

fake = Faker("pt_BR")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    code = factory.Sequence(lambda n: f"PROD-{n:05d}")
    description = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    unit_value = factory.Sequence(lambda n: f"{(n + 1) * 10:.2f}")
    commission_percentage = factory.Sequence(lambda n: f"{(n % 11):.2f}")
