from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    ROLE_CHOICES = [
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STAFF')
    start_date = models.DateField()
    remaining_leaves = models.FloatField(default=15)  # TODO: Take default value from settings

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class CheckInOut(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    late_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.employee.user.username} - {self.check_in_time.date()}"


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    LEAVE_TYPE_CHOICES = [
        ('ANNUAL', 'Annual'),
        ('SICK', 'Sick'),
        ('MATERNITY', 'Maternity'),
        ('UNPAID', 'Unpaid'),]

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"

    @property
    def leave_duration(self):
        return (self.end_date - self.start_date).days + 1


class Notification(models.Model):
    ROLE_CHOICES = [
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.message[:20]}"
