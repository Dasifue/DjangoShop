from .models import User

def favorites_count(request):
    user: User = request.user
    if user.is_authenticated:
        count = user.favorites.count()
    else:
        count = 0
    
    context = {
        "favorites_count": count
    }

    return context