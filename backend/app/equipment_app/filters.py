import django_filters
from django.db.models import Q

from .models import Equipment, EquipmentType


class EquipmentTypeFilter(django_filters.FilterSet):
    class Meta:
        model = EquipmentType
        fields = {
            'name': ['icontains'],
            'serial_number_mask': ['exact'],
        }


class EquipmentFilter(django_filters.FilterSet):
    created_at_gte = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Created after (inclusive)',
        help_text='(e.g. 2023-01-15 or 2023-01-15T14:30:00)'
    )
    created_at_lte = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Created before (inclusive)',
        help_text='(e.g. 2023-01-15 or 2023-01-15T14:30:00)'
    )
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search (includes serial_number, notes, equipment_type results)'
    )

    def filter_search(self, queryset, name, value):
        q_serial = Q(serial_number__contains=value)
        q_notes = Q(notes__icontains=value)
        q_type = Q(equipment_type__name__icontains=value)
        return queryset.filter(q_serial | q_notes | q_type)

    class Meta:
        model = Equipment
        fields = {
            'equipment_type__name': ['icontains'],
            'serial_number': ['exact', 'contains'],
            'notes': ['icontains']
        }
