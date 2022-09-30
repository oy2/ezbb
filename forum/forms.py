from django import forms

from .models import Post, Comment


# Form for creating posts
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_topic', 'post_title', 'post_content']
        # post_content max 5000 chars
        widgets = {'post_topic': forms.HiddenInput(), 'post_content': forms.Textarea(attrs={'maxlength': 5000})}


# Form for creating comments (on posts)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content', 'comment_post']
        # comment_content max 5000 chars, name Comment
        widgets = {'comment_post': forms.HiddenInput(), 'comment_content': forms.Textarea(attrs={'maxlength': 5000})}

