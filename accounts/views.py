from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import RegisterForm


# Register view
def register(request):
    # if post RegisterForm
    if request.method == 'POST':
        # form
        form = RegisterForm(request.POST)
        # if valid
        if form.is_valid():
            # save form
            user = form.save(commit=False)
            # set password
            user.set_password(form.cleaned_data['password'])
            # save form
            user.save()
            # redirect to login
            messages.add_message(request, messages.SUCCESS, 'Account created successfully')
            return redirect('login')
    # else
    else:
        form = RegisterForm()
    # pass form
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required
def view_user(request, user_id):
    # get user if exists
    user = get_object_or_404(User, pk=user_id)
    # get Posts excluding hidden
    posts = user.post_set.exclude(post_visible=False)
    # get Comments excluding hidden
    comments = user.comment_set.exclude(comment_visible=False)
    details = False
    # if user is viewing their own profile
    if request.user == user:
        details = True
    # pass posts and comments
    context = {'user': user, 'posts': posts, 'comments': comments,
               'details': details}
    return render(request, 'accounts/profile.html', context)


@login_required
def profile(request):
    # Get all posts by user
    posts = request.user.post_set.exclude(post_visible=False)
    # Get all comments by user
    comments = request.user.comment_set.exclude(comment_visible=False)
    context = {'user': request.user, 'posts': posts, 'comments': comments, 'details': True}
    return render(request, 'accounts/profile.html', context)

