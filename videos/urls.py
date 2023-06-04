from django.urls import path
from videos import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload-videos', views.upload_video, name='upload_video'),
    path('like-videos/<int:pk>', views.video_like_view, name='like_video'),
    path('video/<int:pk>', views.show_video, name='show_video'),
    path('delete-comment/<int:pk>', views.comment_delete_view, name='delete_comment'),
    path('edit-comment/<int:pk>', views.comment_update_view, name='edit_comment'),
    path('subcribe/<int:pk>', views.subcriber_view, name='subscribe'),
    path('unsubcribe/<int:pk>', views.unsubcriber_view, name='unsubscribe'),
    path('signup', views.signup_view, name='signup'),
    path('signin', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]