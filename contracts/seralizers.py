from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import Contract
class ContractSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='created_by.username')
    email = serializers.ReadOnlyField(source='created_by.email')
    role = serializers.ReadOnlyField(source='created_by.role')
    class Meta:
        model=Contract
        fields = ['id', 'username', 'email', 'role', 'title', 'description', 
            'status', 'deadline', 'document', 'created_at', 'parties']
        read_only_fields=['created_at']
        

class UplodeFiles(serializers.ModelSerializer):
    class Meta:
        model=Contract
        fields =['document']
    
        def validate_fieldname(self,document):
            if not(FileExtensionValidator(allowed_extensions=['pdf','docx'])):
                raise serializers.ValidationError("the file not allowed ")
            return True
