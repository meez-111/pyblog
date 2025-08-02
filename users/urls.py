from django.urls import path
from . import views


urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("login", views.user_login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.user_logout, name="logout"),
    path("changepassword", views.user_password_change, name="changepassword"),
]
