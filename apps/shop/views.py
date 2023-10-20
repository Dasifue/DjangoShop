from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from .models import Category, Product


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


def category_products_view(request, slug):

    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    context = {
        "category": category,
        "products": products,
    }

    return render(request=request, template_name="category_products.html", context=context)


def product_details_view(request, slug):

    product = get_object_or_404(Product, slug=slug)

    context = {
        "product": product
    }

    return render(request=request, template_name="detail.html", context=context)