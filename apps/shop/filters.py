import django_filters
from django import forms

from .models import Product

class ProductFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ("price", "sizes", "colors")
        order_by = (
            ("price", "From cheap to expensive"),
            ("-price", "From expensive to cheap"),
            ("created", "From oldest to newest"),
            ("-created", "From newest to oldest")
        )
       
