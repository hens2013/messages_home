
import json
from datetime import datetime

from django.db import models
from django.db.models import DateTimeField

from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator

class Profile(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=120, blank=False, null=True, unique=True, validators=[phone_regex])
    is_active = models.BooleanField(default=True)

class Message(models.Model):
    content = models.TextField(help_text='Message text', null=False, blank=True)
    subject = models.TextField(help_text='Message text', null=False, blank=True)
    creation_time = DateTimeField(default=datetime.now)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    read = models.BooleanField(default=False, null=True, blank=True)
    receiver = models.TextField(help_text='Phone numbers', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['receiver', 'creation_time']),
        ]

    def sender_name(self):
        return self.sender.first_name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
# Create your models here.
