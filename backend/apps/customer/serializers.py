from rest_framework import serializers
from apps.core.serializers.serializers import PersonSerializer
from apps.customer.models import Customer


class CustomerCreateUpdateSerializer(PersonSerializer):
    class Meta:
        model  = Customer
        fields = [
            "id",
            "name",
            "email",
            "phone"
        ]

class CustomerDetailSerializer(PersonSerializer):

    class Meta:
        model  = Customer
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "created_at",
            "updated_at"
        ]

class CustomerListSerializer(PersonSerializer):

    class Meta:
        model  = Customer
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "created_at",
            "updated_at"
        ]
