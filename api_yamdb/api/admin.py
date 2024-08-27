from django.contrib import admin
from .models import Categories, Genres, Titles, Reviews, CustomUser

# (｡◕‿◕｡)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """Настройки отображения модели Categories в административной панели."""

    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    """Настройки отображения модели Genres в административной панели."""

    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    """Настройки отображения модели Titles в административной панели."""

    list_display = (
        'name',
        'year',
        'description',
        'category',
        'created_at',
        'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'genre', 'year')


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Настройки отображения модели Reviews в административной панели."""

    list_display = ('title', 'author', 'score', 'created_at', 'updated_at')
    search_fields = ('title__name', 'author__username', 'text')
    list_filter = ('score', 'created_at')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Настройки отображения модели CustomUser в административной панели."""

    list_display = ('username',
                    'email',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'is_superuser'
                    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser')
