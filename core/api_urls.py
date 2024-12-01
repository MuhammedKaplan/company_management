from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, CheckInView, CheckOutView, LeaveRequestListView, LeaveRequestCreateView, \
    LeaveRequestApprovalView, get_notifications

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checkin', CheckInView.as_view(), name='checkin'),
    path('checkout', CheckOutView.as_view(), name='checkout'),
    path('checkout<int:employee_id>', CheckOutView.as_view(), name='checkout-with-id'),
    path('leaverequests', LeaveRequestListView.as_view(), name='leave-request-list'),
    path('leaverequests/create', LeaveRequestCreateView.as_view(), name='leave-request-create'),
    path('leaverequests/<int:leave_request_id>/<str:status>', LeaveRequestApprovalView.as_view(),
         name='leave-request-approval'),
    path('notifications', get_notifications, name='get-notifications'),
]
