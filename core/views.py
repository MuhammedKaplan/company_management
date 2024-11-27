from rest_framework import viewsets
from .models import Employee, CheckInOut, LeaveRequest
from .serializers import EmployeeSerializer, CheckInOutSerializer, LeaveRequestSerializer
from .tasks import send_late_notification


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CheckInOutViewSet(viewsets.ModelViewSet):
    queryset = CheckInOut.objects.all()
    serializer_class = CheckInOutSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.late_minutes > 0:
            send_late_notification.delay(instance.employee.id)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
