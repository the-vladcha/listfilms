from django.shortcuts import render
from django.http import HttpResponse

from fseen.models import Film


def index(request):
    films = Film.objects.order_by('rating')
    context = {
        'films': films,
        'title': 'Список фильмов'
    }
    return render(request, template_name='fseen/index.html', context=context)
