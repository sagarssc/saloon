from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'password', 'username')

	def create(self, validated_data):
			validated_data["password"] = make_password(validated_data['password'])
			user = User(**validated_data)
			user.save()
			return user
