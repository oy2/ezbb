from django.contrib import admin

# Register your models here.

from .models import Topic, Post, Comment


# Register Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_topic', 'post_title', 'post_user', 'created_at', 'post_locked', 'post_visible', 'post_sticky')
    list_filter = ('created_at', 'post_user', 'post_topic')
    search_fields = ('post_title', 'post_content')
    date_hierarchy = 'created_at'

admin.site.register(Topic)

admin.site.register(Comment)



