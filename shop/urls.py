from django.urls import path

from .views import (
    index,
    get_clothes_by_category,
    get_clothes_by_id,
    search_clothes,
)

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>', get_clothes_by_category, name="get_clothes_by_category"),
    path('clothes/<int:id>', get_clothes_by_id, name="get_clothes_by_id"),
    path('clothes/search/', search_clothes, name="search_clothes"),
]