from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import RegisterForm, PrivateMessageForm, PrivateMessageReplyForm
from accounts.models import PrivateMessage, PrivateMessageReplies
from forum.models import Settings


def register(request):
    """
    Register user view. Allows user to submit required fields to register an account. Additionally, validates
    password and password2 fields to ensure they match. If successful, redirects user to login page. If sign up is
    disabled, the user will be redirected away.

    Args:
        request: HTTP request object.

    Returns:
        If request method is GET, returns register.html template. If request method is POST, returns login.html if
        successful. If errors, redirects with errors.

    """
    settings = Settings.load()
    # check settings.accounts_signup_enabled
    if not settings.accounts_signup_enabled:
        messages.add_message(request, messages.ERROR, 'Sign up is disabled')
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # set password
            user.set_password(form.cleaned_data['password'])
            user.save()

            # redirect to login
            messages.add_message(request, messages.SUCCESS, 'Account created successfully')
            return redirect('login')
    else:
        form = RegisterForm()
    # pass form
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required
def view_user(request, user_id):
    """
    View user view. Allows user to view another user's profile.

    Args:
        request: The request object.
        user_id: The target user's id.

    Returns:
        Returns profile template with user information. If a user is not found, returns 404.

    """
    # get user if exists
    user = get_object_or_404(User, pk=user_id)

    # get posts and comments excluding hidden
    posts = user.post_set.exclude(post_visible=False)
    comments = user.comment_set.exclude(comment_visible=False)
    details = False

    # if user is viewing their own profile show details0
    if request.user == user:
        details = True

    # pass user, posts, comments, and account detail boolean
    context = {'user': user, 'posts': posts, 'comments': comments,
               'details': details}
    return render(request, 'accounts/profile.html', context)


@login_required
def profile(request):
    """
    Profile view. Allows user to view their own profile. Contains additional details as opposed to view_user.

    Args:
        request: The request object.

    Returns:
        Returns profile template with user information.

    """
    # Get all posts and comments by user
    posts = request.user.post_set.exclude(post_visible=False)
    comments = request.user.comment_set.exclude(comment_visible=False)

    # pass user, posts, comments, and account detail boolean
    context = {'user': request.user, 'posts': posts, 'comments': comments, 'details': True}
    return render(request, 'accounts/profile.html', context)


@login_required
def send_pm(request, user_id):
    """
    Send private message view. Allows user to send a private message to another user. If it is received as a post from
    forms/PrivateMessageForm, a private message will be created and the user will be redirected to their inbox after
    validation.

    Args:
        request: The request object.
        user_id: The target user's id (that the user is attempting to message).

    Returns:
        If GET, returns send_pm template with form. If a user is not found, returns 404. If a user attempts to message
        themselves, redirects with error. If post, returns inbox if successful. If errors, redirects with errors.

    """
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            recipient = get_object_or_404(User, pk=user_id)
            #  create a message from the form
            message = PrivateMessage(pm_sender=request.user, pm_receiver=recipient,
                                     pm_content=form.cleaned_data['pm_content'], pm_title=form.cleaned_data['pm_title'])
            message.save()

            # redirect to profile
            messages.add_message(request, messages.SUCCESS, 'Message sent successfully')
            return redirect('view_pms')
    else:
        form = PrivateMessageForm()

    # validate user_id
    user = get_object_or_404(User, pk=user_id)

    # ensure user is not trying to message themselves
    if user == request.user:
        # redirect to profile
        messages.add_message(request, messages.ERROR, 'You can\'t send a message to yourself')
        return redirect('profile')

    # pass form
    context = {'form': form, 'user': user}
    return render(request, 'accounts/private_message.html', context)


@login_required
def view_messages(request):
    """
    View private messages view. Allows user to view their inbox. Contains all messages sent to the user, and all messages
    sent by the user.

    Args:
        request: The request object.

    Returns:
        Returns the accounts/messages.html template with user messages

    """

    # get all messages sent to user, order by pm_read_receiver, updated_at
    user_messages = PrivateMessage.objects.filter(pm_receiver=request.user).order_by('pm_read_receiver', 'updated_at')
    # get all messages sent by user, order by pm_read_sender, updated_at
    sent_messages = PrivateMessage.objects.filter(pm_sender=request.user).order_by('pm_read_sender', 'updated_at')

    # merge messages
    messages_list = list(user_messages) + list(sent_messages)
    # sort messages
    messages_list.sort(key=lambda x: x.updated_at, reverse=True)

    # pass messages
    context = {'user_messages': messages_list}
    return render(request, 'accounts/messages.html', context)


@login_required
def view_message(request, message_id):
    """
    View private message view. Allows user to view a private message. If the message is unread, it will be marked as read.
    Additionally, if received as POST by PrivateMessageReplyForm, a reply will be created and the user will be redirected
    to their inbox after validation.

    Args:
        request: The request object.
        message_id: The target message's id.

    Returns:
        If GET, Returns the accounts/message.html template with the message and replies. If a message is not found, returns 404.
        If POST, returns message if successful. If errors, redirects with errors.
    """
    message = get_object_or_404(PrivateMessage, pk=message_id)
    # check if message is for user or was sent by user (if not, redirect to inbox)
    if message.pm_receiver != request.user and message.pm_sender != request.user:
        messages.add_message(request, messages.ERROR, 'You can\'t view this message')
        return redirect('view_messages')

    # forms/PrivateMessageReplyForm
    if request.method == 'POST':
        form = PrivateMessageReplyForm(request.POST)
        if form.is_valid():
            # Create reply PrivateMessageReplies from form and request data
            reply = PrivateMessageReplies(pmr_pm=message, pmr_sender=request.user,
                                          pmr_content=form.cleaned_data['pmr_content'])
            # save reply
            reply.save()

            # make message unread for other user, update updated_at
            if message.pm_receiver == request.user:
                message.pm_read_sender = False
            else:
                message.pm_read_receiver = False
            message.save()

            messages.add_message(request, messages.SUCCESS, 'Reply sent successfully')
            return redirect('view_pm', message_id=message_id)

    # Mark as Read
    if message.pm_receiver == request.user:
        if not message.pm_read_receiver:
            message.pm_read_receiver = True
            message.save()
    if message.pm_sender == request.user:
        if not message.pm_read_sender:
            message.pm_read_sender = True
            message.save()

    replies = message.get_replies()
    form = PrivateMessageReplyForm()

    # pass message, replies, and form
    context = {'message': message, 'replies': replies, 'form': form}
    return render(request, 'accounts/message.html', context)
