from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("signup/", views.signup, name="signup"),
    path('logout/', views.logout_view, name='logout'),

    path("dash/", views.dashboard, name="dashboard"),
    path("dash/admin", views.admindashboard, name="admindashboard"),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/update/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    path("apply/", views.apply, name="apply"),
    path('update/<int:aplid>/', views.update_leave_status, name='update_leave_status'),
    path("history/", views.history, name="history"),

]