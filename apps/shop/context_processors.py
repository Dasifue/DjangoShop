from .models import Category
from .utils import get_or_create_cart

def categories_processor(request):
    categories = Category.objects.filter(parent=None)

    context = {
        "categories": categories
    }

    return context


def cart_products_count(request):

    user = request.user

    if user.is_authenticated:
        cart = get_or_create_cart(request)
        count = 0
        for product in cart.cart_products.all():
            count += product.quantity
    else:
        count = 0

    context = {
        "cart_products_count": count
    }

    return context