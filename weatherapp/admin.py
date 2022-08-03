from django.contrib import admin
from .models import UserInfo, Cities


class UserInfoAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['user']
    list_display_links = ['user']


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Cities)
