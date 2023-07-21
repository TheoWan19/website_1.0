from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.customer_home, name="customer-home"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('employee/', views.employee_view, name='employee-home'),
    path('signup/customer/', views.CustomerSignUpView.as_view(), name='customer-signup'),
    path('signup/employee/', views.EmployeeSignUpView.as_view(), name='employee-signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
]