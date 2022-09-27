from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # topic/topic_id
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    # post/post_id
    path('post/<int:post_id>/', views.post, name='post'),
    # new_post
    path('post/newpost/', views.new_post, name='newpost'),
    # new_comment
    path('post/newcomment/', views.new_comment, name='newcomment'),
]
