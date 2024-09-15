from rest_framework import serializers
from.models import Blog,CustomUser
from django.contrib.auth import get_user_model, authenticate
import re

from .models import CustomUser

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'first_name', 'last_name', 'role' ,'is_active', 'is_staff'
        )

    def validate_email(self, value):
        
        # Check that the email is unique.
       
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self,value):
        pattern = r"^(?=.*[\W_])"
        if not re.match(pattern, value) and len(value)<=8:
            print(value)
            raise serializers.ValidationError("Password must contain at least conatain 8 digits.")
        
        

    def validate_phone_number(self, value):
       
        # Validate phone number format (optional).
       
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value

    def create(self, validated_data):
        # Create a new CustomUser instance.
       
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
      
        # Update an existing CustomUser instance.
       
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role',instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance
    


User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'role']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role = validated_data['role']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        return data

