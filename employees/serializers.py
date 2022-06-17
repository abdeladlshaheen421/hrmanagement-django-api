from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Attendence
User=get_user_model()


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class AttendenceSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Attendence
        fields = ['id','check_in','check_out']