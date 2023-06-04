from django.contrib import admin
from videos.models import Video, Comment


admin.site.register(Video)
admin.site.register(Comment)