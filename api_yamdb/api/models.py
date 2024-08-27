from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.utils import timezone

from .models import CustomUser

# ｡◕‿‿◕｡


class Categories(models.Model):
    """Модель для хранения категорий (типов) произведений."""

    name = models.CharField(
        verbose_name='Категория',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def save(self, *args, **kwargs):
        """Генерирует slug из названия категории, еесли он не указан."""
        if not self.slug:
            self.slug = slugify(self.name)
        super(Categories, self).save(*args, **kwargs)

    class Meta:
        """Мета класс категории."""

        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Описание категории."""
        return self.name


class Genres(models.Model):
    """Модель для хранения жанров произведений."""

    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Жанр',
    )
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        """Генерирует slug из названия жанра, если он не указан."""
        if not self.slug:
            self.slug = slugify(self.name)
        super(Genres, self).save(*args, **kwargs)

    class Meta:
        """Мета класс жанра."""

        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Описание жанра."""
        return self.name


class Titles(models.Model):
    """Модель для хранения произведений, к которым пишут отзывы."""

    name = models.CharField('Произведение', max_length=256)
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MaxValueValidator(timezone.now().year),
            MinValueValidator(0)
        ]
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        """Мета класс произведения."""

        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Описание произведения."""
        return self.name


class Reviews(models.Model):
    """Модель для хранения отзывов на произведения."""

    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10'),
        ],
        verbose_name='Рейтинг',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        """Мета класс отзыва."""

        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('title', 'author')

    def __str__(self):
        """Описание отзыва."""
        return f'{self.author.username} - {self.title.name}'


class Comments(models.Model):
    """Модель для хранения комментариев к отзывам на произведения."""

    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        """Мета класс комментария."""

        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Мета класс комментария."""
        return f'{self.author.username} - {self.review.title.name}'
