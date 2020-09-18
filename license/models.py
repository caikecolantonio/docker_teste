""" Data model for licenses application
"""
import enum
from datetime import timedelta, datetime
from typing import Tuple, List
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

LICENSE_EXPIRATION_DELTA = timedelta(days=90)


def get_default_license_expiration() -> datetime:
    """Get the default expiration datetime"""
    return datetime.utcnow() + LICENSE_EXPIRATION_DELTA


class License(models.Model):
    """ Data model for a client license allowing access to a package
    """
    PACKAGE_CHOISES = (
    ('Production', 'Production'),
    ('Evaluation', 'Evaluation'),
    )
    LICENSE_CHOISES = (
        ('js', 'Javascript_sdk'),
        ('ios', 'Ios_sdk'),
        ('android', 'Android_sdk'),
    )

    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    package = models.CharField(max_length=15, choices=PACKAGE_CHOISES, blank=True, null=True)
    license_type = models.CharField(max_length=15, choices=LICENSE_CHOISES, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField(default=get_default_license_expiration)
    is_send = models.BooleanField(default=False, blank=True, null=True)

    def days_to_expire(self):
        return (self.expiration_datetime - timezone.now()).days


class Client(models.Model):
    """ A client who holds licenses to packages
    """
    client_name = models.CharField(max_length=120, unique=True)
    poc_contact_name = models.CharField(max_length=120)
    poc_contact_email = models.EmailField()

    admin_poc = models.ForeignKey(User, limit_choices_to={'is_staff': True}, on_delete=models.CASCADE)

    def __str__(self):
        return self.client_name   
