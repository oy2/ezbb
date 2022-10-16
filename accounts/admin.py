from django.contrib import admin

# Register your models here.
from .models import PrivateMessage, PrivateMessageReplies


class PrivateMessageRepliesInline(admin.TabularInline):
    model = PrivateMessageReplies
    extra = 0


# Register PrivateMessages model with Replies in admin
@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('pm_sender', 'pm_receiver', 'pm_title', 'pm_content', 'created_at', 'updated_at')
    list_filter = ('created_at', 'pm_sender', 'pm_receiver')
    search_fields = ('pm_sender', 'pm_receiver', 'pm_title', 'pm_content')
    date_hierarchy = 'updated_at'

    # Display replies inline
    inlines = [
        PrivateMessageRepliesInline,
    ]
