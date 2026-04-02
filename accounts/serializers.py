
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    
    def validate_email(self,email):
        print("hello")
        if User.objects.filter(email=email).exists():
            print("hello")
            raise serializers.ValidationError("the email is alreadt token")
        return email
    
    def validate_password(self, value):
        if value.isdigit():
            raise serializers.ValidationError("You have to use character with number")
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
            
        return value
    
    def create(self,data):
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=User.CLIENT  
        )
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']