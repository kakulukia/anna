# importing settings
from django.conf import settings
from application.models import ZoomLink


def aws_media(request):
    output = {
        'MEDIA_URL': settings.MEDIA_URL,
        'ZOOM_LINK': None
    }
    if request.user.is_authenticated:
        zoom_link = ZoomLink.objects.filter(user=request.user).first()
        output['ZOOM_LINK'] = zoom_link
    return output
