from rest_framework import serializers
from .models import Storage

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['id', 'address', 'company']
        read_only_fields = ['company']

    def create(self, validated_data):
        user = self.context['request'].user
        company = user.owned_company

        if hasattr(company, 'storage'):
            raise serializers.ValidationError('У компании уже есть склад')

        validated_data['company'] = company
        return super().create(validated_data)
