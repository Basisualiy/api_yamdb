from django.contrib import admin
from .models import Category, Genre, Title, Review


# (｡◕‿◕｡)


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    """Настройки отображения модели Categories в административной панели."""

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    """Настройки отображения модели Genres в административной панели."""

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    """Настройки отображения модели Titles в административной панели."""

    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name', 'description')
    list_filter = ('category', 'genre', 'year')


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    """Настройки отображения модели Reviews в административной панели."""

    list_display = ('title', 'author', 'score')
    search_fields = ('title__name', 'author__username', 'text')
    list_filter = ('score',)
