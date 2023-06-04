from django.urls import path
from videos import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload-videos', views.upload_video, name='upload_video'),
    path('signup', views.signup_view, name='signup'),
    path('signin', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]