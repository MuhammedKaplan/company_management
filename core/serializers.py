import pytz

from datetime import datetime, time

from rest_framework import serializers
from .models import Employee, CheckInOut, LeaveRequest
from .notification import create_notification
from .leave import deduct_leave_for_lateness


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInOut
        fields = ['check_in_time']

    def validate_check_in_time(self, value):
        # Is the date today?
        if value.date() != datetime.now().date():
            raise serializers.ValidationError("Check-in date must be today.")
        # Is the time in weekdays?
        if value.weekday() >= 5:
            raise serializers.ValidationError("Check-in must be on a weekday.")
        return value

    def create(self, validated_data):
        employee = self.context['request'].user.employee

        # Check if there is already a check-in record for today
        today = datetime.now().date()
        if CheckInOut.objects.filter(employee=employee, check_in_time__date=today).exists():
            raise serializers.ValidationError("Check-in already recorded for today.")

        # Expected start time
        tz = pytz.UTC
        expected_start_time = tz.localize(datetime.combine(today, datetime.strptime("08:00:00", "%H:%M:%S").time()))

        # Calculate late minutes
        late_minutes = max(0, int((validated_data['check_in_time'] - expected_start_time).total_seconds() // 60))

        # Deduct leave for lateness
        deduct_leave_for_lateness(employee, late_minutes)

        # Send notification if late
        if late_minutes > 0:
            message = f"{employee.user.username} is late by {late_minutes} minutes."
            create_notification(message, role='MANAGER')

        # Create the check-in record
        return CheckInOut.objects.create(employee=employee, late_minutes=late_minutes, **validated_data)


class CheckOutSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(required=False)

    class Meta:
        model = CheckInOut
        fields = ['employee_id']

    def validate(self, data):
        employee = self.context['request'].user.employee
        today = datetime.now().date()

        employee_id = data.get('employee_id')

        if employee_id:
            try:
                check_in = CheckInOut.objects.get(employee__id=employee_id, check_in_time__date=today)
            except CheckInOut.DoesNotExist:
                raise serializers.ValidationError({"error": "Check-in not found for the provided employee."})
        else:
            try:
                check_in = CheckInOut.objects.get(employee=employee, check_in_time__date=today)
            except CheckInOut.DoesNotExist:
                raise serializers.ValidationError({"error": "Check-in not found for the authenticated user."})

        if check_in.check_out_time is not None:
            raise serializers.ValidationError({"error": "Check-out already recorded."})

        self.check_in = check_in
        return data

    def save(self, **kwargs):
        self.check_in.check_out_time = datetime.now()
        self.check_in.save()
        return self.check_in


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)
    requested_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    leave_duration = serializers.IntegerField(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'leave_type', 'start_date', 'end_date',
            'reason', 'status', 'requested_at', 'updated_at', 'leave_duration'
        ]
