from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    set_cookie_viev,
    get_cookie_viev,
    set_session_viev,
    get_session_viev,
    AboutMeView,
    RegisterView,
    FooBarYou,
    UserListView,
    UserUpdateViev,
)
from django.contrib.auth.views import LoginView

app_name = "myauth"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="myauth:login"), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("user/<int:pk>/", UserUpdateViev.as_view(), name="user_update"),
    path("cookie/get/", get_cookie_viev, name="cookie-get"),
    path("cookie/set/", set_cookie_viev, name="cookie-set"),
    path("session/set/", set_session_viev, name="session-set"),
    path("session/get/", get_session_viev, name="session-get"),
    path("foo-bar/", FooBarYou.as_view(), name="foo-bar"),
]
