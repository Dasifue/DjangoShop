from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator

from .models import Category, Clothes

# Create your views here.
def index(request):

    return render(request, "home.html")


def search_clothes(request):

    search = request.GET.get("search")
    page = request.GET.get("page", 1)

    if search is not None:
        clothes = Clothes.objects.filter(name__icontains=search)
    else:
        clothes = Clothes.objects.all()

    paginator = Paginator(clothes, 1)
    clothes = paginator.page(page)

    context = {
        "clothes": clothes
    }
    return render(request, "search.html", context)


def get_clothes_by_category(request, category_id):
    "Функция фильтрует одежду по категории и возвращает html"

    clothes = Clothes.objects.filter(category__id = category_id)

    page = request.GET.get("page", 1)

    paginator = Paginator(clothes, 20)
    clothes = paginator.page(page)

    context = {
        "clothes": clothes,
    }

    return render(request, "clothes_by_category.html", context)


def get_clothes_by_id(request, id):
    "Функция возвращает одежду по ID"

    try:
        clothes = Clothes.objects.get(id=id)
    except Clothes.DoesNotExist:
        return HttpResponseNotFound("Clothes not found")

    context = {
        "clothes": clothes
    }
    return render(request, "clothes_detail.html", context)
