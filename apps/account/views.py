from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, ProfileForm, ResetPasswordForm
from .models import User
from ..shop.models import Product, ProductColors, ProductSizes
from ..shop.filters import ProductFilter

def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return redirect("shop:index")
        
        context = {
            "form": form,
            "error": "Registration failed"
        }
        return render(request=request, template_name="register.html", context=context)
    
    context = {
        "form": form
    }

    return render(request=request, template_name="register.html", context=context)


def login_view(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(username, password, "\n\n\n")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("shop:index")
        
        context = {
            "form": form,
            "error": "Authentication failed!"
        }
        return render(request=request, template_name="login.html", context=context)

    context = {
        "form": form,
    }

    return render(request=request, template_name="login.html", context=context)

def logout_view(request):
    logout(request)
    return redirect("account:login")


@login_required
def my_profile_view(request):
    user = request.user

    context = {
        "user": user,
    }

    return render(request=request, template_name="my_profile.html", context=context)


@login_required
def profile_update_view(request):
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
        else:
            context = {
             "form": form
            }
            return render(request=request, template_name="profile_update.html", context=context)

    context = {
        "form": form
    }

    return render(request=request, template_name="profile_update.html", context=context)


@login_required
def reset_password_view(request):
    form = ResetPasswordForm()

    if request.method == "POST":
        form = ResetPasswordForm(data=request.POST, instance=request.user)
        password_failed = None
        if form.is_valid():
            user = authenticate(request=request, username=request.user.username, password=form.cleaned_data.get("password"))
            if user is not None:
                user: User = form.save(commit=False)
                user.set_password(raw_password=form.cleaned_data.get("new_password"))
                user.save()
                return redirect("account:my_profile")
            password_failed = "wrong password!"
        context = {
            "form": form,
            "error": "Failed to reset password",
            "password": password_failed,
        }
        return render(request=request, template_name="reset_password.html", context=context)

    context = {
        "form": form,
    }
    return render(request=request, template_name="reset_password.html", context=context)


@login_required
def add_to_favorites_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    user = request.user

    if product not in user.favorites.all():
        user.favorites.add(product)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_from_favorites_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    user = request.user

    if product in user.favorites.all():
        user.favorites.remove(product)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def favorites_view(request):
    user: User = request.user

    queryset = user.favorites.all()

    order_by = request.GET.get("order_by")
    if order_by is not None:
        queryset = queryset.order_by(order_by)
    
    filter = ProductFilter(data=request.GET, queryset=queryset)


    sizes = ProductSizes.objects.all().distinct()
    colors = ProductColors.objects.all().distinct()

    context = {
        "sizes": sizes,
        "colors": colors,
        "filter": filter,
    }

    return render(request=request, template_name="favorites.html", context=context)