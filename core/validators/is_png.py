from django.core.exceptions import ValidationError
from core.images.core_utils import get_image_format


def validate_is_png(image):
    format = get_image_format(image)
    if str(format).upper() != "PNG":
        raise ValidationError("A imagem precisa ser uma imagem PNG")
