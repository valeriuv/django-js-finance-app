from .views import EmailValidationView, LogoutView, RegistrationView, UsernameValidationView, VerificationView, LoginView, RequestPasswordResetEmail
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', csrf_exempt(LoginView.as_view()), name='login'),
    path('logout', csrf_exempt(LogoutView.as_view()), name='logout'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('request-reset-link', RequestPasswordResetEmail.as_view(), name='request-password'),
]
