from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'municipality', 'locality', 'password')
        extra_kwargs = {'password': {'write_only': True},}
    
    def validate_email(self, value):
        user = self.instance # Solo tiene valor cuando se está actualizando
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError("Email already in used.")
        return value
    
    def validate_username(self, value):
        user = self.instance
        if CustomUser.objects.filter(username=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError("Username already in used.")
        return value
    
    def validate_password(self, value):
        if len(value) < 8 or not any(char.isdigit() for char in value) or not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
        
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
