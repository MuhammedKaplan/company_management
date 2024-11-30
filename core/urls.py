from django.urls import path

from .views import dashboard, login_view, manager_login_view, manager_dashboard, notification_list, \
    manage_leave_requests, update_leave_request_status, manage_employees, leave_history, logout_view, monthly_report, \
    my_leaves

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('manager/login/', manager_login_view, name='manager-login'),
    path('logout/', logout_view, name='logout'),
    path('manager/dashboard/', manager_dashboard, name='manager-dashboard'),
    path('notifications/', notification_list, name='notification-list'),
    path('manager/notifications/', notification_list, name='manager-notification-list'),
    path('manager/leaverequests/', manage_leave_requests, name='manage-leave-requests'),
    path('manager/leaverequests/<int:leave_request_id>/<str:status>/', update_leave_request_status,
         name='update-leave-request-status'),
    path('manager/employees/', manage_employees, name='manage-employees'),
    path('manager/leavehistory/', leave_history, name='leave-history'),
    path('manager/monthlyreport/', monthly_report, name='monthly-report'),
    path('myleaves/', my_leaves, name='my-leaves'),
]
