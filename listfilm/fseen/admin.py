from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True
    list_display = ('title', 'country', 'year', 'display_genre', 'director', 'category', 'rating', 'is_watched')
    list_display_links = ('title',)
    ordering = ['title']
    search_fields = ('title',)
    list_filter = ('category', 'year', 'director', 'country')
    readonly_fields = ('created_at', 'get_photo', 'rating')
    fields = (
        'title', 'slug', 'category', 'genre', 'year', 'country', 'director', 'actors', 'photo', 'get_photo',
        'is_watched', 'rating', 'mark', 'comment', 'counter', 'created_at')

    def display_genre(self, obj):
        return [genre.title for genre in obj.genre.all()]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo}", height="100">')

        return '-'

    display_genre.short_description = 'Жанр'
    get_photo.short_description = 'Постер'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['title']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['title']


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
