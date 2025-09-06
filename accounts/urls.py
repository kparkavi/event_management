from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from . import views

def auth_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', auth_redirect, name='auth-redirect'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]