from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('auth/redirect', views.redirect_user, name='redirect_user'),
    path('auth/setup', views.setup, name='setup'),
    path('auth/login/', views.login_user, name='login_user'),
    path('auth/logout/', views.logout_user, name='logout_user'),
    path('auth/setup/pharmacist/', views.pharmacist_setup, name='pharmacist_setup'),
    path('auth/setup/patient/', views.patient_setup, name='patient_setup'),
    


]