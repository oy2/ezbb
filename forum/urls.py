from django.urls import path
from . import views

# The following is a list of all the paths that are available to the user for the forum app.
urlpatterns = [
    path('', views.index, name='index'),
    # topic/topic_id
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    # topic/topicid_id/new
    path('topic/<int:topic_id>/new', views.new_post, name='new_post'),
    # topic/topic_id/post/post_id
    path('topic/<int:topic_id>/post/<int:post_id>/', views.post, name='post'),
    # topic/topic_id/post/post_id/new
    path('topic/<int:topic_id>/post/<int:post_id>/new', views.new_comment, name='new_comment'),
]
