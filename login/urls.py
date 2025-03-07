from django.urls import path
from .views import LogoutView, CustomLoginView , ProfileView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
     path("profile/", ProfileView.as_view(), name="profile")
]
