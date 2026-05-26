from apps.core.serializers.serializers import PersonSerializer
from apps.seller.models import Seller


class SellerCreateUpdateSerializer(PersonSerializer):
    class Meta:
        model  = Seller
        fields = [
            "id",
            "name",
            "email",
            "phone"
        ]


class SellerDetailSerializer(PersonSerializer):

    class Meta:
        model  = Seller
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "created_at",
            "updated_at"
        ]


class SellerListSerializer(PersonSerializer):

    class Meta:
        model  = Seller
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "created_at",
            "updated_at"
        ]
