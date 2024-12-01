from asgiref.sync import async_to_sync

from celery import shared_task
from channels.layers import get_channel_layer
from django.core.mail import send_mail


@shared_task
def send_notification(users, message):
    channel_layer = get_channel_layer()

    for user in users:
        async_to_sync(channel_layer.group_send)(
            f"notifications_{user.id}",
            {
                "type": "send_notification",
                "message": message,
            }
        )

    return f'Notification sent to ', ', '.join([user.username for user in users])


@shared_task
def send_email(users, message):
    for user in users:
        send_mail(
            'Late Notification',
            message,
            'admin@company.com',  # TODO: Take this from settings
            [user.email],
        )

    return f'Email sent to ', ', '.join([user.username for user in users])
