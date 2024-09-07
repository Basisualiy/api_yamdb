from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

# ｡◕‿‿◕｡


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValueError(f'Год выпуска не может быть больше {current_year}.')
    if value < 0:
        raise ValueError('Год выпуска не может быть отрицательным.')


class BaseModel(models.Model):
    """Абстрактная базовая модель."""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        """Генерирует slug из названия, если он не указан."""
        if not self.slug:
            self.slug = slugify(self.name)
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        """Мета класс абстрактной базовой модели."""

        abstract = True
        ordering = ('name',)

    def __str__(self):
        """Описание объекта."""
        return self.name


class Category(BaseModel):
    """Модель для хранения категорий (типов) произведений."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):
    """Модель для хранения жанров произведений."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель для хранения произведений, к которым пишут отзывы."""

    name = models.CharField('Произведение', max_length=256)
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
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


class Review(models.Model):
    """Модель для хранения отзывов на произведения."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
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
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]

    def __str__(self):
        """Описание отзыва."""
        return f'{self.author.username} - {self.title.name}'


class Comments(models.Model):
    """Модель для хранения комментариев к отзывам на произведения."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        """Мета класс комментария."""

        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Описание комментария."""
        return f'{self.author.username} - {self.review.title.name}'
