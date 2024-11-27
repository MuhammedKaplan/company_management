from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.core.mail import send_mail

from .models import Employee


@shared_task
def send_late_notification(employee_id):
    # Get employee
    employee = Employee.objects.get(id=employee_id)

    # Create message
    message = f'{employee.user.username} is late today.'

    # Send email to manager
    send_mail(
        'Late Notification',
        message,
        'admin@company.com',
        ['manager@company.com'],
    )

    # Send notification to ws
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": message,
        }
    )

    # Return success message
    return f'Email sent to {employee.user.username}'
