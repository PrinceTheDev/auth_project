from django.db import models as dj_models
from django.contrib.auth.models import AbstractUser
from includes.helpers import PrimaryKeyMixin, DateHistoryMixin, InvalidInputError
from .manager import CustomUserManager

import re
from datetime import datetime, timezone


"""
This module defines the custom user model for the
authentication system. 
"""


class User(AbstractUser, PrimaryKeyMixin, DateHistoryMixin):
    email = dj_models.EmailField(unique=True)
    phone = dj_models.CharField(max_length=15, blank=True, null=True)
    is_email_verified = dj_models.BooleanField(default=False)
    is_phone_verified = dj_models.BooleanField(default=False)
    profile_picture = dj_models.ImageField(upload_to='', blank=True, null=True)
    date_created = dj_models.DateTimeField(auto_now_add=True)
    last_login_ip = dj_models.GenericIPAddressField(blank=True, null=True)
    is_active = dj_models.BooleanField(default=True)
    is_superusr = dj_models.BooleanField(default=False)
    failed_login_attempts = dj_models.IntegerField(default=0)
    email_verification_datetime = dj_models.DateTimeField(blank=True, null=True)
    phone_verification_datetime = dj_models.DateTimeField(blank=True, null=True)
    is_locked = dj_models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'user'

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.clean_names()
        self.validate_phone_no()
        super().save(*args, **kwargs)


    def validate_name(self, value: str) -> str:
        if not re.match(r"^[A-Za-z]+([A-Za-z]+)*$", value):
            raise ValueError("Invalid Name")
        if len(value) < 2 or len(value) > 50:
            raise ValueError("Name must be between 2 and 50 characters")
        
        return value
    
    def validate_phone_no(self):
        if self.phone:
            pattern = re.compile(r"^\+[1-9]\d{1,14}$")
            if not pattern.match(self.phone):
                raise InvalidInputError("Invalid phone number format")
            

    def clean_names(self):
        if self.first_name:
            self.first_name = self.validate_name(self.first_name)
        if self.last_name:
            self.last_name = self.validate_name(self.last_name)

    def get_full_names(self):
        return " ".join(filter(None, [self.first_name, self.last_name])
    )
    

    @property
    def is_email_verified(self) -> bool:
        return self.email_verification_datetime is not None
    
    @property
    def is_phone_verified(self) -> bool:
        return self.phone_verification_datetime is not None
    

    @property
    def can_request_new_otp(self) -> bool:
        return (
            not hasattr(self, "otp_model")
            or self.otp_model.date_created_at + timezone.timedelta(minutes=5)
            < timezone.now()
        )