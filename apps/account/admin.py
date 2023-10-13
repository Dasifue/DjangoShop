from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ("username", "email", "date_joined")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("slug", "username", "email", "first_name", "last_name")


admin.site.register(User, UserAdmin)