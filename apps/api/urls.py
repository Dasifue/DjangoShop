from django.urls import path, include

from . import views

urlpatterns = [
    path("register/", view=views.RegisterAPIView.as_view()),
    path("", include("djoser.urls.authtoken")),
    path("profile/update/", view=views.ProfileUpdateAPIView.as_view()),
    path("profile/password/reset/", view=views.ResetPasswordAPIView.as_view())
]