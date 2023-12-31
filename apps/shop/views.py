import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .filters import ProductFilter
from .forms import CartProductForm
from .utils import get_or_create_cart
from .models import (
    Category, 
    Product, 
    ProductSizes, 
    ProductColors, 
    CartProduct, 
    PromoCode, 
    Cart,
    )

from ..account.forms import ProfileForm


class IndexView(ListView):
    model = Category
    queryset = Category.objects.exclude(parent=None)
    template_name = "index.html"
    context_object_name = "subcategories"


class CategoryProductsView(DetailView):
    model = Category
    queryset = Category.objects.exclude(parent=None)
    template_name = "category_products.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    


def index_view(request):

    subcategories = Category.objects.exclude(parent=None)

    context = {
        "subcategories": subcategories
    }

    return render(request=request, template_name="index.html", context=context)


def category_products_view(request, slug=None):

    if slug is None:
        queryset = Product.objects.all()
    else:
        queryset = Product.objects.filter(category__slug=slug)

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

    return render(request=request, template_name="category_products.html", context=context)


def product_details_view(request, slug):

    product = get_object_or_404(Product, slug=slug)

    context = {
        "product": product
    }

    return render(request=request, template_name="detail.html", context=context)


@login_required
def add_to_cart_view(request, slug):
    if request.method == "POST":
        print(request.POST)
        product = get_object_or_404(Product, slug=slug)
        form = CartProductForm(data=request.POST)
        cart = get_or_create_cart(request)
        if form.is_valid():
            cart_product = form.save(commit=False)
            cart_product.cart = cart

            updated = False
            for c_p in cart.cart_products.all():
                if c_p.product == product and c_p.color == form.cleaned_data["color"] and c_p.size == form.cleaned_data["size"]:
                    c_p.quantity += form.cleaned_data["quantity"]
                    c_p.save()
                    updated = True
                    break

            if updated == False:
                cart_product.product = product
                cart_product.save()
            messages.info(request=request, message="Succesfully added to cart!")
        else:        
            messages.error(request=request, message=form.errors)
            

    return redirect(request.META.get('HTTP_REFERER', '/'))
    



@login_required
def cart_view(request):
    cart = get_or_create_cart(request=request)

    if request.method == "POST":
        promo_code = PromoCode.objects.filter(name=request.POST.get("coupon")).first()
        if promo_code is not None:
            cart.promo = promo_code
            cart.save()
            messages.info(request=request, message="Promo code was applied!")
        else:
            messages.info(request=request, message="Promo not found!")

    context = {
        "cart": cart,
    }

    return render(request=request, template_name="cart.html", context=context)


@login_required
def delete_from_cart_view(request, pk):
    cart_product = get_object_or_404(CartProduct, pk=pk)

    cart = get_or_create_cart(request=request)

    if cart_product in cart.cart_products.all():
        cart_product.delete()

    return redirect("shop:cart")

@login_required
def checkout_view(request):
    cart = get_or_create_cart(request=request)
    form = ProfileForm(instance=request.user)

    if request.method == "POST":
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid() and cart.cart_products.count() > 0:
            form.save()
            cart.status = Cart.WAITING
            cart.save()
        else:
            messages.info(request=request, message="Cart must contain at least one product!")

    url = "https://restcountries.com/v3.1/all?fields=name"
    response = requests.get(url=url)

    countries = [country['name']['official'] for country in response.json()]
    countries.sort()

    context = {
        "cart": cart,
        "form": form,
        "countries": countries,
    }

    return render(request=request, template_name="checkout.html", context=context)