from django.contrib import admin

# Register your models here.

from .models import Topic, Post, Comment


# Comment inline class
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

# Register Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'post_topic', 'post_title', 'post_user', 'created_at', 'updated_at', 'post_locked', 'post_visible',
        'post_sticky')
    list_filter = ('created_at', 'post_user', 'post_topic')
    search_fields = ('post_title', 'post_content')
    date_hierarchy = 'updated_at'

    # Display comments inline
    inlines = [
        CommentInline,
    ]


admin.site.register(Topic)


