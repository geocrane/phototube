from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_superuser",
    )

    search_fields = ("username",)
    list_filter = ("is_superuser",)
    empty_value_display = "-пусто-"
