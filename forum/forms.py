from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    Form for creating a new post in a topic. This form is used in the new_post view. Binds to the Post
    model. The post_content field is a Textarea widget with a max length of 5000 characters.
    """
    class Meta:
        model = Post
        fields = ['post_topic', 'post_title', 'post_content']
        labels = {'post_title': 'Title', 'post_content': 'Content'}
        # post_content max 5000 chars
        widgets = {'post_topic': forms.HiddenInput(), 'post_content': forms.Textarea(attrs={'maxlength': 5000})}


# Form for creating comments (on posts)
class CommentForm(forms.ModelForm):
    """
    Form for creating a new comment on a post.
    """
    class Meta:
        model = Comment
        fields = ['comment_content', 'comment_post']
        labels = {'comment_content': 'Comment'}
        # comment_content max 5000 chars, name Comment
        widgets = {'comment_post': forms.HiddenInput(), 'comment_content': forms.Textarea(attrs={'maxlength': 5000})}

