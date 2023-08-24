from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.account.models import User

class UserModelAdmin(BaseUserAdmin):
    list_display = ["id", "email", "full_name"]
    list_filter = ["id"]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "full_name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", 'id']
    filter_horizontal = []

# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)