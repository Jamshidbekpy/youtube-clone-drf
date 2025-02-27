from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from .models import MyUser,Channel,UserProfile
class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ['username', 'email', 'profile_picture']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_picture', 'bio')}),
    )

admin.site.register(MyUser, MyUserAdmin)

admin.site.register(Channel)
admin.site.register(UserProfile)
