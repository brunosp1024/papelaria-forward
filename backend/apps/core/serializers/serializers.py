from rest_framework import serializers
from utils.validators import validate_phone as validate_phone_util


class PersonSerializer(serializers.ModelSerializer):

    def validate_phone(self, value):
        if not value:
            return None

        validate_phone_util(value)

        qs = self.Meta.model.objects.filter(phone=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Telefone já cadastrado no sistema.')

        return value
