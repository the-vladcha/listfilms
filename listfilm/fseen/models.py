from django.db import models
from django.urls import reverse

'''
Film
=============



'''


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Genre(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('genre', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['title']


class Director(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('director', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Режисер'
        verbose_name_plural = 'Режисеры'
        ordering = ['name']


class Actor(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'
        ordering = ['name']


class Film(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)
    genre = models.ManyToManyField(Genre, related_name='films', verbose_name='Жанр')
    country = models.CharField(max_length=50, verbose_name='Страна')
    year = models.IntegerField(verbose_name='Год выпуска')
    actors = models.ManyToManyField(Actor, related_name='films', verbose_name='Актер')
    comment = models.TextField(max_length=150, verbose_name='Комментарий', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    counter = models.IntegerField(default=0, verbose_name='Число просмотров')
    photo = models.ImageField(verbose_name='Постер', upload_to='photos/%Y/%m/%d/', blank=True)
    is_watched = models.BooleanField(default=True, verbose_name='Просмотренно')
    mark = models.IntegerField(verbose_name='Моя оценка', blank=True, null=True)
    rating = models.CharField(max_length=5, verbose_name='Рейтинг', default='-')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='films', verbose_name='Категория')
    director = models.ForeignKey(Director, on_delete=models.PROTECT, related_name='films', blank=True,
                                 verbose_name='Режиссер')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('film', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['title']
