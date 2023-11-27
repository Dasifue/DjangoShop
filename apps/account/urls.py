from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("register/", view=views.register_view, name="register"),
    path("login/", view=views.login_view, name="login"),
    path("logout/", view=views.logout_view, name="logout"),
    path("profile/", view=views.my_profile_view, name="my_profile"),
    path("profile/update/", view=views.profile_update_view, name="profile_update"),
    path("profile/password/reset/", view=views.reset_password_view, name="reset_password"),

    path("favorites/", view=views.favorites_view, name="favorites"),
    path("favorites/add/<slug:slug>", view=views.add_to_favorites_view, name="add_to_favorites"),
    path("favorites/remove/<slug:slug>", view=views.remove_from_favorites_view, name="remove_from_favorites"),
]