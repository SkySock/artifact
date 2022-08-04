from django.core.exceptions import ValidationError


def validate_size_file(file_obj):
    megabyte_limit = 32
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"File size must be <= {megabyte_limit} megabytes")
