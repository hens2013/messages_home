from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import ModelAdmin, register

from messages_sending.models import Message, Profile

# Register your models here.
admin.site.site_header = 'Admin Site'


@register(Message)
class MessageAdmin(ImportExportModelAdmin):
    list_display = (
        'content', "subject", "receiver", "sender", "creation_time", "receiver")
    list_filter = ("sender", "receiver")


@register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    list_display = (
         'username', 'phone_number', 'first_name', 'last_name')