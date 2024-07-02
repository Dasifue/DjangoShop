from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Cart, CartProduct
from shop.models import Clothes

@login_required()
def get_cart(request):
    cart = Cart.objects.get(user=request.user)

    context = {
        "cart": cart
    }
    return render(request, "cart.html", context)


@login_required
def add_to_cart(request, clothes_id):
    clothes = get_object_or_404(Clothes, id=clothes_id)
    quantity = request.GET.get("quantity", 1)

    for product in request.user.cart.products.all():
        if product.clothes == clothes:
            product.quantity += int(quantity)
            product.save()
            break
    else:
        CartProduct.objects.create(
            cart=request.user.cart,
            clothes=clothes,
            quantity=quantity,
        )
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def change_quantity(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, id=cart_product_id)
    quantity = request.GET["quantity"]

    cart_product.quantity = abs(int(quantity))
    cart_product.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def delete_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, id=cart_product_id)
    cart_product.delete()
    return redirect(request.META.get("HTTP_REFERER", "/"))
