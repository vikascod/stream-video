from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Channel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    video = models.ForeignKey("Video", on_delete=models.CASCADE, null=True, blank=True)
    channel_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    bio = models.TextField(blank=True, null=True)
    social_link = models.CharField(max_length=300)
    updated_on = models.DateTimeField(User, auto_now=True)
    subscribers = models.ManyToManyField(User, through='Subscription', related_name='subscribed_channels')


    
    def total_subscribers(self):
        return self.subscribers.count()

    def __str__(self):
        return self.channel_name

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name='subscribers', on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, related_name='subscription', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.subscriber.username} subscribed to {self.channel.channel_name}"


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

