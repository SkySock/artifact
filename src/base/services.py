from django.core.exceptions import ValidationError


def get_path_upload_profile_image(instance, file):
    return f'profile_images/{instance.id}/{file}'


def validate_size_image(file_obj):
    megabyte_limit = 4
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Image size must be <= {megabyte_limit} megabytes")
