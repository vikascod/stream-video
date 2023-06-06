from django.contrib import admin
from videos.models import Video, Comment, Channel, VideoHistory, SaveVideo


admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Channel)
admin.site.register(VideoHistory)
admin.site.register(SaveVideo)