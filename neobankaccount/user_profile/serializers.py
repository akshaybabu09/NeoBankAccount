from django.contrib.auth import authenticate
from rest_framework import serializers

from user_profile.models import UserProfile
from user_profile.services import user_authentication


class UserRegistrationSerializer(serializers.ModelSerializer):

    mobile = serializers.IntegerField(
        min_value=5000000000,
        max_value=9999999999,
        required=True
    )
    aadhaar_number = serializers.IntegerField(
        min_value=000000000000,
        max_value=999999999999,
        required=True)
    pan_detail = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(required=True)
    account_number = serializers.IntegerField()
    ifsc_code = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = (
            'mobile',
            'password',
            'aadhaar_number',
            'pan_detail',
            'account_number',
            'ifsc_code',
        )

    def create(self, validated_data):
        user = UserProfile.objects.create(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    mobile = serializers.IntegerField(
        min_value=5000000000,
        max_value=9999999999,
        required=True
    )
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = user_authentication(**data)

        if user is None:
            raise serializers.ValidationError("Either username or password is incorrect.")
        return user

    class Meta:
        model = UserProfile
        fields = (
            'mobile',
            'password',
        )
