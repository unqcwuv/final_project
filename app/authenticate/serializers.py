from rest_framework import serializers
from .models import User, Company

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'inn', 'title', 'owner', 'address', 'phone', 'email']
        read_only_fields = ['owner']

    def create(self, validated_data):
        user = self.context['request'].user

        if hasattr(user, 'owned_company'):
            raise serializers.ValidationError('У вас уже есть компания')

        company = Company.objects.create(owner=user, **validated_data)
        user.is_company_owner = True
        user.company = company
        user.save(update_fields=['is_company_owner', 'company'])
        return company


class AddEmployeeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь с таким email не найден')

        if user.is_company_owner:
            raise serializers.ValidationError('Пользователь является владельцем компании и не может стать сотрудником')

        if user.company_id is not None:
            raise serializers.ValidationError('Пользователь уже привязан к другой компании')

        self.employee = user
        return value

    def save(self, **kwargs):
        company = kwargs['company']
        self.employee.company = company
        self.employee.save(update_fields=['company'])
        return self.employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


