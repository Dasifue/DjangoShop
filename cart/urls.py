from django.urls import path

from .views import (
    get_cart,
    add_to_cart,
    change_quantity,
    delete_from_cart,
    reset_cart,
)


urlpatterns = [
    path("", get_cart, name="get_cart"),
    path("add/<int:clothes_id>", add_to_cart, name="add_to_cart"),
    path("change/quantity/<int:cart_product_id>", change_quantity, name="change_quantity"),
    path("delete/<int:cart_product_id>", delete_from_cart, name="delete_from_cart"),
    path("reset/", reset_cart, name="reset_cart"),
]
