from django.core.cache import cache
from django.db import models


# Create your models here.

# Model for topics
class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    topic_description = models.CharField(max_length=200)
    restricted_superuser = models.BooleanField(default=False)
    restricted_logged_in = models.BooleanField(default=False)

    def get_latest_post(self):
        return self.post_set.order_by('-created_at').first()

    def get_latest_post_link(self):
        return f'/topic/{self.id}/post/{self.get_latest_post().id}/'

    def __str__(self):
        return self.topic_name


# Model for posts
class Post(models.Model):
    post_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # user
    post_title = models.CharField(max_length=200)
    post_content = models.TextField(max_length=5000)
    post_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # date
    created_at = models.DateTimeField(auto_now_add=True)
    # Locked bool
    post_locked = models.BooleanField(default=False)
    # visible bool -- for soft delete
    post_visible = models.BooleanField(default=True)
    # sticky bool
    post_sticky = models.BooleanField(default=False)
    # updated_at
    updated_at = models.DateTimeField(auto_now=True)

    def get_latest_comment(self):
        # return the latest comment
        # return Comment.objects.filter(comment_post=self).order_by('-created_at').first()
        return self.comment_set.order_by('-created_at').first()

    def __str__(self):
        return self.post_title


# Model for comments (replies)
class Comment(models.Model):
    comment_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # user
    comment_content = models.TextField(max_length=5000)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_visible = models.BooleanField(default=True)
    comment_sticky = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content


# singleton settings model
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

    def set_cache(self):
        cache.set(self.__class__.__name__, self)


# ezbb Settings Model *Singleton*
class Settings(SingletonModel):
    class Meta:
        verbose_name = 'Setting'
    site_name = models.CharField(max_length=200, default='ezbb')
    site_description = models.CharField(max_length=200, default='An ezbb site')

    index_welcome_banner_enabled = models.BooleanField(default=True)
    index_welcome_banner_title = models.TextField(max_length=5000, default='Welcome to ezbb!')
    index_welcome_banner_content = models.TextField(max_length=5000, default='Welcome to your new installation of '
                                                                             'ezbb. This message can be changed from '
                                                                             'the settings section in the admin site! '
                                                                             'To get started with your new forum add '
                                                                             'a topic in the admin site!')

    posts_per_page = models.IntegerField(default=10)
    comments_per_page = models.IntegerField(default=10)



    footer_social_links = models.BooleanField(default=True)
    footer_social_links_facebook = models.CharField(max_length=200, default='#')
    footer_social_links_twitter = models.CharField(max_length=200, default='#')
    footer_social_links_instagram = models.CharField(max_length=200, default='#')
    footer_privacy_policy = models.CharField(max_length=200, default='#')
    footer_terms_of_service = models.CharField(max_length=200, default='#')
    accounts_signup_enabled = models.BooleanField(default=True)
