from .models import SocialInformation
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class SocialInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialInformation
        fields = [
            'id',
            'owner',
            'state',
            'city',
            'income',
            'education',
            'job',
            'birth_date',
        ]


class UserSerializer(serializers.ModelSerializer):
    social_information = SocialInformationSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'social_information',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def create(self, validated_data):
        voxpopuser = User(**validated_data)
        password = validated_data['password']
        voxpopuser.set_password(password)
        voxpopuser.save()
        token = Token.objects.create(user=voxpopuser)
        token.save()
        return voxpopuser
