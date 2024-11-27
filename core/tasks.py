from celery import shared_task
from django.core.mail import send_mail
from .models import Employee


@shared_task
def send_late_notification(employee_id):
    employee = Employee.objects.get(id=employee_id)
    send_mail(
        'Late Notification',
        f'{employee.user.username} is late today.',
        'admin@company.com',
        ['manager@company.com'],
    )
    return f'Email sent to {employee.user.username}'
