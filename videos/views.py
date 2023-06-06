from django.shortcuts import render, redirect, get_object_or_404
from videos.models import Video, Comment, Channel, VideoHistory, SaveVideo
from videos.forms import SignUpForm, CommentForm, ChannelForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages


@login_required(login_url='login')
def home(request):
    videos = Video.objects.all()
    return render(request, 'videos/home.html', {'videos':videos})


@login_required(login_url='login')
def create_channel(request):
    if request.method == "POST":
        form = ChannelForm(request.POST, request.FILES)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.user = request.user
            channel.save()
            messages.success(request, "Channel Created!")
            return redirect('home')
    form = ChannelForm()
    return render(request, 'videos/channel.html', {'form':form})


@login_required(login_url='login')
def show_video(request, pk):
    video = get_object_or_404(Video, id=pk)
    if not video:
        return HttpResponse("Video does not exists!")
    video.views += 1
    video.save()

    video_history = VideoHistory.objects.filter(user=request.user).order_by('-watched_on')
    recent_video = video_history.first()
    if recent_video is None or recent_video.video.id != video.id:
        VideoHistory.objects.create(user=request.user, video=video)

    user = User.objects.get(id=request.user.id)
    if video:
        form = CommentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = user
                comment.video = video
                comment.save()
                return redirect(request.META.get('HTTP_REFERER'))
        comments = Comment.objects.filter(video=video).order_by('-created_on')
        return render(request, 'videos/video.html', {'video':video, 'form':form, 'comments':comments})
    else:
        return HttpResponse("Video does not exists!")


@login_required(login_url='login')
def save_video_view(request, pk):
    video = get_object_or_404(Video, id=pk)
    if not video:
        return HttpResponse("Video does not exist!")

    save_video, created = SaveVideo.objects.get_or_create(user=request.user, video=video)

    if created:
        messages.success(request, "Video Saved!")
        save_video.save()
    else:
        messages.warning(request, "Video Unsaved!")
        save_video.delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def library(request):
    videos = SaveVideo.objects.filter(user=request.user).order_by('-saved_on')
    return render(request, 'videos/library.html', {'videos':videos})


@login_required(login_url='login')
def trending_videos(request):
    videos = Video.get_tranding_videos()
    return render(request, 'videos/tranding_videos.html', {'videos':videos})


@login_required(login_url='login')
def video_history(request):
    videos = VideoHistory.objects.filter(user=request.user).order_by('-watched_on')
    return render(request, 'videos/video_history.html', {'videos':videos})


@login_required(login_url='login')
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("Comment not found")


@login_required(login_url='login')
def comment_update_view(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment:
        form = CommentForm(request.POST or None, instance=comment)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('show_video', pk=pk)
        return render(request, 'videos/comment_edit.html', {'form':form, 'comment':comment})
    else:
        return HttpResponse("Comment not found")


@login_required(login_url='login')
def subcriber_view(request, pk):
    user_subscribe = Channel.objects.get(user_id=pk)
    user_channel = request.user.channel

    if user_subscribe in user_channel.subscribe.all():
        user_channel.subscribe.remove(user_subscribe)
        messages.warning(request, "Unsubscribed!")
    else:
        user_channel.subscribe.add(user_subscribe)
        messages.warning(request, "Subscribed!")
    
    user_channel.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def video_like_view(request, pk):
    video = get_object_or_404(Video, id=pk)
    liked = video.likes.filter(id=request.user.id)
    if liked:
        video.likes.remove(request.user)
    else:
        video.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def upload_video_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        Video.objects.create(title=title, description=description, video_file=video_file, user=request.user)
        messages.success(request, "Video Uploaded!")
        return redirect('home')
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