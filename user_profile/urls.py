from django.urls import path
from .views import SignUpView, logout_view
from django.contrib.auth import views as auth_views


app_name = 'user_profile'



urlpatterns = [
	path('signup/', SignUpView.as_view(), name='signup'),
	path('login/',auth_views.LoginView.as_view(template_name='user_profile/login.html',redirect_authenticated_user=True),name='login'), 
	path('logout/',logout_view, name='logout')
]	