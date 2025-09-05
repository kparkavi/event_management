from django.urls import path
from django.shortcuts import redirect
from . import views

def auth_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', auth_redirect, name='auth-redirect'),  # Redirects /api/auth/ to login
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]