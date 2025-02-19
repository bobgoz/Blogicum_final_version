from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'text',
            'location',
            'category',
            'pub_date',
            )
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'text',
            ]
