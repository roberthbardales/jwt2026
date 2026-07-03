from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['occupation'] = user.occupation
        token['gender'] = user.gender
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'occupation', 'gender', 'date_birth', 'phone', 'is_active', 'is_staff']
        read_only_fields = ['id', 'is_active', 'is_staff']


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    occupation = serializers.ChoiceField(choices=User.OCCUPATION_CHOICES, required=False)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    date_birth = serializers.DateField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este correo ya está registrado.')
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
