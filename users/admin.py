from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User
from cart.models import Cart

admin.site.unregister(Group)


class CartInline(admin.StackedInline):
    model = Cart
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'full_name', 'last_login']
    list_display_links = ['id', 'email', 'full_name', 'last_login']
    search_fields = ['email', 'full_name']
    list_filter = ['is_active', 'is_staff']
    fieldsets = [
        (
            None,
            {
                "fields": ['email', 'full_name', 'date_joined', 'last_login', 'is_active']
            }
        )
    ]
    inlines = [CartInline]
