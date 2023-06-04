from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Channel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    video = models.ForeignKey("Video", on_delete=models.CASCADE)
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