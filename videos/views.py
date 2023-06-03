from django.shortcuts import render, redirect
from videos.models import Video

# Create your views here.

def home(request):
    return render(request, 'videos/home.html')

def upload_video(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        Video.objects.create(title=title, description=description, video_file=video_file)
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'videos/upload_video.html')


def play_video(request):
    videos = Video.objects.all()
    return render(request, 'videos/play_videos.html', {'videos':videos})