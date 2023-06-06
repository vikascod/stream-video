from django import template
from videos.models import SaveVideo

register = template.Library()

@register.filter
def is_saved(video, user):
    return SaveVideo.objects.filter(video=video, user=user).exists()
