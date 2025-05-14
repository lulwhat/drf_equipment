from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Equipment, EquipmentType


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value


class EquipmentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for EquipmentType model.
    """
    equipment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = EquipmentType
        fields = ['id', 'name', 'serial_number_mask', 'equipment_count']


class EquipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Equipment model.
    """
    equipment_type_name = serializers.ReadOnlyField(
        source='equipment_type.name'
    )
    
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_type', 'equipment_type_name',
                  'serial_number', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
