from django.contrib.auth.models import User

from .models import Notification
from .tasks import send_notification, send_email


def create_notification(message, role=None, users=None, is_send_notification=True, is_send_email=True):
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

    if is_send_notification:
        send_notification(users, message)

    if is_send_email:
        send_email(users, message)
