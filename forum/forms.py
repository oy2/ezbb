from django import forms

from .models import Topic, Post, Comment


# Form for creating posts
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_topic', 'post_title', 'post_content']

