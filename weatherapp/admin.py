from django.contrib import admin
from .models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['user', 'cities']
    list_display_links = ['user']
    list_editable = ['cities']


admin.site.register(UserInfo, UserInfoAdmin)
