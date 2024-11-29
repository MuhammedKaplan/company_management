﻿from django.contrib.auth.models import User

from .models import Notification
from .tasks import send_late_notification, send_late_email


def create_notification(message, role=None, users=None, send_notification=False, send_email=False):
    if role:
        users = User.objects.filter(employee__role=role)
    elif users:
        users = User.objects.filter(id__in=users)
    else:
        users = User.objects.all()

    notifications = [
        Notification(recipient=user, message=message, role=user.employee.role)
        for user in users
    ]
    Notification.objects.bulk_create(notifications)

    if send_notification:
        send_late_notification(users, message)

    if send_email:
        send_late_email(users, message)
