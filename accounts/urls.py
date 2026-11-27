from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, ProfileUpdateView, StyledLoginView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("login/", StyledLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]