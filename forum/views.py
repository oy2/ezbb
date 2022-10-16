from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone

from forum.forms import PostForm, CommentForm
from forum.models import Topic, Post, Settings


def index(request):
    """
    View function for home page of site. This is the main page of the forum. It displays all topics and their most
    recent post.

    Args:
        request: The request object.

    Returns:
        Always returns a rendered template of the index page (forum/index.html) with the topics that the user
        has access to.

    """
    topics = Topic.objects.all()
    # Remove from topics if topic is restricted to superusers and user is not superuser
    if not request.user.is_superuser:
        topics = topics.filter(restricted_superuser=False)
    # Remove from topics if topic is restricted to logged in users and user is not logged in
    if not request.user.is_authenticated:
        topics = topics.filter(restricted_logged_in=False)

    # pass topics to template
    context = {'topics': topics}
    return render(request, 'forum/index.html', context)


def topic(request, topic_id):
    """
    View function for viewing a topic. This is the page that displays all posts in a topic that are visible to the
    user. If the user is authenticated, they can also create a new post. Depending on the topic settings, a user may
    not be able to view the topic and will be redirected. Posts are displayed in paginated form, with sticky posts
    on top.

    Args:
        request: The request object.
        topic_id: The id of the topic to be viewed, used to get the topic from the database.

    Returns:
        Redirects user if topic does not exist or a permission error occurs. Otherwise, returns a rendered template
        of the topic page (forum/topic.html) with the topic and posts that the user has access to.

    """

    topic_requested = Topic.objects.filter(id=topic_id).first()

    if topic_requested:
        # check if restricted superuser
        if topic_requested.restricted_superuser and not request.user.is_superuser:
            return redirect('index')
        # check if restricted logged in
        if topic_requested.restricted_logged_in and not request.user.is_authenticated:
            return redirect('index')

        # get posts in order so most recent is first
        posts = topic_requested.post_set.order_by('-updated_at')

        # ensure visible posts, put sticky first
        posts = posts.filter(post_visible=True)
        sticky_posts = posts.filter(post_sticky=True)
        posts = posts.filter(post_sticky=False)
        # append stick_posts to the top of posts
        posts = list(chain(sticky_posts, posts))

        # set up paginator
        settings = Settings.load()
        paginator = Paginator(posts, settings.posts_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # pass paginated posts and topic to template
        context = {'page_obj': page_obj, 'topic': topic_requested}
        return render(request, 'forum/topic.html', context)
    else:
        # Topic not found -> 404
        messages.add_message(request, messages.ERROR, 'Invalid topic')
        return redirect('index')


def post(request, topic_id, post_id):
    """
    View function for viewing a post. This is the page that displays a post and its comments. If the user is
    authenticated and the post is not locked, they can also create a new comment. Comments are displayed in
    paginated form. Sticky comments come first, with the rest in order of creation.

    Args:
        request: The request object.
        topic_id: The id of the topic to be viewed, used to get the topic from the database.
        post_id: The id of the post to be viewed, used to get the post from the database.

    Returns:
        Redirects user if topic or post does not exist or a permission error occurs. Otherwise, returns a rendered
        template of the post page (forum/post.html) with the post and comments that the user has access to.

    """
    # get post from post_id
    post_requested = Post.objects.filter(id=post_id).first()

    if post_requested:
        # check if post is visible
        if not post_requested.post_visible:
            messages.add_message(request, messages.ERROR, 'Invalid post')
            return redirect('index')
        # check if post_requested.topic_id matches topic_id
        if post_requested.post_topic.id != topic_id:
            messages.add_message(request, messages.ERROR, 'Invalid post')
            return redirect('index')

        # establish comment form
        form = CommentForm()
        form.fields['comment_post'].initial = post_id

        # get comments so the most recent is last, ensure sticky first
        comments = post_requested.comment_set.order_by('created_at')
        sticky_comments = comments.filter(comment_sticky=True)
        comments = comments.filter(comment_sticky=False)
        # append stick_comments to the top of comments
        comments = list(chain(sticky_comments, comments))

        # set up paginator
        settings = Settings.load()
        paginator = Paginator(comments, settings.comments_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # pass paginated comments, post, and form to template
        context = {'post': post_requested, 'topic': post_requested.post_topic, 'form': form, 'page_obj': page_obj}
        return render(request, 'forum/post.html', context)
    else:
        # Post not found -> 404
        messages.add_message(request, messages.ERROR, 'Invalid post')
        return redirect('index')


@login_required
def new_post(request, topic_id):
    """
    View function for creating a new post. This is the page that allows a user to create a new post in a topic.
    If it is recived as a POST, the form is validated and the post is created. If it is received as a GET, the
    form is displayed via the template (forum/form/post_form.html).
    Args:
        request: The request object.
        topic_id: This is the topic ID that the post will be created in. Created posts reference this topic, and it
            is used to validate any permissions.

    Returns:
        Redirects user if topic does not exist or a permission error occurs. Otherwise, returns a rendered template
        of the new post page (forum/form/post_form.html) with the form. If recieved as a POST, the form is validated
        and the post is created. If the form is invalid, the user is redirected with an error message.

    """
    if request.method == 'POST':
        # create form from POST data
        form = PostForm(request.POST)
        if form.is_valid():
            # get topic if exists
            topic_requested = Topic.objects.filter(id=topic_id).first()

            # if topic_requested exists
            if (not topic_requested) or form.cleaned_data['post_topic'] != topic_requested:
                return redirect('index')

            # check if restricted superuser
            if topic_requested.restricted_superuser and not request.user.is_superuser:
                return redirect('index')

            # check if max langth is violated
            if len(form.cleaned_data['post_content']) > 5000:
                messages.add_message(request, messages.ERROR, 'Post content too long')
                return redirect('index')

            # save form with post_user
            form.save(commit=False)
            form.instance.post_user = request.user
            form.save()

            # redirect to post
            messages.add_message(request, messages.SUCCESS, 'Posted successfully')
            return redirect('post', topic_id=topic_id, post_id=form.instance.id)
    # else
    else:
        form = PostForm()
        # form with topic_id as post_topic
        form.fields['post_topic'].initial = topic_id

    # get topic_id if exists
    topic_requested = Topic.objects.filter(id=topic_id).first()

    # if topic_requested doesn't exist
    if not topic_requested:
        return redirect('index')

    # pass form and topic to template
    context = {'form': form, 'topic': topic_requested}
    return render(request, 'forum/form/post_form.html', context)


@login_required
def new_comment(request, topic_id, post_id):
    """
    View function for creating a new comment. This function responds to POSTs from the comment form on a post page.
    The form is validated and the comment is created. If the form is invalid, the user is redirected with an error.

    Args:
        request: The request object.
        topic_id: The topic ID of the Post that the comment will be created in.
        post_id: The post ID of the Post that the comment will be created in.

    Returns:
        A redirect to the post page if the comment is created successfully. Otherwise, the user is redirected with
        an error message.

    """
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            # check for any max length violations
            if len(form.cleaned_data['comment_content']) > 5000:
                messages.add_message(request, messages.ERROR, 'Comment too long')
                return redirect('post', topic_id=topic_id, post_id=post_id)

            # ensure post_locked is not violated
            post_requested = Post.objects.filter(id=post_id).first()
            if post_requested.post_locked:
                messages.add_message(request, messages.ERROR, 'Post locked')
                return redirect('post', topic_id=topic_id, post_id=post_id)

            # save form with comment_user
            form.save(commit=False)
            form.instance.comment_user = request.user
            form.save()

            # Update the post to show it was updated (for ranking)
            post_requested.updated_at = timezone.now()
            post_requested.save()

            # redirect to post with new comment
            messages.add_message(request, messages.SUCCESS, 'Posted successfully')
            return redirect('post', topic_id=topic_id, post_id=post_id)
