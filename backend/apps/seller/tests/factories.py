import factory
from faker import Faker

from apps.seller.models import Seller

fake = Faker("pt_BR")


class SellerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Seller

    code = factory.Sequence(lambda n: f"S{n:05d}")
    name = factory.LazyFunction(lambda: fake.name())
    email = factory.Sequence(lambda n: f"seller{n}@example.com")
    phone = factory.Sequence(lambda n: f"1198888{n:04d}")
