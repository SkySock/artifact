from django.core.exceptions import ValidationError
import httplib2


def get_path_upload_profile_image(instance, file):
    return f'avatars/{instance.id}/{file}'


def get_path_upload_subscription_image(instance, file):
    return f'subscriptions/user_{instance.owner.id}/{instance.id}.{file.split(".")[-1]}'


def get_default_profile_image():
    return 'avatars/defaults/default_profile_image.png'


def validate_size_image(file_obj):
    megabyte_limit = 4
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Image size must be <= {megabyte_limit} megabytes")


def download_img(img_url):
    h = httplib2.Http('.cache')
    response, content = h.request(img_url)
    return content
