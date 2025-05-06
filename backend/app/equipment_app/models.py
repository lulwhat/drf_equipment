import re

from django.db import models
from django.core.exceptions import ValidationError


class EquipmentType(models.Model):
    """
    Model representing equipment types with serial number mask patterns.
    """
    name = models.CharField(max_length=255)
    serial_number_mask = models.CharField(max_length=255)
    
    class Meta:
        app_label = 'equipment_app'
    
    def __str__(self):
        return self.name

    def validate_serial_number(self, serial_number):
        """
        Validates a serial number against this equipment type's mask.

        :param str serial_number:

        Returns:
            bool: True if valid, False otherwise

        Raises:
            ValidationError: If the serial number doesn't match the mask
        """
        if len(serial_number) != len(self.serial_number_mask):
            raise ValidationError(
                f"Serial number must be {len(self.serial_number_mask)} "
                f"characters long, current length: {len(serial_number)}"
            )

        errors = []
        char_patterns = {
            'N': r'^[0-9]$',
            'A': r'^[A-Z]$',
            'a': r'^[a-z]$',
            'X': r'^[A-Z0-9]$',
            'Z': r'^[-_@]$'
        }
        for i, (char, mask_char) in enumerate(
                zip(serial_number, self.serial_number_mask)
        ):
            pattern = char_patterns.get(mask_char)

            if not re.match(pattern, char):
                error_messages = {
                    'N': "must be a digit (0-9)",
                    'A': "must be an uppercase letter",
                    'a': "must be a lowercase letter",
                    'X': "must be an uppercase letter or digit",
                    'Z': "must be one of: -, _, @"
                }
                errors.append(
                    f"Character at position {i+1} "
                    f"{error_messages[mask_char]}"
                )
        if errors:
            raise ValidationError(errors)

        return True


class Equipment(models.Model):
    """
    Model representing equipment items with type, serial number, and notes.
    """
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE,
                                       related_name='equipment')
    serial_number = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)  # For soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'equipment_app'
        unique_together = ('equipment_type', 'serial_number')
        
    def __str__(self):
        return f"{self.equipment_type.name} - {self.serial_number}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to validate serial number before saving.
        """
        if not self.is_deleted:  # Only validate if not being soft-deleted
            self.equipment_type.validate_serial_number(self.serial_number)
            
            # Check for uniqueness
            if Equipment.objects.filter(
                equipment_type=self.equipment_type,
                serial_number=self.serial_number,
                is_deleted=False
            ).exclude(pk=self.pk).exists():
                raise ValidationError(
                    f"Serial number {self.serial_number} "
                    f"already exists for this equipment type"
                )
                
        super().save(*args, **kwargs)
