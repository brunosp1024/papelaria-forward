import factory
from faker import Faker

from apps.customer.tests.factories import CustomerFactory
from apps.seller.tests.factories import SellerFactory
from apps.sale.models.sale import Sale

fake = Faker("pt_BR")


class SaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sale

    datetime = factory.LazyFunction(fake.date_time_this_year)
    customer = factory.SubFactory(CustomerFactory)
    seller = factory.SubFactory(SellerFactory)
