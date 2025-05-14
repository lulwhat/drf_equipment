from django.db import models

from .managers import EquipmentManager, EquipmentTypeManager


class EquipmentType(models.Model):
    """
    Model representing equipment types with serial number mask patterns.
    """
    name = models.CharField(max_length=255)
    serial_number_mask = models.CharField(max_length=50)

    objects = EquipmentTypeManager()

    class Meta:
        app_label = 'equipment_app'
    
    def __str__(self):
        return self.name


class Equipment(models.Model):
    """
    Model representing equipment items with type, serial number, and notes.
    """
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE,
                                       related_name='equipment')
    serial_number = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True, max_length=255)
    # For soft delete
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EquipmentManager()

    class Meta:
        app_label = 'equipment_app'
        
    def __str__(self):
        return f"{self.equipment_type.name} - {self.serial_number}"
