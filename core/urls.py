from django.urls import path
from .views import dashboard, login_view, manager_login_view, manager_dashboard

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('manager/login/', manager_login_view, name='manager-login'),
    path('manager/dashboard', manager_dashboard, name='manager-dashboard'),
]