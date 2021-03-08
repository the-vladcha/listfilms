from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'country', 'year', 'director', 'category', 'created_at', 'rating', 'is_watched')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', 'year', 'director', 'country')
    readonly_fields = ('created_at', 'get_photo', 'rating')
    fields = (
        'title', 'slug', 'category', 'genre', 'year', 'country', 'director', 'actors', 'photo', 'get_photo',
        'is_watched', 'rating', 'mark', 'comment', 'counter', 'created_at')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}", height="100">')

        return '-'

    get_photo.short_description = 'Постер'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
