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
    remaining_leaves = models.PositiveIntegerField(default=15)

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

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    days_requested = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.employee.user.username} - {self.status}"
