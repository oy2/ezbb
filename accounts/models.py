from django.db import models


class PrivateMessage(models.Model):
    """
    Model for private messages. Allows users to send private messages to other users.

    Attributes:
        pm_sender: User who sent the private message.
        pm_receiver: User who received the private message.
        pm_title: Title of the private message.
        pm_content: Content of the private message.
        pm_read_sender: Boolean to indicate if the sender has read the private message.
        pm_read_receiver: Boolean to indicate if the receiver has read the private message.
        created_at: Date and time when the private message was created.
        updated_at: Date and time when the private message was last updated.

    """
    pm_sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pm_sender')
    pm_receiver = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pm_receiver')
    pm_title = models.CharField(max_length=100)
    pm_content = models.TextField(max_length=5000)
    pm_read_sender = models.BooleanField(default=True)
    pm_read_receiver = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_replies(self):
        """
        Get all replies for a private message. Collects replies with message as foreign key.

        Returns:
            List of replies.

        """
        return PrivateMessageReplies.objects.filter(pmr_pm=self.pk)

    def get_num_replies(self):
        """
        Get the number of replies for a private message. Collects replies with message as foreign key and counts them.

        Returns:
            Number of replies.

        """
        return PrivateMessageReplies.objects.filter(pmr_pm=self.pk).count()

    def __str__(self):
        return self.pm_content

    class Meta:
        ordering = ['-created_at']


class PrivateMessageReplies(models.Model):
    """
    Model for private message replies. Allows users to reply to private messages.

    Attributes:
        pmr_pm: Private message that the reply is for.
        pmr_sender: User who sent the private message reply.
        pmr_content: Content of the private message reply.
        created_at: Date and time when the private message reply was created.

    """
    pmr_pm = models.ForeignKey('PrivateMessage', on_delete=models.CASCADE, related_name='pmr_pm')
    pmr_sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pmr_sender')
    pmr_content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pmr_content
