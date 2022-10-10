from django.db import models


# Model fo private messages
class PrivateMessage(models.Model):
    pm_sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pm_sender')
    pm_receiver = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pm_receiver')
    pm_title = models.CharField(max_length=100)
    pm_content = models.TextField(max_length=5000)
    pm_read_sender = models.BooleanField(default=True)
    pm_read_receiver = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_replies(self):
        return PrivateMessage.objects.filter(pmr_pm=self.pk)

    # get number of replies
    def get_num_replies(self):
        return PrivateMessage.objects.filter(pmr_pm=self.pk).count()

    def __str__(self):
        return self.pm_content

    class Meta:
        ordering = ['-created_at']


# Model for private message replies
class PrivateMessageReplies(models.Model):
    pmr_pm = models.ForeignKey('PrivateMessage', on_delete=models.CASCADE, related_name='pmr_pm')
    pmr_sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pmr_sender')
    pmr_content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pmr_content
