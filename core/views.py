import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, ExpressionWrapper, F, DurationField
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employee, LeaveRequest, CheckInOut, Notification
from .notification import create_notification
from .serializers import EmployeeSerializer, CheckInSerializer, LeaveRequestSerializer, CheckOutSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.employee.role == 'MANAGER':
            return Employee.objects.all()
        return Employee.objects.filter(user=self.request.user)


class CheckInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CheckInSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Check-in successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckOutView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CheckOutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Check-out successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status = request.GET.get('status')

        leave_requests = LeaveRequest.objects.filter(employee=request.user).order_by('-requested_at')

        if status:
            leave_requests = leave_requests.filter(status=status)

        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data)


class LeaveRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user)
            return Response({"message": "Leave request created successfully."}, status=201)
        return Response(serializer.errors, status=400)


class LeaveRequestApprovalView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, leave_request_id, status):
        try:
            leave_request = LeaveRequest.objects.get(id=leave_request_id)
            if status not in ['APPROVED', 'REJECTED']:
                return Response({"error": "Invalid status."}, status=400)

            if leave_request.status != 'PENDING':
                return Response({"error": "Leave request is not pending approval."}, status=400)

            leave_request.status = status
            leave_request.save()
            return Response({"message": f"Leave request {status.lower()} successfully."}, status=200)
        except LeaveRequest.DoesNotExist:
            return Response({"error": "Leave request not found."}, status=404)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token[0].key, 'role': user.employee.role})
        else:
            messages.error(request, 'Invalid username or password.')
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return render(request, 'core/login.html')


def manager_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.employee.role == 'MANAGER':
            login(request, user)
            token = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token[0].key, 'role': user.employee.role})
        else:
            messages.error(request, 'Invalid username or password, or you do not have manager access.')
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return render(request, 'core/manager_login.html')


def logout_view(request):
    logout(request)
    role = request.COOKIES.get('user_role')
    if role == 'manager':
        return redirect('manager-login')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user

    remaining_leaves = user.employee.remaining_leaves

    total_used_leaves = LeaveRequest.objects.filter(
        employee=user,
        start_date__year=datetime.now().year,
        status='APPROVED'
    ).count()

    pending_leave_request = LeaveRequest.objects.filter(
        employee=user,
        status='PENDING'
    ).order_by('-requested_at').first()

    today = datetime.now()
    total_late_minutes = CheckInOut.objects.filter(
        employee=user.employee,
        check_in_time__year=today.year,
        check_in_time__month=today.month
    ).aggregate(total_late_minutes=Sum('late_minutes'))['total_late_minutes'] or 0

    return render(request, 'core/dashboard.html', {
        'remaining_leaves': remaining_leaves,
        'total_used_leaves': total_used_leaves,
        'pending_leave_request': pending_leave_request,
        'total_late_minutes': total_late_minutes
    })


@login_required
def manager_dashboard(request):
    if not request.user.employee.role == 'MANAGER':
        return redirect('dashboard')

    total_employees = Employee.objects.count()
    pending_leave_requests = LeaveRequest.objects.filter(status='PENDING').count()
    today = datetime.now().date()
    late_employees_today = CheckInOut.objects.filter(
        check_in_time__date=today,
        late_minutes__gt=0
    ).count()

    leave_usage_raw = LeaveRequest.objects.filter(
        start_date__year=datetime.now().year,
        status='APPROVED'
    ).annotate(
        duration=ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField())
    ).values(
        'employee__first_name', 'employee__last_name'
    ).annotate(
        total_days=Sum('duration')
    )

    leave_usage = [
        {
            'first_name': leave['employee__first_name'],
            'last_name': leave['employee__last_name'],
            'total_days': leave['total_days'].days
        }
        for leave in leave_usage_raw
    ]

    late_statistics = CheckInOut.objects.filter(
        late_minutes__gt=0
    ).values(
        'employee__user__first_name', 'employee__user__last_name'
    ).annotate(
        total_late_minutes=Sum('late_minutes')
    )

    leave_usage_json = json.dumps(leave_usage)
    late_statistics_json = json.dumps(list(late_statistics))

    return render(request, 'core/manager_dashboard.html', {
        'total_employees': total_employees,
        'pending_leave_requests': pending_leave_requests,
        'late_employees_today': late_employees_today,
        'leave_usage': leave_usage_json,
        'late_statistics': late_statistics_json,
    })


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:5]
    return JsonResponse(list(notifications.values('message', 'created_at')), safe=False)


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'core/notification_list.html', {'notifications': notifications})


@login_required
def manage_leave_requests(request):
    if not request.user.employee.role == 'MANAGER':
        return redirect('dashboard')

    pending_requests = LeaveRequest.objects.filter(status='PENDING').order_by('-start_date')
    approved_requests = LeaveRequest.objects.filter(status='APPROVED').order_by('-start_date')
    rejected_requests = LeaveRequest.objects.filter(status='REJECTED').order_by('-start_date')

    return render(request, 'core/manage_leave_requests.html', {
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
    })


@login_required
def update_leave_request_status(request, leave_request_id, status):
    if not request.user.employee.role == 'MANAGER':
        return redirect('dashboard')

    leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)

    if status in ['APPROVED', 'REJECTED']:
        leave_request.status = status
        leave_request.save()

        message = (f"Your leave request from {leave_request.start_date} to {leave_request.end_date} "
                   f"has been {status.lower()}.")
        create_notification(message, users=[leave_request.employee.id])

    return redirect('manage-leave-requests')


@login_required
def manage_employees(request):
    if not request.user.employee.role == 'MANAGER':
        return redirect('dashboard')

    employees = Employee.objects.select_related('user').all()
    return render(request, 'core/manage_employees.html', {'employees': employees})


@login_required
def leave_history(request):
    if not request.user.employee.role == 'MANAGER':
        return redirect('dashboard')

    employee_id = request.GET.get('employee_id')
    employee = Employee.objects.filter(id=employee_id).select_related('user').first()

    if not employee:
        return render(request, 'core/leave_history.html', {
            'error_message': 'Employee not found.',
            'leave_requests': [],
            'employee': None
        })

    leave_requests = LeaveRequest.objects.filter(employee=employee.user).order_by('-start_date')
    return render(request, 'core/leave_history.html', {
        'employee': employee,
        'leave_requests': leave_requests
    })


@login_required
def monthly_report(request):
    if not request.user.employee.role == 'MANAGER':
        return redirect('dashboard')

    today = datetime.now().date()

    monthly_work_hours = CheckInOut.objects.filter(
        check_in_time__year=today.year,
        check_in_time__month=today.month
    ).values(
        'employee__user__first_name', 'employee__user__last_name'
    ).annotate(
        total_work_hours=Sum(F('check_out_time') - F('check_in_time'), output_field=DurationField())
    )

    late_statistics = CheckInOut.objects.filter(
        late_minutes__gt=0,
        check_in_time__year=today.year,
        check_in_time__month=today.month
    ).values(
        'employee__user__first_name', 'employee__user__last_name'
    ).annotate(
        total_late_minutes=Sum('late_minutes')
    )

    return render(request, 'core/monthly_report.html', {
        'monthly_work_hours': monthly_work_hours,
        'late_statistics': late_statistics
    })


@login_required
def my_leaves(request):
    leave_requests = LeaveRequest.objects.filter(employee=request.user).order_by('-start_date')

    return render(request, 'core/my_leaves.html', {
        'leave_requests': leave_requests
    })
