from django.db import models
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404


class EquipmentManager(models.Manager):
    def get_queryset(self):
        """Queryset with related equipment types"""
        return super().get_queryset().select_related('equipment_type')

    def active(self):
        return self.get_queryset().filter(is_deleted=False)

    def get_active_or_404(self, **kwargs):
        return get_object_or_404(self.active(), **kwargs)


class EquipmentTypeManager(models.Manager):
    def with_equipment_count(self):
        return super().get_queryset().annotate(
            equipment_count=Count(
                'equipment',
                filter=Q(equipment__is_deleted=False)
            )
        )
