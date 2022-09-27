from django.contrib.auth.models import User
from django.test import TestCase

from forum.models import Topic, Post, Comment


# Test for topic model
class TopicModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Topic.objects.create(topic_name='test topic', topic_description='test topic description')

    def test_topic_name_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('topic_name').verbose_name
        self.assertEquals(field_label, 'topic name')

    def test_topic_description_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('topic_description').verbose_name
        self.assertEquals(field_label, 'topic description')

    def test_topic_name_max_length(self):
        topic = Topic.objects.get(id=1)
        max_length = topic._meta.get_field('topic_name').max_length
        self.assertEquals(max_length, 200)

    def test_topic_description_max_length(self):
        topic = Topic.objects.get(id=1)
        max_length = topic._meta.get_field('topic_description').max_length
        self.assertEquals(max_length, 200)

    def test_topic_name(self):
        topic = Topic.objects.get(id=1)
        expected_object_name = f'{topic.topic_name}'
        self.assertEquals(expected_object_name, 'test topic')

    def test_topic_description(self):
        topic = Topic.objects.get(id=1)
        expected_object_name = f'{topic.topic_description}'
        self.assertEquals(expected_object_name, 'test topic description')

    def test_topic_restricted_superuser(self):
        topic = Topic.objects.get(id=1)
        expected_object_name = f'{topic.restricted_superuser}'
        self.assertEquals(expected_object_name, 'False')

    def test_topic_restricted_logged_in(self):
        topic = Topic.objects.get(id=1)
        expected_object_name = f'{topic.restricted_logged_in}'
        self.assertEquals(expected_object_name, 'False')


# Post model test
class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create user for tests
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        # create topic for tests
        test_topic = Topic.objects.create(topic_name='test topic', topic_description='test topic description')
        # Set up non-modified objects used by all test methods
        Post.objects.create(post_title='test post',
                            post_content='test post content',
                            post_topic=test_topic,
                            post_user=test_user1)

    def test_post_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('post_title').verbose_name
        self.assertEquals(field_label, 'post title')

    def test_post_content_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('post_content').verbose_name
        self.assertEquals(field_label, 'post content')

    def test_post_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('post_title').max_length
        self.assertEquals(max_length, 200)

    def test_post_title(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.post_title}'
        self.assertEquals(expected_object_name, 'test post')

    def test_post_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.post_content}'
        self.assertEquals(expected_object_name, 'test post content')

    def test_post_locked(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.post_locked}'
        self.assertEquals(expected_object_name, 'False')

    def test_post_visible(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.post_visible}'
        self.assertEquals(expected_object_name, 'True')

    def test_post_sticky(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.post_sticky}'
        self.assertEquals(expected_object_name, 'False')


# Comment model test
class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create user for tests
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        # create topic for tests
        test_topic = Topic.objects.create(topic_name='test topic', topic_description='test topic description')
        # create post for tests
        test_post = Post.objects.create(post_title='test post',
                                        post_content='test post content',
                                        post_topic=test_topic,
                                        post_user=test_user1)
        # Set up non-modified objects used by all test methods
        Comment.objects.create(comment_content='test comment content',
                               comment_post=test_post,
                               comment_user=test_user1)

    def test_comment_content_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('comment_content').verbose_name
        self.assertEquals(field_label, 'comment content')

    def test_comment_content(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = f'{comment.comment_content}'
        self.assertEquals(expected_object_name, 'test comment content')

    def test_comment_visible(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = f'{comment.comment_visible}'
        self.assertEquals(expected_object_name, 'True')

    def test_comment_sticky(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = f'{comment.comment_sticky}'
        self.assertEquals(expected_object_name, 'False')