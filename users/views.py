from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .models import User
from .forms import RegisterForm, LoginForm

from cart.models import Cart

def register_view(request):

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            user.save()
            Cart.objects.create(user=user)
            login(request, user)
            return redirect("index")

    context = {
        "form": form
    }

    return render(request, "register.html", context)


def login_view(request):

    form = LoginForm()
    message = ""

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                message = "Check your data"

    context = {
        "form": form,
        "message": message,
    }

    return render(request, "login.html", context)


def logout_view(request):

    return render(request, "logout.html")


def logout_commit_view(request):
    
    logout(request)
    return redirect("login")