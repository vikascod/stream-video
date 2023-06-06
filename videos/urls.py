from django.urls import path
from videos import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload-videos', views.upload_video_view, name='upload_video'),
    path('like-videos/<int:pk>', views.video_like_view, name='like_video'),
    path('video/<int:pk>', views.show_video, name='show_video'),
    path('delete-comment/<int:pk>', views.comment_delete_view, name='delete_comment'),
    path('edit-comment/<int:pk>', views.comment_update_view, name='edit_comment'),
    path('subcribe/<int:pk>', views.subcriber_view, name='subscribe'),
    path('save/<int:pk>', views.save_video_view, name='save_video'),
    path('tranding', views.trending_videos, name='tranding'),
    path('create-channel', views.create_channel, name='create_channel'),
    path('library', views.library, name='library'),
    path('history', views.video_history, name='history'),
    path('signup', views.signup_view, name='signup'),
    path('signin', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]