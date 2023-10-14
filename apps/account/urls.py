from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("register/", view=views.register_view, name="register"),
    path("login/", view=views.login_view, name="login"),
    path("logout/", view=views.logout_view, name="logout"),
    path("profile/", view=views.my_profile_view, name="my_profile"),
    path("profile/update/", view=views.profile_update_view, name="profile_update"),
]