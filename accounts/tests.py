from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import PrivateMessageForm, RegisterForm, PrivateMessageReplyForm
from accounts.models import PrivateMessage, PrivateMessageReplies


# Test models/PrivateMessage
class PrivateMessageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create a user for sender
        sender = User.objects.create_user(username='sender', password='1X<ISRUkw+tuK')
        # create a user for receiver
        receiver = User.objects.create_user(username='receiver', password='1X<ISRUkw+tuK')
        # create a private message
        PrivateMessage.objects.create(pm_sender=sender, pm_receiver=receiver, pm_title='test title',
                                      pm_content='test content')

    def test_pm_sender_label(self):
        pm = PrivateMessage.objects.get(id=1)
        field_label = pm._meta.get_field('pm_sender').verbose_name
        self.assertEquals(field_label, 'pm sender')

    def test_pm_receiver_label(self):
        pm = PrivateMessage.objects.get(id=1)
        field_label = pm._meta.get_field('pm_receiver').verbose_name
        self.assertEquals(field_label, 'pm receiver')

    def test_pm_title_label(self):
        pm = PrivateMessage.objects.get(id=1)
        field_label = pm._meta.get_field('pm_title').verbose_name
        self.assertEquals(field_label, 'pm title')

    def test_pm_content_label(self):
        pm = PrivateMessage.objects.get(id=1)
        field_label = pm._meta.get_field('pm_content').verbose_name
        self.assertEquals(field_label, 'pm content')

    def test_pm_read_sender_label(self):
        pm = PrivateMessage.objects.get(id=1)
        field_label = pm._meta.get_field('pm_read_sender').verbose_name
        self.assertEquals(field_label, 'pm read sender')

    def test_pm_read_receiver_label(self):
        pm = PrivateMessage.objects.get(id=1)
        field_label = pm._meta.get_field('pm_read_receiver').verbose_name
        self.assertEquals(field_label, 'pm read receiver')

    def test_pm_title_max_length(self):
        pm = PrivateMessage.objects.get(id=1)
        max_length = pm._meta.get_field('pm_title').max_length
        self.assertEquals(max_length, 100)

    def test_pm_content_max_length(self):
        pm = PrivateMessage.objects.get(id=1)
        max_length = pm._meta.get_field('pm_content').max_length
        self.assertEquals(max_length, 5000)

    def test_pm_sender(self):
        pm = PrivateMessage.objects.get(id=1)
        expected_object_name = f'{pm.pm_sender}'
        self.assertEquals(expected_object_name, 'sender')

    def test_pm_receiver(self):
        pm = PrivateMessage.objects.get(id=1)
        expected_object_name = f'{pm.pm_receiver}'
        self.assertEquals(expected_object_name, 'receiver')

    def test_pm_title(self):
        pm = PrivateMessage.objects.get(id=1)
        expected_object_name = f'{pm.pm_title}'
        self.assertEquals(expected_object_name, 'test title')


# Test models/PrivateMessageReplies
class PrivateMessageRepliesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create a user for sender
        sender = User.objects.create_user(username='sender', password='1X<ISRUkw+tuK')
        # create a user for receiver
        receiver = User.objects.create_user(username='receiver', password='1X<ISRUkw+tuK')
        # create a private message
        pm = PrivateMessage.objects.create(pm_sender=sender, pm_receiver=receiver, pm_title='test title',
                                           pm_content='test content')
        # create a private message reply
        PrivateMessageReplies.objects.create(pmr_pm=pm, pmr_sender=sender, pmr_content='test content')

    def test_pmr_pm_label(self):
        pmr = PrivateMessageReplies.objects.get(id=1)
        field_label = pmr._meta.get_field('pmr_pm').verbose_name
        self.assertEquals(field_label, 'pmr pm')

    def test_pmr_sender_label(self):
        pmr = PrivateMessageReplies.objects.get(id=1)
        field_label = pmr._meta.get_field('pmr_sender').verbose_name
        self.assertEquals(field_label, 'pmr sender')

    def test_pmr_content_label(self):
        pmr = PrivateMessageReplies.objects.get(id=1)
        field_label = pmr._meta.get_field('pmr_content').verbose_name
        self.assertEquals(field_label, 'pmr content')

    def test_pmr_content_max_length(self):
        pmr = PrivateMessageReplies.objects.get(id=1)
        max_length = pmr._meta.get_field('pmr_content').max_length
        self.assertEquals(max_length, 5000)

    def test_pmr_pm(self):
        pmr = PrivateMessageReplies.objects.get(id=1)
        expected_object_name = f'{pmr.pmr_pm}'
        self.assertEquals(expected_object_name, 'test content')

    def test_pmr_sender(self):
        pmr = PrivateMessageReplies.objects.get(id=1)
        expected_object_name = f'{pmr.pmr_sender}'
        self.assertEquals(expected_object_name, 'sender')

    def test_pmr_content(self):
        pmr = PrivateMessageReplies.objects.get(id=1)
        expected_object_name = f'{pmr.pmr_content}'
        self.assertEquals(expected_object_name, 'test content')


# Test forms/RegisterForm
class RegisterFormTest(TestCase):

    def test_register_form(self):
        form_data = {'username': 'testuser', 'email': 'test@abc.com', 'password': '1X<ISRUkw+tuK',
                     'password2': '1X<ISRUkw+tuK'}
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid(self):
        form_data = {'username': 'testuser', 'email': 'test@abc.com', 'password': '1X<+tuK', 'password2': '1X<ISRUkw+tuK'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


# Test forms/PrivateMessageForm
class PrivateMessageFormTest(TestCase):
    def test_pm_form(self):
        form = PrivateMessageForm(data={'pm_title': 'test title', 'pm_content': 'test content'})
        self.assertTrue(form.is_valid())

    def test_pm_form_invalid(self):
        form = PrivateMessageForm(data={'pm_title': '', 'pm_content': ''})
        self.assertFalse(form.is_valid())


# Test forms/PrivateMessageRepliesForm
class PrivateMessageRepliesFormTest(TestCase):
    def test_pmr_form(self):
        form = PrivateMessageReplyForm(data={'pmr_content': 'test content'})
        self.assertTrue(form.is_valid())

    def test_pmr_form_invalid(self):
        form = PrivateMessageReplyForm(data={'pmr_content': ''})
        self.assertFalse(form.is_valid())
