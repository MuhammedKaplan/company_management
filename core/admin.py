from django.contrib import admin
from .models import Employee, CheckInOut, LeaveRequest, Notification

admin.site.register(Employee)
admin.site.register(CheckInOut)
admin.site.register(LeaveRequest)
admin.site.register(Notification)
