from rest_framework import serializers
from apps.core.serializers.serializers import PersonSerializer
from apps.customer.models import Customer


class CustomerCreateUpdateSerializer(PersonSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone"]
        read_only_fields = ["id"]


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
