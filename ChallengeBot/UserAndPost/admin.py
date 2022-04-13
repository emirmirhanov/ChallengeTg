
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Post, Report, Members
# Register your models here.


@admin.register(Members)
class MembersAdd(admin.ModelAdmin):
    search_fields = ("name__startswith", "user_name__startswith")
    fields = ('name', 'lastname', 'user_name', 'live')
    list_display = ('name', 'lastname', 'user_name', 'live')


@admin.register(Post)
class PostAdd(admin.ModelAdmin):
    fields = ('content', 'active')
    list_display = ('content', 'active')


@admin.register(Report)
class ReportAdd(admin.ModelAdmin):
    list_display = ('member', 'type_challenge', 'time')


admin.site.unregister(Group)
