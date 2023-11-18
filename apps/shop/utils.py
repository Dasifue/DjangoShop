from .models import Cart

def get_or_create_cart(request):
    user = request.user

    cart = Cart.objects.filter(status=Cart.ACTIVE, user=user).order_by("-created").first()

    if cart is None:
        cart = Cart.objects.create(user=user)

    return cart