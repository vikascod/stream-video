from django.contrib import admin
from videos.models import Video, Comment, Channel


admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Channel)