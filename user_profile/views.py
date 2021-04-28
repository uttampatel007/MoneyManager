from django.shortcuts import render, redirect
from django.conf import settings

User = settings.AUTH_USER_MODEL 
# Create your views here.

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm
from django.contrib.auth import logout




class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_profile:login')
    template_name = 'user_profile/signup.html'



def logout_view(request):
    logout(request)
    return redirect('user_profile:login')