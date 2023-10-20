from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ("slug", "username", "email", "date_joined")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("slug", "username", "email", "first_name", "last_name")
    list_display_links = ("username",)


admin.site.register(User, UserAdmin)