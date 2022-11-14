# importing settings
from django.conf import settings


def aws_media(request):
    output = {
        "MEDIA_URL": settings.MEDIA_URL,
        "STAGE": settings.STAGE
    }
    return output
