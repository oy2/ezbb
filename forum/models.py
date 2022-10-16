from django.core.cache import cache
from django.db import models


class Topic(models.Model):
    """
    This model is used for Topics within the forum. Topics are used to group posts together. Topics have a name and a
    description. Topics can be restricted to superusers only or logged in users only.

    Attributes:
        topic_name (str): The name of the topic. [max_length=200]
        topic_description (str): The description of the topic. [max_length=200]
        restricted_superuser (bool): If the topic is restricted to superusers only.
        restricted_logged_in (bool): If the topic is restricted to logged in users only.

    """
    topic_name = models.CharField(max_length=200)
    topic_description = models.CharField(max_length=200)
    restricted_superuser = models.BooleanField(default=False)
    restricted_logged_in = models.BooleanField(default=False)

    def get_latest_post(self):
        """
        Get the latest post in the topic and return it. The post_set for this topic refers to items in the Post model
        with this Topic as a foreign key. The order_by method is used to sort the posts by the updated_at field in
        descending order. The first item in the list is returned.

        Returns:
            Post: The latest post in the topic.
            Empty: If there are no posts in the topic.

        """
        return self.post_set.order_by('-created_at').first()

    def get_latest_post_link(self):
        """
        Returns the link to the latest post in the topic. References the get_latest_post method to get the latest post.
        Always validate that there is a posts to avoid unexpected errors.

        Returns:
            str: The link to the latest post in the topic.

        """
        return f'/topic/{self.id}/post/{self.get_latest_post().id}/'

    def __str__(self):
        """
        Returns the topic name when the object is called.

        Returns:
            str: The topic name.

        """
        return self.topic_name


class Post(models.Model):
    """
    This model is used for Posts within the forum. Posts are used to group comments together. Posts have a title and a
    description. Posts are created by a user and are assigned to a topic. They inherit visibility from the topic. Posts
    may be locked, sticky, or hidden.

    Attributes:
        post_title (str): The title of the post. [max_length=200]
        post_content (str): The content of the post. [max_length=5000]
        post_topic (Topic): The topic that the post belongs to.
        post_user (User): The user that created the post.
        post_locked (bool): If the post is locked.
        post_visible (bool): If the post is visible.
        post_sticky (bool): If the post is sticky.

    """
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


class Comment(models.Model):
    """
    This model is used for Comments within the forum. Comments are used to reply to posts. Comments have content and are
    created by a user. They are assigned to a post. They inherit visibility from the post. Comments may be hidden.

    Attributes:
        comment_content (str): The content of the comment. [max_length=5000]
        comment_post (Post): The post that the comment belongs to.
        comment_user (User): The user that created the comment.
        comment_visible (bool): If the comment is visible.

    """
    comment_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # user
    comment_content = models.TextField(max_length=5000)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_visible = models.BooleanField(default=True)
    comment_sticky = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content


class SingletonModel(models.Model):
    """
    This is an abstract model that is used to create singleton models. Singleton models are used to store a single
    instance of a model. This is used to store the forum settings.
    """
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
    """
    This model is used to store the settings for the forum. Settings are used to configure the forum. Settings are
    stored in a singleton model. This means that there is only one instance of the model. This is modifiable within
    the admin panel.
    """
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
