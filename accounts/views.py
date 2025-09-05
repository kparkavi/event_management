from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('profile')  # Add this line

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'
    login_url = reverse_lazy('login')  # Add this line