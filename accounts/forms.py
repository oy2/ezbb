# import user,forms
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    """
    Register user form. Allows user to submit required fields to register an account. Additionally, validates
    password and password2 fields to ensure they match.
    """
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class PrivateMessageForm(forms.Form):
    """
    Private message form. Allows user to submit required fields to send a private message.
    """
    pm_title = forms.CharField(max_length=200)
    pm_content = forms.CharField(widget=forms.Textarea)
    pm_title.label = 'Title'
    pm_content.label = 'Content'
    widgets = {'pm_content': forms.Textarea(attrs={'maxlength': 5000}),
               'pm_title': forms.TextInput(attrs={'maxlength': 200})}


class PrivateMessageReplyForm(forms.Form):
    """
    Private message reply form. Allows user to submit required fields to reply to a private message.
    """
    pmr_content = forms.CharField(widget=forms.Textarea)
    pmr_content.label = 'Reply'
    widgets = {'pmr_content': forms.Textarea(attrs={'maxlength': 5000})}
