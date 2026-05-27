from rest_framework import serializers
from apps.core.serializers.serializers import PersonSerializer
from apps.seller.models import Seller


class SellerCreateUpdateSerializer(PersonSerializer):
    class Meta:
        model  = Seller
        fields = ["id", "name", "email", "phone"]
        read_only_fields = ["id"]


class SellerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Seller
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by"
        ]


class SellerListSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Seller
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by"
        ]
