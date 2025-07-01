from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)
    firstname = serializers.CharField(write_only=True)
    lastname = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'password', 'password2', 'user_type', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        firstname = validated_data.pop('firstname')
        lastname = validated_data.pop('lastname')
        phone = validated_data.pop('phone')
        user_type = validated_data.pop('user_type')
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=firstname,
            last_name=lastname
        )

        UserProfile.objects.create(user=user, user_type=user_type, phone=phone)
        return user
