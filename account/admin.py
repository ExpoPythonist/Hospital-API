from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.list_display += ('status',)
UserAdmin.list_filter += ('status',)
UserAdmin.fieldsets += (('Status', {'fields': ('status',)}),)
admin.site.register(User, UserAdmin)
