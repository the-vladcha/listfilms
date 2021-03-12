from django.shortcuts import render, get_object_or_404

from fseen.models import Film, Category


def index(request):
    films = Film.objects.order_by('rating')
    categories = Category.objects.all()
    context = {
        'films': films,
        'title': 'Список фильмов',
        'categories': categories,
    }
    return render(request, template_name='fseen/index.html', context=context)


def get_category(request, slug):
    category_id = Category.objects.get(slug=slug).pk
    films = Film.objects.filter(category_id=category_id)
    # category = Category.objects.get(category_id=category_id)
    return render(request, 'fseen/category.html', {'films': films})


def view_film(request, slug):
    # film_item = Film.objects.get(slug=slug)
    film_item = get_object_or_404(Film, slug=slug)
    return render(request, 'fseen/view_film.html', {'film_item': film_item})