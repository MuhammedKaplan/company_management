from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, CheckInView, CheckOutView, LeaveRequestViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'leaverequests', LeaveRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checkin', CheckInView.as_view(), name='checkin'),
    path('checkout', CheckOutView.as_view(), name='checkout'),
    path('checkout/<int:employee_id>', CheckOutView.as_view(), name='checkout_with_id'),
]
