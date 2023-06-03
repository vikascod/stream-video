from django.urls import path
from videos import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload-videos', views.upload_video, name='upload_video'),
    path('play-videos', views.play_video, name='play_video'),
]