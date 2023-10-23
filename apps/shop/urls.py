from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", view=views.index_view, name="index"),
    path("products/<slug:slug>", view=views.category_products_view, name="category_products"),
    path("products/details/<slug:slug>", view=views.product_details_view, name="product_details"),
    path("products/search/", view=views.search_view, name="search")
]