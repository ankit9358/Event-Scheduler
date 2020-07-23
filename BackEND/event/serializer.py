from rest_framework import serializers
from .models import Schedule
from webapp.models import User

class Sche_ser(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['title','event','date']

class UserSer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['firstname','lastname']

class Sche_ser2(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['title','event','date','slug']