from django.contrib import admin

# Register your models here.
from .models import PrivateMessage, PrivateMessageReplies


class PrivateMessageRepliesInline(admin.TabularInline):
    """
    Inline for PrivateMessageReplies allows admin view to see replies within private messages.
    """
    model = PrivateMessageReplies
    extra = 0


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    """
    Admin view for PrivateMessage model. Allows admin to view, moderate, and interact with private messages.
    Also allows admin to view replies within private messages as inline.
    """
    list_display = ('pm_sender', 'pm_receiver', 'pm_title', 'pm_content', 'created_at', 'updated_at')
    list_filter = ('created_at', 'pm_sender', 'pm_receiver')
    search_fields = ('pm_sender', 'pm_receiver', 'pm_title', 'pm_content')
    date_hierarchy = 'updated_at'

    # Display replies inline
    inlines = [
        PrivateMessageRepliesInline,
    ]
