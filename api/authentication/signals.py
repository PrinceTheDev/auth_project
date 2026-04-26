from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


"""
This module contains signal handlers related to user authentication
events.
"""


@receiver(user_logged_in)
def update_last_login_ip(sender, user, request, **kwargs):
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        user.last_login_ip = ip
        user.save(update_fields=['last_login_ip'])

