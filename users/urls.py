from django.urls import path

from .views import (
    register_view,
    login_view,
    logout_view,
    logout_commit_view,
)


urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("logout/commit/", logout_commit_view, name="logout_commit"),
]