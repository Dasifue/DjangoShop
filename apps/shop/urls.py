from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", view=views.index_view, name="index"),
    path("products/", view=views.category_products_view, name="category_products"),
    path("products/<slug:slug>", view=views.category_products_view, name="category_products"),
    path("products/details/<slug:slug>", view=views.product_details_view, name="product_details"),

    path("cart/", view=views.cart_view, name="cart"),
    path("cart/add/<slug:slug>", view=views.add_to_cart_view, name="add_to_cart"),
    path("cart/remove/<int:pk>", view=views.delete_from_cart_view, name="delete_from_cart"),
    path("cart/checkout/", view=views.checkout_view, name="checkout")
]