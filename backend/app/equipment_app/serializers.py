from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    
    def validate(self, data):
        """
        Validate the equipment data.
        """
        equipment_type = data.get('equipment_type')
        serial_number = data.get('serial_number')
        
        if equipment_type and serial_number:
            try:
                equipment_type.validate_serial_number(serial_number)
            except ValidationError as e:
                raise serializers.ValidationError({'serial_number': e.message})
            
            # Check for uniqueness
            if Equipment.objects.filter(
                equipment_type=equipment_type,
                serial_number=serial_number,
                is_deleted=False
            ).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise serializers.ValidationError({
                    'serial_number':
                    'This serial number already exists for this equipment type'
                })
        
        return data


class BulkEquipmentCreateSerializer(serializers.Serializer):
    """
    Serializer for bulk creation of equipment.
    """
    equipment_type = serializers.PrimaryKeyRelatedField(
        queryset=EquipmentType.objects.all()
    )
    serial_numbers = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """
        Validate all serial numbers against the equipment type mask.
        """
        equipment_type = data.get('equipment_type')
        serial_numbers = data.get('serial_numbers')
        errors = []
        
        for i, serial_number in enumerate(serial_numbers):
            try:
                equipment_type.validate_serial_number(serial_number)
                
                # Check for uniqueness
                if Equipment.objects.filter(
                    equipment_type=equipment_type,
                    serial_number=serial_number,
                    is_deleted=False
                ).exists():
                    errors.append({
                        'index': i,
                        'serial_number': serial_number,
                        'error': 'This serial number already exists '
                                 'for this equipment type'
                    })
            except ValidationError as e:
                errors.append({
                    'index': i,
                    'serial_number': serial_number,
                    'error': str(e)
                })
        
        if errors:
            raise serializers.ValidationError({
                'serial_numbers_errors': errors
            })
        
        return data
    
    def create(self, validated_data):
        """
        Create multiple equipment instances.
        """
        equipment_type = validated_data.get('equipment_type')
        serial_numbers = validated_data.get('serial_numbers')
        notes = validated_data.get('notes', '')
        
        created_equipment = []
        for serial_number in serial_numbers:
            equipment = Equipment.objects.create(
                equipment_type=equipment_type,
                serial_number=serial_number,
                notes=notes
            )
            created_equipment.append(equipment)
        
        return created_equipment
