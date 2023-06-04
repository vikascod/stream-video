from django.shortcuts import render, redirect
from videos.models import Video
from videos.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    videos = Video.objects.all()
    return render(request, 'videos/home.html', {'videos':videos})

@login_required(login_url='login')
def upload_video(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        Video.objects.create(title=title, description=description, video_file=video_file)
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'videos/upload_video.html')


def signup_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'videos/signup.html', {'form':form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'videos/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')