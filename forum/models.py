from django.db import models


# Create your models here.

# Model for topics
class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    topic_description = models.CharField(max_length=200)
    restricted_superuser = models.BooleanField(default=False)
    restricted_logged_in = models.BooleanField(default=False)

    # method to get latest post from post model with post_topic as this
    def get_latest_post(self):
        return self.post_set.order_by('-created_at').first()

    def __str__(self):
        return self.topic_name


# Model for posts
class Post(models.Model):
    post_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # user
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    post_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # date
    created_at = models.DateTimeField(auto_now_add=True)
    # Locked bool
    post_locked = models.BooleanField(default=False)
    # visible bool -- for soft delete
    post_visible = models.BooleanField(default=True)
    # sticky bool
    post_sticky = models.BooleanField(default=False)

    def __str__(self):
        return self.post_title


# Model for comments (replies)
class Comment(models.Model):
    comment_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # user
    comment_content = models.TextField()
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_visible = models.BooleanField(default=True)
    comment_sticky = models.BooleanField(default=False)
    # date
    created_at = models.DateTimeField(auto_now_add=True)
    # visible bool
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.comment_content
