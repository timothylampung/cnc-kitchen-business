from django.shortcuts import render

# Create your views here.
from app.models import Recipe


def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', context={'data': 'name', 'recipes': recipes})
