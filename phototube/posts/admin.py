from django.contrib import admin

from .models import Comment, Follow, Group, Post


class CommentAdmin(admin.StackedInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "text",
        "pub_date",
        "author",
        "group",
    )

    inlines = [CommentAdmin]

    list_editable = ("group",)
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
admin.site.register(Follow)
