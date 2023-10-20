from .models import Category

def categories_processor(request):
    categories = Category.objects.filter(parent=None)

    context = {
        "categories": categories
    }

    return context