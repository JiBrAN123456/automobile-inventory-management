from django.urls import path
from .views import LogoutView, CustomLoginView , ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Generates Access & Refresh tokens
    TokenRefreshView,      # Generates a new Access token using Refresh token
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
     path("profile/", ProfileView.as_view(), name="profile")
]
