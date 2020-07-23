from rest_framework import serializers
from .models import User


# serializers for creating and modifying user

class UserSer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['firstname','lastname','email','password']


# serializers for getting token and personal info

class loginSer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','password']