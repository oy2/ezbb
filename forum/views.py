from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from forum.forms import PostForm
from forum.models import Topic, Post


# View for index
def index(request):
    # Get all topics
    topics = Topic.objects.all()
    # pass topics
    context = {'topics': topics}
    return render(request, 'forum/index.html', context)


# Views viewing topics
def topic(request, topic_id):
    # get topic from topic_id
    topic_requested = Topic.objects.filter(id=topic_id).first()
    # check if exists
    if topic_requested:
        # check if restricted superuser
        if topic_requested.restricted_superuser and not request.user.is_superuser:
            return redirect('index')
        # check if restricted logged in
        if topic_requested.restricted_logged_in and not request.user.is_authenticated:
            return redirect('index')
        # get posts in order so most recent is first
        posts = topic_requested.post_set.order_by('-created_at')
        paginator = Paginator(posts, 10)  # show 10 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # pass posts
        context = {'page_obj': page_obj, 'topic': topic_requested}
        return render(request, 'forum/topic.html', context)
    else:
        # 404 todo
        return redirect('index')


# View for viewing posts
def post(request, post_id):
    # get post from post_id
    post_requested = Post.objects.filter(id=post_id).first()
    # check if exists
    if post_requested:
        # check if post is visible
        if not post_requested.post_visible:
            return redirect('index')
        # pass post
        context = {'post': post_requested, 'topic': post_requested.post_topic}
        return render(request, 'forum/post.html', context)
    else:
        # 404 todo
        return redirect('index')


# View for /newpost
@login_required
def newpost(request):
    # if post
    if request.method == 'POST':
        # form
        form = PostForm(request.POST)
        # if valid
        if form.is_valid():
            form.save()
            return redirect('index')
    # else
    else:
        form = PostForm()
    # pass form
    context = {'form': form}
    return render(request, 'forum/form/post_form.html', context)
