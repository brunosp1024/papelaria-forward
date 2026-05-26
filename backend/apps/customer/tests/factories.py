import factory
from faker import Faker
from apps.customer.models import Customer

fake = Faker('pt_BR')


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.LazyFunction(lambda: fake.name())
    email = factory.Sequence(lambda n: f"customer{n}@example.com")
    phone = factory.Sequence(lambda n: f"1199999{n:04d}")
