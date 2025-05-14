import re

from django.utils.html import escape
from rest_framework.exceptions import ValidationError


def _get_serial_numbers_errors(
        serial_number, serial_number_mask
) -> list:
    """
    Validates a serial number against equipment type's mask.

    :param str serial_number:
    :param str serial_number_mask:

    Returns:
        list: list of errors
    """
    sn_len = len(serial_number)
    mask_len = len(serial_number_mask)
    if sn_len != mask_len:
        return [
            f"Serial number must be {mask_len} "
            f"characters long, current length: {sn_len}"
        ]

    errors = []
    char_patterns = {
        'N': r'^[0-9]$',
        'A': r'^[A-Z]$',
        'a': r'^[a-z]$',
        'X': r'^[A-Z0-9]$',
        'Z': r'^[-_@]$'
    }
    error_messages = {
        'N': "must be a digit (0-9)",
        'A': "must be an uppercase letter",
        'a': "must be a lowercase letter",
        'X': "must be an uppercase letter or digit",
        'Z': "must be one of: -, _, @"
    }
    for i, (char, mask_char) in enumerate(
            zip(serial_number, serial_number_mask)
    ):
        pattern = char_patterns.get(mask_char)
        if not pattern:
            raise ValidationError(
                f"Unknown mask character '{mask_char}' at position {i + 1}"
            )

        if not re.match(pattern, char):
            errors.append(
                f"Character at position {i + 1} "
                f"{error_messages[mask_char]}"
            )

    return errors


def _validate_and_prepare_bulk_equipment(
        equipment_type, serial_numbers, notes=""
):
    """Iterates over serial_numbers and returns list of Equipment

    Raises:
        rest_framework.exceptions.ValidationError
    """
    from equipment_app.models import Equipment  # fix circular import

    objects_for_creation = []
    errors = []

    # check no duplicates in the request
    if len(serial_numbers) != len(set(serial_numbers)):
        duplicates = {x for x in serial_numbers if serial_numbers.count(x) > 1}
        raise ValidationError(
            detail={
                "serial_numbers_errors": [{
                    "index": i,
                    "serial_number": sn,
                    "error": ["Duplicate serial number in request"]
                } for i, sn in enumerate(duplicates)]
            }
        )

    for i, serial_number in enumerate(serial_numbers):
        try:
            if Equipment.objects.active().filter(
                equipment_type=equipment_type,
                serial_number__iexact=serial_number
            ).exists():
                raise ValidationError(
                    "This serial number already exists for this equipment type"
                )

            current_sn_errors = _get_serial_numbers_errors(
                serial_number, equipment_type.serial_number_mask
            )
            if current_sn_errors:
                raise ValidationError(current_sn_errors)

            objects_for_creation.append(
                Equipment(
                    equipment_type=equipment_type,
                    serial_number=serial_number,
                    notes=notes
                )
            )

        except ValidationError as e:
            errors.append({
                "index": i,
                "serial_number": serial_number,
                "error": e.detail
            })

    if errors:
        raise ValidationError(
            detail={"serial_numbers_errors": errors}
        )

    return objects_for_creation


def create_equipment(equipment_type_id, serial_numbers, notes=""):
    """Creates multiple instances of equipment. Includes validation

    :param str equipment_type_id:
    :param list serial_numbers:
    :param str notes:

    Returns:
        list: list of Equipment

    Raises:
        rest_framework.exceptions.ValidationError with error dict
        "serial_numbers_errors": dict of errors for every serial_number
    """
    # fix circular imports
    from equipment_app.models import Equipment, EquipmentType

    # XSS injection protection
    notes = escape(notes)

    if not equipment_type_id or not serial_numbers:
        raise ValidationError(
            detail={
                "serial_numbers_errors": [{
                    "index": 0,
                    "serial_number": "",
                    "error": "Equipment type and serial numbers are required"
                }]
            }
        )

    try:
        equipment_type = EquipmentType.objects.get(
            pk=equipment_type_id
        )
    except EquipmentType.DoesNotExist:
        raise ValidationError(
            detail={
                "serial_numbers_errors": [{
                    "index": 0,
                    "serial_number": "",
                    "error": "Equipment type not found"
                }],
            }
        )
    except ValueError:
        raise ValidationError(
            detail={
                "serial_numbers_errors": [{
                    "index": 0,
                    "serial_number": "",
                    "error": "Invalid value for equipment_type, "
                             "must be correct id(int)"
                }],
            }
        )

    equipments = _validate_and_prepare_bulk_equipment(
        equipment_type, serial_numbers, notes
    )
    Equipment.objects.bulk_create(equipments)
    return equipments


def soft_delete_equipment(equipment):
    equipment.is_deleted = True
    equipment.save()
