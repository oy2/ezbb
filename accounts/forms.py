# import user,forms
from django import forms
from django.contrib.auth.models import User


# Register user form
class RegisterForm(forms.ModelForm):
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


# Form for private message
class PrivateMessageForm(forms.Form):
    pm_title = forms.CharField(max_length=200)
    pm_content = forms.CharField(widget=forms.Textarea)
    widgets = {'pm_content': forms.Textarea(attrs={'maxlength': 5000}),
               'pm_title': forms.TextInput(attrs={'maxlength': 200})}


# Form for private message reply
class PrivateMessageReplyForm(forms.Form):
    pmr_content = forms.CharField(widget=forms.Textarea)
    widgets = {'pmr_content': forms.Textarea(attrs={'maxlength': 5000})}
