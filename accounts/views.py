from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import RegisterForm, PrivateMessageForm
from accounts.models import PrivateMessage


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


@login_required
def send_pm(request, user_id):
    # forms/PrivateMessageForm
    if request.method == 'POST':
        # check form
        form = PrivateMessageForm(request.POST)
        # if valid
        if form.is_valid():
            # get recipient
            recipient = get_object_or_404(User, pk=user_id)
            # create message
            message = PrivateMessage(pm_sender=request.user, pm_receiver=recipient,
                                     pm_content=form.cleaned_data['pm_content'], pm_title=form.cleaned_data['pm_title'])
            # save message
            message.save()
            # redirect to profile
            messages.add_message(request, messages.SUCCESS, 'Message sent successfully')
            return redirect('profile')
    # else
    else:
        form = PrivateMessageForm()

    # validate user_id
    user = get_object_or_404(User, pk=user_id)
    # check if user is request.user
    if user == request.user:
        # redirect to profile
        messages.add_message(request, messages.ERROR, 'You can\'t send a message to yourself')
        return redirect('profile')
    # pass form
    context = {'form': form, 'user': user}
    return render(request, 'accounts/private_message.html', context)


def view_messages(request):
    # get all messages sent to user, order by pm_read_receiver, updated_at
    user_messages = PrivateMessage.objects.filter(pm_receiver=request.user).order_by('pm_read_receiver', 'updated_at')
    # pass messages
    context = {'user_messages': user_messages}
    return render(request, 'accounts/messages.html', context)


def view_message(request, message_id):
    # get message
    message = get_object_or_404(PrivateMessage, pk=message_id)
    # check if message is for user or was sent by user
    if message.pm_receiver != request.user and message.pm_sender != request.user:
        # redirect to messages
        messages.add_message(request, messages.ERROR, 'You can\'t view this message')
        return redirect('view_messages')
    # if receiver
    if message.pm_receiver == request.user:
        if not message.pm_read_receiver:
            message.pm_read_receiver = True
            message.save()
    # if sender
    if message.pm_sender == request.user:
        if not message.pm_read_sender:
            message.pm_read_sender = True
            message.save()
    replies = message.get_replies()
    # pass message
    context = {'message': message, 'replies': replies}
    return render(request, 'accounts/message.html', context)
