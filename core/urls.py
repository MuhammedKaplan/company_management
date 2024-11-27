from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, CheckInOutViewSet, LeaveRequestViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'checkinout', CheckInOutViewSet)
router.register(r'leaverequests', LeaveRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
