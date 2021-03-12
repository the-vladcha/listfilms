from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('<str:slug>/', get_category, name='category'),
    path('watch/<str:slug>/', view_film, name='view_film'),
]