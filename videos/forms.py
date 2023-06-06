from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from videos.models import Comment, Channel, Video


class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ChannelForm(forms.ModelForm):
    channel_name = forms.CharField(label="Channel Name", widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.CharField(label="Channel Logo", widget=forms.FileInput(attrs={'class':'form-control'}))
    bio = forms.CharField(label="About Channel", widget=forms.TextInput(attrs={'class':'form-control'}))
    social_link = forms.CharField(label="Social Link", widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Channel
        fields = ['channel_name', 'image', 'bio', 'social_link']
        exclude = ('user', 'video', 'subscribe')
        # widgets = {
        #     'channel_name':forms.TextInput(attrs={'class':'form-control'})
        # }


class CommentForm(forms.ModelForm):
    body = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Comment
        fields = ['body']
        exclude = ('user', 'video')