from django.shortcuts import render, redirect, get_object_or_404
from videos.models import Video, Comment, Channel
from videos.forms import SignUpForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required(login_url='login')
def home(request):
    videos = Video.objects.all()
    return render(request, 'videos/home.html', {'videos':videos})


@login_required(login_url='login')
def show_video(request, pk):
    video = get_object_or_404(Video, id=pk)
    video.views += 1
    video.save()
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


def trending_videos(request):
    videos = Video.get_tranding_videos()
    return render(request, 'videos/tranding_videos.html', {'videos':videos})


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
    request.user.channel.subscribe.add(user_subscribe)
    request.user.channel.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def unsubcriber_view(request, pk):
    user_subscribe = Channel.objects.get(id=pk)
    request.user.channel.subscribe.remove(user_subscribe)
    request.user.channel.save()
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