from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.db.models import Q
from itertools import chain

from .models import Category, Product, ProductSizes

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
    sizes = ProductSizes.objects.all().distinct()

    price = request.GET.get('price')

    if price == 'expensive':
        products = products.order_by("-price")
    elif price == 'cheap':
        products = products.order_by("price")


    sizes_ = request.GET.getlist('size')


    if sizes_:
        size_filter = Q()
        for size in sizes_:
            size_filter |= Q(sizes__size=size)

        products = products.filter(size_filter).distinct()
        

    context = {
        "category": category,
        "products": products,
        "sizes": sizes,
    }

    return render(request=request, template_name="category_products.html", context=context)


def product_details_view(request, slug):

    product = get_object_or_404(Product, slug=slug)

    context = {
        "product": product
    }

    return render(request=request, template_name="detail.html", context=context)


def search_view(request):

    search = request.GET.get("search")
    products = Product.objects.filter(
        Q(name__icontains=search) | Q(description__icontains=search)
    )

    context = {
        "products": products
    }

    return render(request=request, template_name="search_results.html", context=context)
