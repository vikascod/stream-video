from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Channel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    video = models.ForeignKey("Video", on_delete=models.CASCADE, null=True, blank=True)
    subscribe = models.ManyToManyField('self', related_name='subcripbe_by', symmetrical=False, blank=True)
    channel_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    bio = models.TextField(blank=True, null=True)
    social_link = models.CharField(max_length=300)
    updated_on = models.DateTimeField(User, auto_now=True)

    
    def total_subscribers(self):
        return self.subscribe.count()

    def __str__(self):
        return self.channel_name


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to='videos')
    likes = models.ManyToManyField(User, related_name='video_like', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    @classmethod
    def get_tranding_videos(cls):
        return cls.objects.order_by('-views')[:10]

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class VideoHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_on = models.DateTimeField(auto_now_add=True)


class SaveVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    saved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video.title