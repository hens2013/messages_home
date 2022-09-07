from django.contrib import admin
from django.contrib.admin import register

from messages_sending.models import Message, Profile

# Register your models here.
admin.site.site_header = 'Admin Site'



from rest_framework.serializers import ModelSerializer


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'